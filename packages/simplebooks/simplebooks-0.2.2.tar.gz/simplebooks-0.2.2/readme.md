# SimpleBooks

SimpleBooks is a simple accounting library that uses
[sqloquent](https://pypi.org/project/sqloquent) to persist data for identities,
ledgers, accounts, transactions, and entries. Included are tools for
accomplishing basic bookkeeping tasks. The basic accounting formula is this:
`Assets = Liabilities + Equity`. Assets are debit-balance; liabilities and
equity are credit-balance. Every transaction must have entries that have no net
difference between the amount of credits and the amount of debits.

This is a simplification of [bookchain](https://pypi.org/project/bookchain): all
cryptographic features have been removed. This may be useful in scenarios when
cryptographic features cannot be supported.

## Status

All initially planned features have been implemented and tested.

Open issues can be found [here](https://github.com/k98kurz/simplebooks/issues).

The async implementation has an upstream issue from the sqloquent dependency
that can be tracked [here](https://github.com/k98kurz/sqloquent/issues/16). Once
that is fixed, the dependency will be updated, and this notice will be removed.

## Overview

This library provides an accounting system using sqloquent for persistence,
packify for deterministic encoding, and the classic rules of double-entry
bookkeeping. The `Transaction.prepare` and `Transaction.validate` ensure that
the accounting rule is followed.

### Class organization

`Currency` represents a currency/unit of account for a `Ledger`. It includes the
number of subunits to track and optionally the base for conversion to decimal
(defaults to 10), FX symbol, prefix symbol, and/or postfix symbol to be used with
the `format` method (e.g. `USD.format(1200)` could result in "12.00 USD",
"$12.00", or "12.00$", respectively). It also includes `to_decimal` method for
formatting int amounts into `Decimal`s, and `get_units` method for getting a
tuple of whole units and remainders.

`Identity` represents a legal person or other entity that can sign contracts
or engage in transactions. It includes the name, details, and optionally public
key bytes and private key seed bytes.

`Ledger` represents a general ledger for a given `Identity` using a specific
`Currency`. It includes a name, a `LedgerType`, the `Identity` id, and the
`Currency` id. `LedgerType` is an enum representing the valid ledger types,
either `PRESENT` or `FUTURE` for cash and accrual accounting, respectively, or
for other uses the package user may define.

`Account` represents an account for a given `Ledger`. It includes a name, a type
(one of the `AccountType` enum options), the `Ledger` id, an optional locking
script for access control, and optional details.

`AccountCategory` represents a category for `Account`s. It includes a name, a
`LedgerType`, and a destination (str description; e.g. "Balance Sheet" or
"Profit and Loss").

`AccountType` is an enum representing the valid account types. The options are
`DEBIT_BALANCE`, `ASSET`, `CONTRA_ASSET`, `CREDIT_BALANCE`, `LIABILITY`,
`EQUITY`, `CONTRA_LIABILITY`, and `CONTRA_EQUITY`.

`Entry` represents an entry in the general ledger for a given `Account`. It
includes a type (one of the `EntryType` enum options), an amount, a nonce, the
`Account` id, and optional details.

`EntryType` is an enum representing the valid entry types. The options are
CREDIT and DEBIT.

`Transaction` represents a transaction made of `Entry`s. It includes the `Entry`
ids, `Ledger` ids, a timestamp, and the details. Each `Transaction` must include
entries that balance the number of credits and debits applied to each ledger
affected by the transaction. Use `Transaction.prepare` to prepare a transaction
-- it will raise validation errors if the transaction is not valid -- then call
`.save()` on the result to persist it to the database. Transactions in the
database can be validated by using `.validate()`, which will return `True` if it
is valid and `False` if it is not (it will also raise errors in some situations
that require more information about the validation failure).

`Customer` and `Vendor` are provided in case they are useful in some way, but no
relations are set up for them currently. This is likely to change in a future
release.

- `Identity` has many `Ledger`s
- `Ledger` belongs to `Identity` and `Currency`, has many `Account`s, and is within `Transaction`s
- `Account` belongs to `Ledger` and `AccountCategory`, and has many `Entry`s
- `AccountCategory` has many `Account`s
- `Entry` belongs to `Account` and is within `Transaction`s
- `Transaction` contains `Ledger`s and `Entry`s

## Installation and Setup

Install with `pip install simplebooks`. If you want to use the async version,
instead install with `pip install simplebooks[asyncql]`.

Once installed, use the following to setup your project as appropriate:

```python
import simplebooks

simplebooks.publish_migrations(path_to_migrations_folder)
simplebooks.automigrate(path_to_migrations_folder, db_file_path)
simplebooks.set_connection_info(db_file_path)
```

To use the async version:

```python
import simplebooks
import simplebooks.asyncql

simplebooks.publish_migrations(path_to_migrations_folder)
simplebooks.automigrate(path_to_migrations_folder, db_file_path)
simplebooks.asyncql.set_connection_info(db_file_path)
```

The `simplebooks.publish_migrations` function can be passed a callback that
takes the str model name and str migration file contents, and returns the
modified str migration file contents. This can be used to modify the migration
file contents before they are written to disk. For example, if you wanted to
modify the `Account` migration file to add a unique constraint to the `name`
column, you could do the following:

```python
def migration_callback(name: str, m: str) -> str:
    if name == 'Account':
        return m.replace("t.text('name').index()", "t.text('name').unique()")
    return m

simplebooks.publish_migrations(path_to_migrations_folder, migration_callback)
```

## More Resources

Documentation generated by [autodox](https://pypi.org/project/autodox) can be
found [here](https://github.com/k98kurz/simplebooks/blob/v0.2.1/dox.md). Docs for
the async version can be found
[here](https://github.com/k98kurz/simplebooks/blob/v0.2.1/asyncql_dox.md).

Check out the [Pycelium discord server](https://discord.gg/b2QFEJDX69). If you
experience a problem, please discuss it on the Discord server. All suggestions
for improvement are also welcome, and the best place for that is also Discord.
If you experience a bug and do not use Discord, open an issue on Github.

## Tests

There are a total of 7 tests (2 e2e tests and 5 tests for miscellaneous
tools/features). To run them, clone the repo, set up a virtual environment
(e.g. `python -m venv venv && source venv/bin/activate`), install the
dependencies with `pip install -r requirements.txt`, and then run the following:
`find tests -name test_*.py -print -exec python {} \;`. On Windows, the 3 test
files will have to be individually run with the following:

```bash
python tests/test_async_basic_e2e.py
python tests/test_basic_e2e.py
python tests/test_misc.py
```

## Personal, Non-commercial Use License

Copyright (c) 2024 Jonathan Voss (k98kurz)

Permission to use, copy, modify, and/or distribute this software
for any personal, non-commercial purpose is hereby granted, provided
that the above copyright notice and this permission notice appear in
all copies. For other uses, contact the software author.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
