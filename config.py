from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent


# Folders
DATA_FOLDER = BASE_DIR / "data"
UPLOAD_FOLDER = BASE_DIR / "uploads"
REPORT_FOLDER = BASE_DIR / "reports"

UPLOAD_FOLDER.mkdir(exist_ok=True)
REPORT_FOLDER.mkdir(exist_ok=True)


# Raw VTU exports
RAW_USERS_FILE = DATA_FOLDER / "users.xlsx"
RAW_DATA_TRANSACTIONS_FILE = DATA_FOLDER / "data_transactions.xlsx"


# Cleaned datasets
CLEAN_USERS_FILE = UPLOAD_FOLDER / "users_clean.xlsx"
CLEAN_DATA_TRANSACTIONS_FILE = (
    UPLOAD_FOLDER / "data_transactions_clean.xlsx"
)


# Generated reports
REVENUE_REPORT_FILE = REPORT_FOLDER / "revenue_report.xlsx"
RANKING_REPORT_FILE = REPORT_FOLDER / "merchant_ranking.xlsx"
INACTIVITY_REPORT_FILE = REPORT_FOLDER / "inactive_merchants.xlsx"


# Analytics defaults
CURRENCY_SYMBOL = "₦"
TOP_MERCHANT_LIMIT = 10
INACTIVE_DAYS = 30


# App information
APP_NAME = "Merchant Performance Tracker"
APP_VERSION = "0.1.0"

# MANAGEMENT REPORTING
MANAGEMENT_REPORT_FILE = (
    REPORT_FOLDER / "merchant_performance_report.xlsx"
)

LOW_ACTIVITY_MAX_TRANSACTIONS = 2