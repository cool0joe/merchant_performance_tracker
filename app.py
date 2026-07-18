from analytics.validation import run_validation
from analytics.cleaning import run_cleaning
from analytics.revenue import generate_revenue_report
from analytics.ranking import generate_ranking_report
from analytics.reports import generate_management_report


def main():
    print("\n===== MERCHANT PERFORMANCE TRACKER =====")

    validation_passed = run_validation()

    if not validation_passed:
        print("\nProcessing stopped because validation failed.")
        return

    run_cleaning()
    generate_revenue_report()
    generate_ranking_report()
    generate_management_report()

    print("\n✅ Pipeline completed successfully.")


if __name__ == "__main__":
    main()