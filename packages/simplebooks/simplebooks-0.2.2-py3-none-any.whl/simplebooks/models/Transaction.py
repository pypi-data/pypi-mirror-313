from __future__ import annotations
from hashlib import sha256
from sqloquent import SqlModel, RelatedCollection
from sqloquent.errors import vert, tert
from .Account import Account, AccountType
from .Entry import Entry, EntryType
from .Identity import Identity
import packify


class Transaction(SqlModel):
    connection_info: str = ''
    table: str = 'transactions'
    id_column: str = 'id'
    columns: tuple[str] = ('id', 'entry_ids', 'ledger_ids', 'timestamp', 'details')
    id: str
    entry_ids: str
    ledger_ids: str
    timestamp: str
    details: bytes
    entries: RelatedCollection
    ledgers: RelatedCollection

    # override automatic properties
    @property
    def details(self) -> dict[str, bytes]:
        """A packify.SerializableType stored in the database as a blob."""
        return packify.unpack(self.data.get('details', b'd\x00\x00\x00\x00'))
    @details.setter
    def details(self, val: dict[str, bytes]):
        if type(val) is not dict:
            return
        if not all([type(k) is str and type(v) is bytes for k, v in val.items()]):
            return
        self.data['details'] = packify.pack(val)

    @classmethod
    def _encode(cls, data: dict|None) -> dict|None:
        """Encode values for saving."""
        if type(data) is not dict:
            return None
        if type(data.get('details', {})) is dict:
            data['details'] = packify.pack(data.get('details', {}))
        return data

    @classmethod
    def prepare(cls, entries: list[Entry], timestamp: str,
                details: packify.SerializableType = None,
                reload: bool = False) -> Transaction:
        """Prepare a transaction. Raises TypeError for invalid arguments.
            Raises ValueError if the entries do not balance for each
            ledger; if a required auth script is missing; or if any of
            the entries is contained within an existing Transaction.
            Entries and Transaction will have IDs generated but will not
            be persisted to the database and must be saved separately.
        """
        tert(type(entries) is list and all([type(e) is Entry for e in entries]),
            'entries must be list[Entry]')
        tert(type(timestamp) is str, 'timestamp must be str')

        ledgers = set()
        for entry in entries:
            entry.id = entry.id if entry.id else entry.generate_id()
            if reload:
                entry.account().reload()
            vert(Transaction.query().contains('entry_ids', entry.id).count() == 0,
                 f"entry {entry.id} is already contained within a Transaction")
            ledgers.add(entry.account.ledger_id)

        txn = cls({
            'entry_ids': ",".join(sorted([
                e.id if e.id else e.generate_id()
                for e in entries
            ])),
            'ledger_ids': ",".join(sorted(list(ledgers))),
            'timestamp': timestamp,
        })
        txn.details = details
        txn.entries = entries
        assert txn.validate(reload), \
            'transaction validation failed'
        txn.id = txn.generate_id()
        return txn

    def validate(self, reload: bool = False) -> bool:
        """Determines if a Transaction is valid using the rules of accounting.
            Raises TypeError for invalid arguments. Raises ValueError if the
            entries do not balance for each ledger; or if any of the entries is
            contained within an existing Transaction. If reload is set to True,
            entries and accounts will be reloaded from the database.
        """
        if reload:
            self.entries().reload()

        # first check that all ledgers balance
        ledgers = {}
        entry: Entry
        for entry in self.entries:
            if reload:
                entry.account().reload()
            if entry.account.ledger_id not in ledgers:
                ledgers[entry.account.ledger_id] = {'Dr': 0, 'Cr': 0}
            if entry.type in (EntryType.CREDIT, EntryType.CREDIT.value):
                ledgers[entry.account.ledger_id]['Cr'] += entry.amount
            else:
                ledgers[entry.account.ledger_id]['Dr'] += entry.amount

        for ledger_id, balances in ledgers.items():
            vert(balances['Cr'] == balances['Dr'],
                f"ledger {ledger_id} unbalanced: {balances['Cr']} Cr != {balances['Dr']} Dr")

        return True

    def save(self, reload: bool = False) -> Transaction:
        """Validate the transaction, save the entries, then save the
            transaction.
        """
        assert self.validate(reload), 'cannot save an invalid Transaction'
        for e in self.entries:
            e.save()
        return super().save()
