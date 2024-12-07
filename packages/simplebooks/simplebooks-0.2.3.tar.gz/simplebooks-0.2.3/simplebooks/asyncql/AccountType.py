from enum import Enum


class AccountType(Enum):
    """Enum of valid Account types: DEBIT_BALANCE, ASSET, CONTRA_ASSET,
        CREDIT_BALANCE, LIABILITY, EQUITY, CONTRA_LIABILITY,
        CONTRA_EQUITY.
    """
    DEBIT_BALANCE = 'd'
    ASSET = 'a'
    CONTRA_ASSET = '-a'
    CREDIT_BALANCE = 'c'
    LIABILITY = 'l'
    EQUITY = 'e'
    CONTRA_LIABILITY = '-l'
    CONTRA_EQUITY = '-e'
