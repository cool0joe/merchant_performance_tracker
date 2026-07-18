# 📊 Merchant Performance Tracker

A data-driven analytics platform designed to evaluate and rank merchant performance using VTU (Virtual Top-up) transaction data. Built with Python and Streamlit for lightweight, accessible data analysis without requiring advanced technical knowledge.

**Version:** 0.1.0 (MVP)  
**Author:** Joseph Adeoye  
**Status:** Active Development

---

## 🎯 What Problem Does This Solve?

Managing merchant performance across a large network is complex and time-consuming. Traditional approaches rely on manual spreadsheet analysis, which is:

- **Error-prone** — Manual calculations and copy-paste errors
- **Time-consuming** — Hours spent organizing and calculating metrics
- **Inconsistent** — Different stakeholders use different methodologies
- **Non-scalable** — Becomes unwieldy as merchant count grows
- **Difficult to track** — Hard to spot trends or underperforming merchants

**Merchant Performance Tracker solves this by:**
- ✅ Automating data validation and cleaning
- ✅ Generating consistent, reproducible reports
- ✅ Identifying revenue patterns and merchant rankings
- ✅ Highlighting inactive merchants for re-engagement
- ✅ Creating actionable management summaries

---

## 🏗️ How It Works

### **Architecture Overview**

```
┌─────────────────────────────────────────┐
│   User (Streamlit Web Interface)        │
│   - Upload Excel Files                  │
│   - View Generated Reports              │
│   - Download Results                    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Streamlit App (streamlit_app.py)      │
│   - File Upload Handler                 │
│   - Pipeline Orchestrator               │
│   - Report Display & Download           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Analytics Pipeline (analytics/)       │
│                                         │
│   1. Validation Layer                   │
│   ├─ Check required columns             │
│   ├─ Verify data types                  │
│   └─ Detect anomalies                   │
│                                         │
│   2. Cleaning Layer                     │
│   ├─ Normalize column names             │
│   ├─ Handle duplicates                  │
│   └─ Standardize formats                │
│                                         │
│   3. Analysis Layer                     │
│   ├─ Revenue calculations               │
│   ├─ Merchant ranking                   │
│   ├─ Inactivity detection               │
│   └─ Management reporting               │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Output (reports/)                     │
│   - revenue_report.xlsx                 │
│   - merchant_ranking.xlsx               │
│   - inactive_merchants.xlsx             │
│   - merchant_performance_report.xlsx    │
└─────────────────────────────────────────┘
```

### **Data Flow**

1. **Upload Phase**
   - User uploads two Excel files (Users + Transactions)
   - Files saved to `data/` directory
   - Streamlit UI provides feedback

2. **Validation Phase**
   - Checks for required columns in both datasets
   - Verifies data types and formats
   - Detects corrupted or missing data
   - Stops pipeline if validation fails

3. **Cleaning Phase**
   - Removes accidental whitespace from column names
   - Standardizes data formats
   - Handles missing values
   - Creates cleaned dataset copies

4. **Analysis Phase**
   - Calculates revenue metrics per merchant
   - Ranks merchants by performance
   - Identifies inactive merchants (no transactions in 30 days)
   - Flags low-activity merchants (≤2 transactions)
   - Generates management summary

5. **Output Phase**
   - Writes 4 Excel reports to `reports/` folder
   - User downloads via Streamlit interface

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit 1.59+ | Web UI for uploads & report viewing |
| **Backend** | Python 3.8+ | Core analytics logic |
| **Data Processing** | Pandas | DataFrame manipulation & analysis |
| **File I/O** | OpenPyXL | Excel read/write operations |

---

## 📖 Usage Guide

### **Upload & Process Files**

1. **Prepare Your Data**
   - Export `users.xlsx` from VTU database (contains merchant info)
   - Export `data_transactions.xlsx` from VTU database (contains transaction records)
   - Ensure both files are in Excel format

2. **Upload Files**
   - Click "📤 Upload & Process Files" tab
   - Upload both Excel files using the file pickers
   - Green checkmarks indicate successful uploads

3. **Process**
   - Click "🚀 Process Files" button
   - Watch the progress bar as pipeline runs
   - Wait for ✅ completion message

4. **View Results**
   - Click "📊 View Reports" tab
   - See all generated reports as interactive tables
   - Download each report as Excel if needed

### **Understanding the Reports**

#### **💰 Revenue Report**
- Merchant ID and name
- Total transactions processed
- Total revenue generated
- Average transaction value
- Revenue ranking

#### **🏆 Merchant Ranking**
- Ranked by transaction volume (Top 10)
- Performance tier classification
- Transaction count & revenue per merchant
- Comparison metrics

#### **⚠️ Inactive Merchants**
- Merchants with no transactions in 30+ days
- Contact information for re-engagement
- Last transaction date
- Historical activity level

#### **📈 Management Summary**
- High-level KPIs (total merchants, revenue, transactions)
- Top performers and bottom performers
- Risk metrics (inactive, low-activity merchants)
- Actionable insights and recommendations

---

## 📁 Project Structure

```
merchant_performance_tracker/
├── streamlit_app.py              # Main Streamlit web application
├── app.py                        # CLI entry point (alternative)
├── config.py                     # Configuration & file paths
├── utils.py                      # Utility functions
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── analytics/                    # Core analytics modules
│   ├── validation.py             # Data validation logic
│   ├── cleaning.py               # Data cleaning & standardization
│   ├── revenue.py                # Revenue calculations
│   ├── ranking.py                # Merchant ranking logic
│   ├── reports.py                # Management report generation
│   ├── growth.py                 # Growth analysis (future)
│   └── inactivity.py             # Inactivity detection (future)
│
├── data/                         # Input data directory
│   ├── users.xlsx                # User/merchant master data
│   └── data_transactions.xlsx    # Transaction records
│
├── uploads/                      # Cleaned data directory
│   ├── users_clean.xlsx          # Validated users data
│   └── data_transactions_clean.xlsx  # Validated transactions
│
└── reports/                      # Output reports directory
    ├── revenue_report.xlsx
    ├── merchant_ranking.xlsx
    ├── inactive_merchants.xlsx
    └── merchant_performance_report.xlsx
```

---

## 🔧 How It Was Carefully Constructed

### **Design Principles**

1. **Separation of Concerns**
   - Validation logic separate from cleaning
   - Analysis independent of I/O operations
   - Frontend (Streamlit) decoupled from backend (analytics/)

2. **Data Integrity**
   - Each step validates before proceeding
   - Pipeline stops on validation failure (prevents garbage output)
   - Original data never modified (kept in `data/`)
   - Cleaned copies stored separately (`uploads/`)

3. **Configurability**
   - All settings centralized in `config.py`
   - Easy to adjust thresholds (inactive days, top merchant limit, etc.)
   - File paths defined once, used everywhere

4. **Scalability**
   - Pandas handles large datasets efficiently
   - Low memory footprint (no database overhead)
   - Can process thousands of merchants without slowdown

5. **User Experience**
   - Streamlit provides intuitive web interface
   - No technical knowledge required to use
   - Progress feedback during processing
   - Clear error messages guide troubleshooting

### **Development Approach**

**Phase 1: Core Pipeline**
- Built validation logic first (trust input data)
- Implemented cleaning procedures (standardize formats)
- Created analysis modules (calculate metrics)
- Tested with real GLO merchant data

**Phase 2: Reporting**
- Designed 4 distinct reports serving different audiences
- Revenue report: for finance teams
- Ranking report: for performance management
- Inactivity report: for business development
- Management summary: for executives

**Phase 3: User Interface**
- Chose Streamlit for lightweight, Python-native UI
- Built upload workflow matching data pipeline
- Added file validation feedback
- Implemented report viewing with download capability

**Phase 4: Polish**
- Added error handling at each pipeline step
- Improved progress visibility
- Enhanced user feedback messages
- Optimized performance

### **Key Technical Decisions**

| Decision | Reasoning |
|----------|-----------|
| **Streamlit** | Native Python, minimal setup, perfect for data apps |
| **Pandas** | Industry-standard for tabular data, excellent Excel support |
| **Excel I/O** | Stakeholders expect Excel reports, OpenPyXL handles it well |
| **Local-first** | Low bandwidth, privacy-preserving, works offline |
| **Sequential Pipeline** | Ensures data quality; stops early if validation fails |
| **No Database** | Overkill for merchant batch processing; files are simpler |

---

## 📊 Current Capabilities

✅ **Implemented**
- User data import and validation
- Transaction data import and validation
- Data cleaning and standardization
- Revenue calculations per merchant
- Merchant ranking by performance
- Inactive merchant detection (30+ days)
- Low-activity merchant flagging (≤2 transactions)
- Management report generation
- Web-based file upload & report viewing
- Excel report downloads

📋 **Planned (v0.2)**
- Growth trend analysis
- Seasonal pattern detection
- Predictive churn modeling
- Custom date range filtering
- Merchant tier classification
- Email report distribution
- Historical data tracking
- Dashboard charts & visualizations

---


## 🔐 Security & Privacy

- **Local processing:** No data sent to external servers
- **No authentication:** Run locally or on secure internal network
- **File validation:** Prevents malformed data from corrupting system
- **Error handling:** Detailed errors logged, not exposed to end users

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Visualizations (Plotly charts)
- Database integration for historical tracking
- API wrapper for programmatic access
- Performance optimizations for 100K+ merchants

---

## 📞 Support

**Issues or Questions?**
- Check the logs in terminal where Streamlit runs
- Verify Excel files have required columns
- Ensure Python 3.8+ installed
- Check GitHub issues for similar problems

---

## 📄 License

This project is currently closed-source. Contact the author for licensing inquiries.

---

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io) — Amazing framework for data apps
- [Pandas](https://pandas.pydata.org) — Data manipulation powerhouse
- Python community — For excellent libraries and tools

---

## 📈 Roadmap

**v0.2 (Q3 2026)**
- Chart visualizations
- Custom reporting filters
- Email delivery

**v0.3 (Q4 2026)**
- Predictive analytics
- Merchant tier automation
- API endpoints

**v1.0 (2027)**
- Multi-source data integration
- Real-time dashboards
- Mobile app

---

**Last Updated:** July 17, 2026  
**Maintained By:** Joseph Adeoye
