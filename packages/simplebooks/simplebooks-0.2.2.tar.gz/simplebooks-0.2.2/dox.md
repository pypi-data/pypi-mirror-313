# simplebooks

## Classes

### `Account(SqlModel)`

#### Annotations

- table: str
- id_column: str
- columns: tuple[str]
- id: str
- name: str
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: str
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- type: str
- ledger_id: str
- parent_id: str
- code: str | None
- category_id: str | None
- details: bytes | None
- active: bool | Default[True]
- ledger: RelatedModel
- parent: RelatedModel
- category: RelatedModel
- children: RelatedCollection
- entries: RelatedCollection

#### Properties

- type: The AccountType of the Account.
- details: A packify.SerializableType stored in the database as a blob.
- ledger: The related Ledger. Setting raises TypeError if the precondition check
fails.
- children: The related Accounts. Setting raises TypeError if the precondition
check fails.
- parent: The related Account. Setting raises TypeError if the precondition
check fails.
- category: The related AccountCategory. Setting raises TypeError if the
precondition check fails.
- entries: The related Entrys. Setting raises TypeError if the precondition
check fails.

#### Methods

##### `@classmethod insert(data: dict) -> Account | None:`

Ensure data is encoded before inserting.

##### `@classmethod insert_many(items: list[dict], /, *, suppress_events: bool = False) -> int:`

Ensure items are encoded before inserting.

##### `update(updates: dict, /, *, suppress_events: bool = False) -> Account:`

Ensure updates are encoded before updating.

##### `@classmethod query(conditions: dict = None, connection_info: str = None) -> QueryBuilderProtocol:`

Ensure conditions are encoded before querying.

##### `balance(include_sub_accounts: bool = True) -> int:`

Tally all entries for this account. Includes the balances of all sub-accounts if
include_sub_accounts is True.

### `AccountCategory(SqlModel)`

#### Annotations

- table: str
- id_column: str
- columns: tuple[str]
- id: str
- name: str
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: str
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- ledger_type: str | None
- destination: str
- accounts: RelatedCollection

#### Properties

- ledger_type: The LedgerType that this AccountCategory applies to, if any.
- accounts: The related Accounts. Setting raises TypeError if the precondition
check fails.

#### Methods

##### `@classmethod insert(data: dict, /, *, suppress_events: bool = False) -> AccountCategory | None:`

Ensure data is encoded before inserting.

##### `@classmethod insert_many(items: list[dict], /, *, suppress_events: bool = False) -> int:`

Ensure items are encoded before inserting.

##### `update(updates: dict, /, *, suppress_events: bool = False) -> AccountCategory:`

Ensure updates are encoded before updating.

##### `@classmethod query(conditions: dict = None, connection_info: str = None) -> QueryBuilderProtocol:`

Ensure conditions are encoded before querying.

### `AccountType(Enum)`

Enum of valid Account types: DEBIT_BALANCE, ASSET, CONTRA_ASSET, CREDIT_BALANCE,
LIABILITY, EQUITY, CONTRA_LIABILITY, CONTRA_EQUITY.

### `Currency(SqlModel)`

#### Annotations

- table: <class 'str'>
- id_column: <class 'str'>
- columns: tuple[str]
- id: <class 'str'>
- name: <class 'str'>
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: <class 'str'>
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- prefix_symbol: str | None
- postfix_symbol: str | None
- fx_symbol: str | None
- unit_divisions: <class 'int'>
- base: int | None
- details: str | None

#### Methods

##### `to_decimal(amount: int) -> Decimal:`

Convert the amount into a Decimal representation.

##### `get_units(amount: int) -> tuple[int]:`

Get the full units and subunits. The number of subunit figures will be equal to
unit_divisions; e.g. if base=10 and unit_divisions=2, get_units(200) will return
(2, 0, 0); if base=60 and unit_divisions=2, get_units(200) will return (0, 3,
20).

##### `format(amount: int, /, *, use_fx_symbol: bool = False, use_postfix: bool = False, use_prefix: bool = True, decimal_places: int = 2) -> str:`

Format an amount using the correct number of decimal_places.

### `Customer(SqlModel)`

#### Annotations

- table: <class 'str'>
- id_column: <class 'str'>
- columns: tuple[str]
- id: <class 'str'>
- name: <class 'str'>
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: <class 'str'>
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- code: str | None
- details: str | None

#### Properties

- details: A packify.SerializableType stored in the database as a blob.

### `Entry(SqlModel)`

#### Annotations

- table: str
- id_column: str
- columns: tuple[str]
- id: str
- name: str
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: str
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- type: str
- amount: int
- nonce: bytes
- account_id: str
- details: bytes
- account: RelatedModel
- transactions: RelatedCollection

#### Properties

- type: The EntryType of the Entry.
- details: A packify.SerializableType stored in the database as a blob.
- account: The related Account. Setting raises TypeError if the precondition
check fails.
- transactions: The related Transactions. Setting raises TypeError if the
precondition check fails.

#### Methods

##### `__hash__() -> int:`

##### `@classmethod insert(data: dict) -> Entry | None:`

Ensure data is encoded before inserting.

##### `@classmethod insert_many(items: list[dict]) -> int:`

Ensure data is encoded before inserting.

##### `@classmethod query(conditions: dict = None) -> QueryBuilderProtocol:`

Ensure conditions are encoded properly before querying.

### `EntryType(Enum)`

Enum of valid Entry types: CREDIT and DEBIT.

### `Identity(SqlModel)`

#### Annotations

- table: str
- id_column: str
- columns: tuple[str]
- id: str
- name: str
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: str
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- columns_excluded_from_hash: tuple[str]
- details: bytes
- pubkey: bytes | None
- seed: bytes | None
- secret_details: bytes | None
- ledgers: RelatedCollection

#### Properties

- ledgers: The related Ledgers. Setting raises TypeError if the precondition
check fails.

#### Methods

##### `public() -> dict:`

Return the public data for cloning the Identity.

### `Ledger(SqlModel)`

#### Annotations

- table: str
- id_column: str
- columns: tuple[str]
- id: str
- name: str
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: str
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- type: str
- identity_id: str
- currency_id: str
- owner: RelatedModel
- currency: RelatedModel
- accounts: RelatedCollection
- transactions: RelatedCollection

#### Properties

- type: The LedgerType of the Ledger.
- owner: The related Identity. Setting raises TypeError if the precondition
check fails.
- currency: The related Currency. Setting raises TypeError if the precondition
check fails.
- accounts: The related Accounts. Setting raises TypeError if the precondition
check fails.
- transactions: The related Transactions. Setting raises TypeError if the
precondition check fails.

#### Methods

##### `balances(reload: bool = False) -> dict[str, tuple[int, AccountType]]:`

Return a dict mapping account ids to their balances. Accounts with sub-accounts
will not include the sub-account balances; the sub-account balances will be
returned separately.

##### `@classmethod insert(data: dict) -> Ledger | None:`

Ensure data is encoded before inserting.

##### `@classmethod insert_many(items: list[dict], /, *, suppress_events: bool = False) -> int:`

Ensure items are encoded before inserting.

##### `update(updates: dict, /, *, suppress_events: bool = False) -> Ledger:`

Ensure updates are encoded before updating.

##### `@classmethod query(conditions: dict = None, connection_info: str = None) -> QueryBuilderProtocol:`

Ensure conditions are encoded before querying.

##### `setup_basic_accounts() -> list[Account]:`

Creates and returns a list of 3 unsaved Accounts covering the 3 basic
categories: Asset, Liability, Equity.

### `LedgerType(Enum)`

Enum of valid ledger types: PRESENT and FUTURE for cash and accrual accounting,
respectively.

### `Transaction(SqlModel)`

#### Annotations

- table: str
- id_column: str
- columns: tuple[str]
- id: str
- name: str
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: str
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- entry_ids: str
- ledger_ids: str
- timestamp: str
- details: bytes
- entries: RelatedCollection
- ledgers: RelatedCollection

#### Properties

- details: A packify.SerializableType stored in the database as a blob.
- entries: The related Entrys. Setting raises TypeError if the precondition
check fails.
- ledgers: The related Ledgers. Setting raises TypeError if the precondition
check fails.

#### Methods

##### `@classmethod prepare(entries: list[Entry], timestamp: str, details: packify.SerializableType = None, reload: bool = False) -> Transaction:`

Prepare a transaction. Raises TypeError for invalid arguments. Raises ValueError
if the entries do not balance for each ledger; if a required auth script is
missing; or if any of the entries is contained within an existing Transaction.
Entries and Transaction will have IDs generated but will not be persisted to the
database and must be saved separately.

##### `validate(reload: bool = False) -> bool:`

Determines if a Transaction is valid using the rules of accounting. Raises
TypeError for invalid arguments. Raises ValueError if the entries do not balance
for each ledger; or if any of the entries is contained within an existing
Transaction. If reload is set to True, entries and accounts will be reloaded
from the database.

##### `save(reload: bool = False) -> Transaction:`

Validate the transaction, save the entries, then save the transaction.

### `Vendor(SqlModel)`

#### Annotations

- table: <class 'str'>
- id_column: <class 'str'>
- columns: tuple[str]
- id: <class 'str'>
- name: <class 'str'>
- query_builder_class: Type[QueryBuilderProtocol]
- connection_info: <class 'str'>
- data: dict
- data_original: MappingProxyType
- _event_hooks: dict[str, list[Callable]]
- code: str | None
- details: str | None

#### Properties

- details: A packify.SerializableType stored in the database as a blob.

## Functions

### `set_connection_info(db_file_path: str):`

Set the connection info for all models to use the specified sqlite3 database
file path.

### `get_migrations() -> dict[str, str]:`

Returns a dict mapping model names to migration file content strs.

### `publish_migrations(migration_folder_path: str, migration_callback: Callable = None):`

Writes migration files for the models. If a migration callback is provided, it
will be used to modify the migration file contents. The migration callback will
be called with the model name and the migration file contents, and whatever it
returns will be used as the migration file contents.

### `automigrate(migration_folder_path: str, db_file_path: str):`

Executes the sqloquent automigrate tool.

## Values

- `__version__`: str
