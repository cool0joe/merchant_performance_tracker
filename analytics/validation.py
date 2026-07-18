import sys

import pandas as pd

from config import (
    RAW_USERS_FILE,
    RAW_DATA_TRANSACTIONS_FILE,
)


# Prevent Windows terminals from failing when printing symbols and emojis.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# These names match the raw VTU database exports.
USER_REQUIRED_COLUMNS = [
    "id",
    "username",
    "FullName",
    "email",
    "Phone",
    "user_type",
    "date_joined",
    "Account_Balance",
]


DATA_TRANSACTION_REQUIRED_COLUMNS = [
    "id",
    "user_id",
    "data_type",
    "network_id",
    "plan_id",
    "plan_amount",
    "Status",
    "create_date",
]


def normalize_column_names(dataframe):
    """Remove accidental spaces around Excel column headers."""

    dataframe.columns = (
        dataframe.columns
        .astype(str)
        .str.strip()
    )

    return dataframe


def validate_columns(dataframe, required_columns, file_name):
    """Confirm that every required column exists."""

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        print(f"\n❌ {file_name} is missing these required columns:")

        for column in missing_columns:
            print(f"- {column}")

        return False

    print(f"✅ {file_name} has all required columns.")
    return True


def validate_no_blank_values(dataframe, column_name, file_name):
    """Check that an important column has no empty values."""

    if column_name not in dataframe.columns:
        print(
            f"\n❌ Cannot check '{column_name}' because it does not exist "
            f"in {file_name}."
        )
        return False

    # Detect both genuinely empty cells and text containing only spaces.
    blank_mask = (
        dataframe[column_name].isna()
        | dataframe[column_name]
        .astype(str)
        .str.strip()
        .eq("")
    )

    blank_rows = dataframe[blank_mask]

    if not blank_rows.empty:
        print(
            f"\n❌ {file_name} has blank values "
            f"in '{column_name}'."
        )

        # Excel row numbers begin at 2 because row 1 contains headers.
        print("Affected Excel rows:")

        for index in blank_rows.index:
            print(f"- Row {index + 2}")

        return False

    print(
        f"✅ {file_name} has no blank values "
        f"in '{column_name}'."
    )

    return True


def validate_numeric_column(dataframe, column_name, file_name):
    """Check that values in a column can be converted to numbers."""

    if column_name not in dataframe.columns:
        print(
            f"\n❌ Cannot validate '{column_name}' because it does not "
            f"exist in {file_name}."
        )
        return False

    converted_values = pd.to_numeric(
        dataframe[column_name],
        errors="coerce",
    )

    invalid_mask = converted_values.isna()
    invalid_rows = dataframe[invalid_mask]

    if not invalid_rows.empty:
        print(
            f"\n❌ {file_name} has invalid numeric values "
            f"in '{column_name}'."
        )

        print("Affected Excel rows:")

        for index in invalid_rows.index:
            print(f"- Row {index + 2}")

        return False

    print(
        f"✅ {file_name} has valid numeric values "
        f"in '{column_name}'."
    )

    return True


def validate_unique_ids(dataframe, column_name, file_name):
    """Check that identifier values are not duplicated."""

    if column_name not in dataframe.columns:
        print(
            f"\n❌ Cannot check duplicate IDs because '{column_name}' "
            f"does not exist in {file_name}."
        )
        return False

    duplicate_mask = dataframe[column_name].duplicated(
        keep=False
    )

    duplicate_rows = dataframe[duplicate_mask]

    if not duplicate_rows.empty:
        print(
            f"\n❌ {file_name} contains duplicate values "
            f"in '{column_name}'."
        )

        print(
            duplicate_rows[
                [column_name]
            ].to_string(index=False)
        )

        return False

    print(
        f"✅ {file_name} has unique values "
        f"in '{column_name}'."
    )

    return True


def validate_user_relationship(users, data_transactions):
    """
    Confirm that every transaction user_id matches an existing users.id.

    A transaction with no matching user is treated as a ghost transaction.
    """

    if "id" not in users.columns:
        print(
            "\n❌ Cannot validate relationships because users.xlsx "
            "has no 'id' column."
        )
        return False

    if "user_id" not in data_transactions.columns:
        print(
            "\n❌ Cannot validate relationships because "
            "data_transactions.xlsx has no 'user_id' column."
        )
        return False

    valid_user_ids = set(
        pd.to_numeric(
            users["id"],
            errors="coerce",
        ).dropna()
    )

    transaction_user_ids = set(
        pd.to_numeric(
            data_transactions["user_id"],
            errors="coerce",
        ).dropna()
    )

    missing_user_ids = transaction_user_ids - valid_user_ids

    if missing_user_ids:
        print(
            "\n❌ Ghost transactions detected."
        )

        print(
            "These transaction user_id values do not exist "
            "in users.xlsx:"
        )

        for user_id in sorted(missing_user_ids):
            print(f"- Missing user_id: {int(user_id)}")

        return False

    print(
        "✅ Every transaction user_id matches an existing user."
    )

    return True


def run_validation():
    """Run all raw-upload validation checks."""

    print("\n===== VALIDATION REPORT =====")

    try:
        users = pd.read_excel(RAW_USERS_FILE)
        data_transactions = pd.read_excel(
            RAW_DATA_TRANSACTIONS_FILE
        )

    except FileNotFoundError as error:
        print("\n❌ One or more input files could not be found.")
        print(error)
        return False

    except Exception as error:
        print("\n❌ The uploaded Excel files could not be read.")
        print(error)
        return False

    users = normalize_column_names(users)
    data_transactions = normalize_column_names(
        data_transactions
    )

    users_columns_ok = validate_columns(
        users,
        USER_REQUIRED_COLUMNS,
        "users.xlsx",
    )

    transactions_columns_ok = validate_columns(
        data_transactions,
        DATA_TRANSACTION_REQUIRED_COLUMNS,
        "data_transactions.xlsx",
    )

    # Only perform field-level checks when the required columns exist.
    if users_columns_ok:
        username_ok = validate_no_blank_values(
            users,
            "username",
            "users.xlsx",
        )

        users_id_numeric_ok = validate_numeric_column(
            users,
            "id",
            "users.xlsx",
        )

        users_id_unique_ok = validate_unique_ids(
            users,
            "id",
            "users.xlsx",
        )

    else:
        username_ok = False
        users_id_numeric_ok = False
        users_id_unique_ok = False

    if transactions_columns_ok:
        user_id_ok = validate_no_blank_values(
            data_transactions,
            "user_id",
            "data_transactions.xlsx",
        )

        transaction_id_ok = validate_no_blank_values(
            data_transactions,
            "id",
            "data_transactions.xlsx",
        )

        plan_amount_blank_ok = validate_no_blank_values(
            data_transactions,
            "plan_amount",
            "data_transactions.xlsx",
        )

        user_id_numeric_ok = validate_numeric_column(
            data_transactions,
            "user_id",
            "data_transactions.xlsx",
        )

        plan_amount_numeric_ok = validate_numeric_column(
            data_transactions,
            "plan_amount",
            "data_transactions.xlsx",
        )

        transaction_id_unique_ok = validate_unique_ids(
            data_transactions,
            "id",
            "data_transactions.xlsx",
        )

    else:
        user_id_ok = False
        transaction_id_ok = False
        plan_amount_blank_ok = False
        user_id_numeric_ok = False
        plan_amount_numeric_ok = False
        transaction_id_unique_ok = False

    if users_columns_ok and transactions_columns_ok:
        relationship_ok = validate_user_relationship(
            users,
            data_transactions,
        )
    else:
        relationship_ok = False

    validation_passed = all(
        [
            users_columns_ok,
            transactions_columns_ok,
            username_ok,
            users_id_numeric_ok,
            users_id_unique_ok,
            user_id_ok,
            transaction_id_ok,
            plan_amount_blank_ok,
            user_id_numeric_ok,
            plan_amount_numeric_ok,
            transaction_id_unique_ok,
            relationship_ok,
        ]
    )

    if validation_passed:
        print(
            "\n🎉 Validation passed. "
            "The raw files are ready for transformation."
        )
    else:
        print(
            "\n⚠️ Validation failed. "
            "Correct the reported issues before transformation."
        )

    return validation_passed


if __name__ == "__main__":
    run_validation()