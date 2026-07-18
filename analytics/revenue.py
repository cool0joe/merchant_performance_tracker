from utils import (
    load_clean_data,
    merge_users_and_transactions,
    format_currency,
)


def print_revenue_summary(merged_data):
    total_revenue = merged_data["plan_amount"].sum()
    total_transactions = len(merged_data)
    average_transaction = merged_data["plan_amount"].mean()
    highest_transaction = merged_data["plan_amount"].max()
    lowest_transaction = merged_data["plan_amount"].min()

    print("\n===== REVENUE SUMMARY =====")
    print(f"Total Revenue: {format_currency(total_revenue)}")
    print(f"Total Transactions: {total_transactions}")
    print(
        "Average Transaction Value:",
        format_currency(average_transaction),
    )
    print(
        "Highest Transaction:",
        format_currency(highest_transaction),
    )
    print(
        "Lowest Transaction:",
        format_currency(lowest_transaction),
    )


def print_revenue_by_merchant(merged_data):
    revenue_by_merchant = (
        merged_data
        .groupby("username")["plan_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n===== REVENUE BY MERCHANT =====")
    print(revenue_by_merchant.head(10))


def print_revenue_by_user_type(merged_data):
    revenue_by_user_type = (
        merged_data
        .groupby("user_type")["plan_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n===== REVENUE BY USER TYPE =====")
    print(revenue_by_user_type)


def print_revenue_by_network(merged_data):
    revenue_by_network = (
        merged_data
        .groupby("network_id")["plan_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n===== REVENUE BY NETWORK =====")
    print(revenue_by_network)


def print_revenue_by_plan(merged_data):
    revenue_by_plan = (
        merged_data
        .groupby("plan_id")["plan_amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n===== REVENUE BY PLAN =====")
    print(revenue_by_plan.head(10))


def generate_revenue_report():
    users, transactions = load_clean_data()

    merged_data = merge_users_and_transactions(
        users,
        transactions,
    )

    print_revenue_summary(merged_data)
    print_revenue_by_merchant(merged_data)
    print_revenue_by_user_type(merged_data)
    print_revenue_by_network(merged_data)
    print_revenue_by_plan(merged_data)


if __name__ == "__main__":
    generate_revenue_report()