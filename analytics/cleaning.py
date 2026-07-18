import sys

import pandas as pd

from config import (
    RAW_USERS_FILE,
    RAW_DATA_TRANSACTIONS_FILE,
    CLEAN_USERS_FILE,
    CLEAN_DATA_TRANSACTIONS_FILE,
)


# Prevent some Windows terminals from failing on emoji or the naira symbol.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


USER_RENAME_MAP = {
    "Phone": "phone",
    "Account_Balance": "account_balance",
    "FullName": "full_name",
}


DATA_RENAME_MAP = {
    "Status": "status",
}


USER_REQUIRED_COLUMNS = [
    "id",
    "username",
    "first_name",
    "last_name",
    "full_name",
    "email",
    "phone",
    "user_type",
    "date_joined",
    "account_balance",
]


DATA_TRANSACTION_REQUIRED_COLUMNS = [
    "id",
    "user_id",
    "data_type",
    "network_id",
    "plan_id",
    "plan_amount",
    "status",
    "create_date",
]


def normalize_column_names(dataframe):
    """Remove unwanted spaces from uploaded Excel column names."""

    dataframe.columns = (
        dataframe.columns
        .astype(str)
        .str.strip()
    )

    return dataframe


def apply_rename_map(dataframe, rename_map):
    """Rename production database columns to analytics-friendly names."""

    return dataframe.rename(columns=rename_map)


def keep_required_columns(dataframe, required_columns, file_name):
    """Keep only required columns and stop if any required field is missing."""

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{file_name} is missing required columns: {missing_columns}"
        )

    return dataframe[required_columns].copy()


def clean_text_column(dataframe, column_name):
    """Remove spaces around text values."""

    if column_name in dataframe.columns:
        dataframe[column_name] = (
            dataframe[column_name]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    return dataframe


def clean_numeric_column(dataframe, column_name):
    """Convert a column to numeric values."""

    if column_name in dataframe.columns:
        dataframe[column_name] = pd.to_numeric(
            dataframe[column_name],
            errors="coerce",
        ).fillna(0)

    return dataframe


def clean_date_column(dataframe, column_name):
    """
    Convert either Excel serial dates or normal date strings
    into Pandas datetime values.
    """

    if column_name not in dataframe.columns:
        return dataframe

    original_values = dataframe[column_name]

    numeric_values = pd.to_numeric(
        original_values,
        errors="coerce",
    )

    numeric_date_mask = numeric_values.notna()

    converted_dates = pd.Series(
        pd.NaT,
        index=dataframe.index,
        dtype="datetime64[ns]",
    )

    if numeric_date_mask.any():
        converted_dates.loc[numeric_date_mask] = pd.to_datetime(
            numeric_values.loc[numeric_date_mask],
            errors="coerce",
            unit="D",
            origin="1899-12-30",
        )

    text_date_mask = ~numeric_date_mask

    if text_date_mask.any():
        converted_dates.loc[text_date_mask] = pd.to_datetime(
            original_values.loc[text_date_mask],
            errors="coerce",
        )

    dataframe[column_name] = converted_dates

    return dataframe


def clean_users():
    """Transform the raw VTU users export."""

    users = pd.read_excel(RAW_USERS_FILE)

    users = normalize_column_names(users)
    users = apply_rename_map(users, USER_RENAME_MAP)

    users_clean = keep_required_columns(
        users,
        USER_REQUIRED_COLUMNS,
        "users.xlsx",
    )

    text_columns = [
        "username",
        "first_name",
        "last_name",
        "full_name",
        "email",
        "phone",
        "user_type",
    ]

    for column in text_columns:
        users_clean = clean_text_column(
            users_clean,
            column,
        )

    users_clean = clean_numeric_column(
        users_clean,
        "id",
    )

    users_clean = clean_numeric_column(
        users_clean,
        "account_balance",
    )

    users_clean = clean_date_column(
        users_clean,
        "date_joined",
    )

    users_clean["date_joined"] = (
        users_clean["date_joined"]
        .dt.strftime("%Y-%m")
        .fillna("unknown")
    )

    users_clean.to_excel(
        CLEAN_USERS_FILE,
        index=False,
    )

    return users_clean


def clean_data_transactions():
    """Transform the raw VTU data transaction export."""

    data_transactions = pd.read_excel(
        RAW_DATA_TRANSACTIONS_FILE
    )

    data_transactions = normalize_column_names(
        data_transactions
    )

    data_transactions = apply_rename_map(
        data_transactions,
        DATA_RENAME_MAP,
    )

    transactions_clean = keep_required_columns(
        data_transactions,
        DATA_TRANSACTION_REQUIRED_COLUMNS,
        "data_transactions.xlsx",
    )

    for column in ["data_type", "status"]:
        transactions_clean = clean_text_column(
            transactions_clean,
            column,
        )

    numeric_columns = [
        "id",
        "user_id",
        "network_id",
        "plan_id",
        "plan_amount",
    ]

    for column in numeric_columns:
        transactions_clean = clean_numeric_column(
            transactions_clean,
            column,
        )

    transactions_clean = clean_date_column(
        transactions_clean,
        "create_date",
    )

    transactions_clean.to_excel(
        CLEAN_DATA_TRANSACTIONS_FILE,
        index=False,
    )

    return transactions_clean


def run_cleaning():
    """Run the complete transformation process."""

    print("\n===== TRANSFORMATION / CLEANING REPORT =====")

    users_clean = clean_users()
    transactions_clean = clean_data_transactions()

    print("\n✅ users.xlsx cleaned successfully.")
    print(f"Output: {CLEAN_USERS_FILE}")
    print("Columns kept:")
    print(users_clean.columns.tolist())

    print("\n✅ data_transactions.xlsx cleaned successfully.")
    print(f"Output: {CLEAN_DATA_TRANSACTIONS_FILE}")
    print("Columns kept:")
    print(transactions_clean.columns.tolist())

    print(
        "\n🎉 Transformation complete. "
        "Clean files are ready for analytics."
    )


if __name__ == "__main__":
    run_cleaning()