from __future__ import annotations
from sqloquent.asyncql import (
    AsyncSqlModel, AsyncRelatedModel, AsyncRelatedCollection,
    AsyncQueryBuilderProtocol, Default,
)
from .AccountType import AccountType
from .Entry import Entry
from .EntryType import EntryType
import packify


class Account(AsyncSqlModel):
    connection_info: str = ''
    table: str = 'accounts'
    id_column: str = 'id'
    columns: tuple[str] = (
        'id', 'name', 'type', 'ledger_id', 'parent_id', 'code',
        'category_id', 'details', 'active'
    )
    id: str
    name: str
    type: str
    ledger_id: str
    parent_id: str
    code: str|None
    category_id: str|None
    details: bytes|None
    active: bool|Default[True]
    ledger: AsyncRelatedModel
    parent: AsyncRelatedModel
    category: AsyncRelatedModel
    children: AsyncRelatedCollection
    entries: AsyncRelatedCollection

    # override automatic property
    @property
    def type(self) -> AccountType:
        """The AccountType of the Account."""
        return AccountType(self.data['type'])
    @type.setter
    def type(self, val: AccountType):
        if type(val) is AccountType:
            self.data['type'] = val.value

    # override automatic property
    @property
    def details(self) -> packify.SerializableType:
        """A packify.SerializableType stored in the database as a blob."""
        return packify.unpack(self.data.get('details', None) or b'n\x00\x00\x00\x00')
    @details.setter
    def details(self, val: packify.SerializableType):
        if isinstance(val, packify.SerializableType):
            self.data['details'] = packify.pack(val)

    @staticmethod
    def _encode(data: dict|None) -> dict|None:
        """Encode Account data without modifying the original dict."""
        if type(data) is not dict:
            return data
        data = {**data}
        if type(data.get('type', None)) is AccountType:
            data['type'] = data['type'].value
        return data

    @classmethod
    async def insert(cls, data: dict) -> Account | None:
        """Ensure data is encoded before inserting."""
        result = await super().insert(cls._encode(data))
        return result

    @classmethod
    async def insert_many(cls, items: list[dict], /, *, suppress_events: bool = False) -> int:
        """Ensure items are encoded before inserting."""
        items = [cls._encode(item) for item in items]
        return await super().insert_many(items, suppress_events=suppress_events)

    async def update(self, updates: dict, /, *, suppress_events: bool = False) -> Account:
        """Ensure updates are encoded before updating."""
        updates = self._encode(updates)
        return await super().update(updates, suppress_events=suppress_events)

    @classmethod
    def query(cls, conditions: dict = None, connection_info: str = None) -> AsyncQueryBuilderProtocol:
        """Ensure conditions are encoded before querying."""
        if conditions and type(conditions.get('type', None)) is AccountType:
            conditions['type'] = conditions['type'].value
        return super().query(conditions, connection_info)

    async def balance(self, include_sub_accounts: bool = True) -> int:
        """Tally all entries for this account. Includes the balances of
            all sub-accounts if include_sub_accounts is True.
        """
        totals = {
            EntryType.CREDIT: 0,
            EntryType.DEBIT: 0,
            'subaccounts': 0,
        }
        async for entries in self.entries().query().chunk(500):
            entry: Entry
            for entry in entries:
                totals[entry.type] += entry.amount

        if include_sub_accounts:
            for acct in self.children:
                acct: Account
                totals['subaccounts'] += await acct.balance(include_sub_accounts=True)

        if self.type in (
            AccountType.ASSET, AccountType.DEBIT_BALANCE,
            AccountType.CONTRA_LIABILITY, AccountType.CONTRA_EQUITY,
        ):
            return totals[EntryType.DEBIT] - totals[EntryType.CREDIT] + totals['subaccounts']

        return totals[EntryType.CREDIT] - totals[EntryType.DEBIT] + totals['subaccounts']
