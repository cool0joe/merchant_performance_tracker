import pandas as pd

from config import (
    RANKING_REPORT_FILE,
    TOP_MERCHANT_LIMIT,
)

from utils import (
    load_clean_data,
    merge_users_and_transactions,
    format_currency,
)


def calculate_merchant_summary(merged_data):
    """
    Create one performance summary row for each merchant.
    """

    merchant_summary = (
        merged_data
        .groupby(
            [
                "user_id",
                "username",
                "full_name",
                "user_type",
            ],
            dropna=False,
        )
        .agg(
            total_revenue=("plan_amount", "sum"),
            transaction_count=("id_transaction", "count"),
            average_transaction=("plan_amount", "mean"),
            highest_transaction=("plan_amount", "max"),
            lowest_transaction=("plan_amount", "min"),
        )
        .reset_index()
    )

    return merchant_summary


def rank_merchants(merchant_summary):
    """
    Rank merchants from highest to lowest transaction revenue.
    """

    ranked_merchants = (
        merchant_summary
        .sort_values(
            by=[
                "total_revenue",
                "transaction_count",
            ],
            ascending=[
                False,
                False,
            ],
        )
        .reset_index(drop=True)
    )

    ranked_merchants.index = ranked_merchants.index + 1
    ranked_merchants.index.name = "rank"

    return ranked_merchants


def filter_by_user_type(ranked_merchants, user_type):
    """
    Return merchants belonging to one user category.
    """

    return ranked_merchants[
        ranked_merchants["user_type"]
        .astype(str)
        .str.strip()
        .str.casefold()
        == user_type.strip().casefold()
    ]


def print_ranking_table(ranked_merchants, title, limit=10):
    """
    Print a readable merchant ranking table.
    """

    display_data = ranked_merchants.head(limit).copy()

    display_data["total_revenue"] = (
        display_data["total_revenue"]
        .apply(format_currency)
    )

    display_data["average_transaction"] = (
        display_data["average_transaction"]
        .apply(format_currency)
    )

    display_data["highest_transaction"] = (
        display_data["highest_transaction"]
        .apply(format_currency)
    )

    display_data["lowest_transaction"] = (
        display_data["lowest_transaction"]
        .apply(format_currency)
    )

    print(f"\n===== {title} =====")

    print(
        display_data[
            [
                "username",
                "full_name",
                "user_type",
                "total_revenue",
                "transaction_count",
                "average_transaction",
            ]
        ].to_string()
    )


def export_ranking_report(ranked_merchants):
    """
    Export the complete merchant ranking to Excel.
    """

    export_data = ranked_merchants.reset_index()

    with pd.ExcelWriter(
        RANKING_REPORT_FILE,
        engine="openpyxl",
    ) as writer:

        export_data.to_excel(
            writer,
            sheet_name="Overall Ranking",
            index=False,
        )

        user_types = (
            export_data["user_type"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        for user_type in user_types:
            filtered_data = export_data[
                export_data["user_type"]
                .astype(str)
                .str.strip()
                .str.casefold()
                == user_type.casefold()
            ]

            # Excel sheet names cannot exceed 31 characters.
            sheet_name = user_type[:31] or "Unknown Type"

            filtered_data.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
            )

    print(
        f"\n✅ Ranking report exported to: "
        f"{RANKING_REPORT_FILE}"
    )


def generate_ranking_report():
    """
    Run the complete merchant-ranking process.
    """

    users, transactions = load_clean_data()

    merged_data = merge_users_and_transactions(
        users,
        transactions,
    )

    merchant_summary = calculate_merchant_summary(
        merged_data
    )

    ranked_merchants = rank_merchants(
        merchant_summary
    )

    print_ranking_table(
        ranked_merchants,
        f"TOP {TOP_MERCHANT_LIMIT} MERCHANTS",
        TOP_MERCHANT_LIMIT,
    )

    api_users = filter_by_user_type(
        ranked_merchants,
        "API USER",
    )

    if not api_users.empty:
        print_ranking_table(
            api_users,
            "TOP API USERS",
            TOP_MERCHANT_LIMIT,
        )

    resellers = filter_by_user_type(
        ranked_merchants,
        "RESELLER",
    )

    if not resellers.empty:
        print_ranking_table(
            resellers,
            "TOP RESELLERS",
            TOP_MERCHANT_LIMIT,
        )

    export_ranking_report(ranked_merchants)

    return ranked_merchants


if __name__ == "__main__":
    generate_ranking_report()