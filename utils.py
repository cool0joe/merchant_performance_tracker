import pandas as pd

from config import (
    CLEAN_USERS_FILE,
    CLEAN_DATA_TRANSACTIONS_FILE,
    CURRENCY_SYMBOL,
)


def load_clean_data():
    """Load the transformed users and transaction datasets."""

    users = pd.read_excel(CLEAN_USERS_FILE)
    transactions = pd.read_excel(CLEAN_DATA_TRANSACTIONS_FILE)

    return users, transactions


def merge_users_and_transactions(users, transactions):
    """Attach merchant details to each transaction using user_id."""

    return transactions.merge(
        users,
        left_on="user_id",
        right_on="id",
        how="left",
        suffixes=("_transaction", "_user"),
    )


def format_currency(amount):
    """Return a number formatted as Nigerian currency."""

    return f"{CURRENCY_SYMBOL}{amount:,.2f}"

