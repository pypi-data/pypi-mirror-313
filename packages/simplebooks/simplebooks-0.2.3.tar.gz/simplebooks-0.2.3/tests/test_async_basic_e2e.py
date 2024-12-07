from asyncio import run
from context import asyncql, simplebooks
from genericpath import isfile
from sqlite3 import OperationalError
from time import time
import os
import unittest


DB_FILEPATH = 'tests/test.db'
MIGRATIONS_PATH = 'tests/migrations'


class TestAsyncBasicE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        asyncql.Identity.connection_info = DB_FILEPATH
        asyncql.Currency.connection_info = DB_FILEPATH
        asyncql.Ledger.connection_info = DB_FILEPATH
        asyncql.Account.connection_info = DB_FILEPATH
        asyncql.AccountCategory.connection_info = DB_FILEPATH
        asyncql.Entry.connection_info = DB_FILEPATH
        asyncql.Transaction.connection_info = DB_FILEPATH
        asyncql.Vendor.connection_info = DB_FILEPATH
        asyncql.Customer.connection_info = DB_FILEPATH
        super().setUpClass()

    def setUp(self):
        if isfile(DB_FILEPATH):
            os.remove(DB_FILEPATH)
        super().setUp()

    def tearDown(self):
        for file in os.listdir(MIGRATIONS_PATH):
            if isfile(f'{MIGRATIONS_PATH}/{file}'):
                os.remove(f'{MIGRATIONS_PATH}/{file}')
        if isfile(DB_FILEPATH):
            os.remove(DB_FILEPATH)
        super().tearDown()

    def automigrate(self):
        simplebooks.publish_migrations(MIGRATIONS_PATH)
        simplebooks.automigrate(MIGRATIONS_PATH, DB_FILEPATH)

    def test_e2e(self):
        with self.assertRaises(OperationalError):
            run(asyncql.Account.query().count())
        self.automigrate()
        assert run(asyncql.Account.query().count()) == 0

        # setup account categories
        equity_acct_cat = run(asyncql.AccountCategory.insert({
            'name': 'Equity',
            'ledger_type': asyncql.LedgerType.PRESENT,
            'destination': 'Balance Sheet',
        }))
        assert equity_acct_cat is not None
        assert run(asyncql.AccountCategory.find(equity_acct_cat.id)) is not None
        asset_acct_cat = run(asyncql.AccountCategory.insert({
            'name': 'Asset',
            'ledger_type': asyncql.LedgerType.PRESENT,
            'destination': 'Balance Sheet',
        }))
        liability_acct_cat = run(asyncql.AccountCategory.insert({
            'name': 'Liability',
            'ledger_type': asyncql.LedgerType.PRESENT,
            'destination': 'Balance Sheet',
        }))

        # setup identity, currency, ledger, and some accounts
        identity = run(asyncql.Identity.insert({'name': 'Test Man'}))
        currency = run(asyncql.Currency.insert({
            'name': 'US Dollar',
            'prefix_symbol': '$',
            'fx_symbol': 'USD',
            'base': 100,
            'unit_divisions': 1,
        }))
        ledger: asyncql.Ledger = run(asyncql.Ledger.insert({
            'name': 'General Ledger',
            'identity_id': identity.id,
            'currency_id': currency.id,
            'type': asyncql.LedgerType.PRESENT,
        }))
        equity_acct = run(asyncql.Account.insert({
            'name': 'General Equity',
            'type': asyncql.AccountType.EQUITY,
            'ledger_id': ledger.id,
            'category_id': equity_acct_cat.id,
        }))
        asset_acct = run(asyncql.Account.insert({
            'name': 'General Asset',
            'type': asyncql.AccountType.ASSET,
            'ledger_id': ledger.id,
            'category_id': asset_acct_cat.id,
        }))
        liability_acct = run(asyncql.Account.insert({
            'name': 'General Liability',
            'type': asyncql.AccountType.LIABILITY,
            'ledger_id': ledger.id,
            'category_id': liability_acct_cat.id,
        }))

        # make sub account
        assert len(liability_acct.children) == 0
        liability_sub_acct = run(asyncql.Account.insert({
            'name': 'Liability Sub Account',
            'type': asyncql.AccountType.LIABILITY,
            'ledger_id': ledger.id,
            'parent_id': liability_acct.id,
        }))
        assert liability_sub_acct.parent is not None, liability_sub_acct.parent
        assert liability_sub_acct.parent.id == liability_acct.id, liability_sub_acct.parent
        run(liability_acct.children().reload())
        assert len(liability_acct.children) == 1
        assert liability_acct.children[0].id == liability_sub_acct.id

        assert equity_acct.category.id == equity_acct_cat.id
        assert asset_acct.category.id == asset_acct_cat.id
        assert liability_acct.category.id == liability_acct_cat.id

        assert len(liability_acct_cat.accounts) == 1, liability_acct_cat.accounts

        # make a vendor and a customer
        vendor = asyncql.Vendor({'name': 'Vendor-san', 'code': '1530'})
        vendor.details = {'some': 'thing'}
        run(vendor.save())
        customer = asyncql.Customer({'name': 'Customer-sama', 'code': '2300'})
        customer.details = {'number': 1234}
        run(customer.save())

        # prepare and save a valid transaction
        txn_nonce = os.urandom(16)
        equity_entry = asyncql.Entry({
            'type': asyncql.EntryType.CREDIT,
            'account_id': equity_acct.id,
            'amount': 10_000_00,
            'nonce': txn_nonce,
        })
        equity_entry.account = equity_acct
        asset_entry = asyncql.Entry({
            'type': asyncql.EntryType.DEBIT,
            'account_id': asset_acct.id,
            'amount': 10_000_00,
            'nonce': txn_nonce,
        })
        asset_entry.account = asset_acct
        txn = run(asyncql.Transaction.prepare(
            [equity_entry, asset_entry], str(time()),
            details='Starting capital asset'
        ))
        assert run(txn.validate())
        run(equity_entry.save())
        run(asset_entry.save())
        run(txn.save())
        # reload txn from database and validate it
        txn: asyncql.Transaction = run(asyncql.Transaction.find(txn.id))
        assert run(txn.validate(reload=True))
        assert len(asset_entry.transactions) == 1
        assert asset_entry.transactions[0].id == txn.id, asset_entry.transactions

        # check balances
        assert run(equity_acct.balance()) == 10_000_00, run(equity_acct.balance())
        assert run(asset_acct.balance()) == 10_000_00, [run(asset_acct.balance()), asset_acct.entries]
        assert run(liability_acct.balance()) == 0, run(liability_acct.balance())
        balances = run(ledger.balances(True))
        assert len(balances.keys()) == 4, balances
        assert balances[equity_acct.id][0] == 10_000_00, balances[equity_acct.id][0]
        assert balances[asset_acct.id][0] == 10_000_00, balances[asset_acct.id][0]
        assert balances[liability_acct.id][0] == 0, balances[liability_acct.id][0]
        assert balances[liability_sub_acct.id][0] == 0, balances[liability_sub_acct.id][0]

        # prepare and save valid transaction for liability sub account
        txn_nonce = os.urandom(16)
        equity_entry = run(asyncql.Entry.insert({
            'type': asyncql.EntryType.DEBIT,
            'account_id': equity_acct.id,
            'amount': 9_99,
            'nonce': txn_nonce,
        }))
        liability_entry = run(asyncql.Entry.insert({
            'type': asyncql.EntryType.CREDIT,
            'account_id': liability_sub_acct.id,
            'amount': 9_99,
            'nonce': txn_nonce,
        }))
        txn = run(asyncql.Transaction.prepare(
            [equity_entry, liability_entry],
            str(time()),
            {
                'vendor_id': vendor.id,
                'customer_id': customer.id,
            }
        ))
        assert run(txn.validate())
        run(txn.save())

        # check balances
        assert run(equity_acct.balance()) == 10_000_00-9_99, run(equity_acct.balance())
        assert run(asset_acct.balance()) == 10_000_00, run(asset_acct.balance())
        assert run(liability_sub_acct.balance()) == 9_99, run(liability_acct.balance())
        assert run(liability_acct.balance()) == 9_99, run(liability_acct.balance())
        assert run(liability_acct.balance(False)) == 0, run(liability_acct.balance(False))
        balances = run(ledger.balances(True))
        assert len(balances.keys()) == 4, balances
        assert balances[equity_acct.id][0] == 10_000_00-9_99, balances[equity_acct.id][0]
        assert balances[asset_acct.id][0] == 10_000_00, balances[asset_acct.id][0]
        assert balances[liability_acct.id][0] == 0, balances[liability_acct.id][0]
        assert balances[liability_sub_acct.id][0] == 9_99, balances[liability_sub_acct.id][0]

        # prepare invalid transaction: reused entries
        with self.assertRaises(ValueError) as e:
            txn = run(asyncql.Transaction.prepare([equity_entry, asset_entry], str(int(time()))))
        assert 'already contained within a Transaction' in str(e.exception)

        # prepare invalid transaction: unbalanced entries
        txn_nonce = os.urandom(16)
        equity_entry = asyncql.Entry({
            'type': asyncql.EntryType.CREDIT,
            'account_id': equity_acct.id,
            'amount': 10_00,
            'nonce': txn_nonce,
        })
        equity_entry.account = equity_acct
        asset_entry = asyncql.Entry({
            'type': asyncql.EntryType.DEBIT,
            'account_id': asset_acct.id,
            'amount': 10_01,
            'nonce': txn_nonce,
        })
        asset_entry.account = asset_acct
        with self.assertRaises(ValueError) as e:
            txn = run(asyncql.Transaction.prepare([equity_entry, asset_entry], str(int(time()))))
        assert 'unbalanced' in str(e.exception)


if __name__ == '__main__':
    unittest.main()
