from __future__ import annotations
from .Account import Account, AccountType
from .Ledger import Ledger
from sqloquent.asyncql import AsyncSqlModel, AsyncRelatedCollection


class Identity(AsyncSqlModel):
    connection_info: str = ''
    table: str = 'identities'
    id_column: str = 'id'
    columns: tuple[str] = ('id', 'name', 'details', 'pubkey', 'seed', 'secret_details')
    columns_excluded_from_hash: tuple[str] = ('seed', 'secret_details')
    id: str
    name: str
    details: bytes
    pubkey: bytes|None
    seed: bytes|None
    secret_details: bytes|None
    ledgers: AsyncRelatedCollection

    def public(self) -> dict:
        """Return the public data for cloning the Identity."""
        return {
            k:v for k,v in self.data.items()
            if k not in self.columns_excluded_from_hash
        }
