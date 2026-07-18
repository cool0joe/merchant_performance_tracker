import streamlit as st
import pandas as pd
from pathlib import Path
import sys

from analytics.validation import run_validation
from analytics.cleaning import run_cleaning
from analytics.revenue import generate_revenue_report
from analytics.ranking import generate_ranking_report
from analytics.reports import generate_management_report
from config import (
    DATA_FOLDER,
    REPORT_FOLDER,
    RAW_USERS_FILE,
    RAW_DATA_TRANSACTIONS_FILE,
    REVENUE_REPORT_FILE,
    RANKING_REPORT_FILE,
    INACTIVITY_REPORT_FILE,
    MANAGEMENT_REPORT_FILE,
    APP_NAME,
    APP_VERSION,
)

st.set_page_config(
    page_title=f"{APP_NAME}",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(f"📊 {APP_NAME}")
st.caption(f"v{APP_VERSION}")


def save_uploaded_file(uploaded_file, target_path):
    """Save uploaded file to target path."""
    try:
        with open(target_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False


def load_report(filepath):
    """Load report Excel file as DataFrame."""
    try:
        if filepath.exists():
            return pd.read_excel(filepath)
        return None
    except Exception as e:
        st.error(f"Error loading report: {e}")
        return None


# Navigation
page = st.sidebar.radio(
    "📍 Navigation",
    ["Upload & Process", "View Reports"],
    index=0,
)

if page == "Upload & Process":
    st.header("📤 Upload & Process Files")
    st.markdown("Upload your Excel files to process merchant data.")

    col1, col2 = st.columns(2)

    users_file = None
    transactions_file = None

    with col1:
        st.subheader("Users File")
        users_file = st.file_uploader(
            "Upload Users Excel File",
            type="xlsx",
            key="users_uploader",
            help="Required: users.xlsx from VTU database export",
        )

    with col2:
        st.subheader("Transactions File")
        transactions_file = st.file_uploader(
            "Upload Transactions Excel File",
            type="xlsx",
            key="transactions_uploader",
            help="Required: data_transactions.xlsx from VTU database export",
        )

    st.divider()

    # Process button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

    with col_btn1:
        process_btn = st.button(
            "🚀 Process Files",
            type="primary",
            use_container_width=True,
        )

    with col_btn2:
        clear_btn = st.button(
            "🗑️ Clear Files",
            use_container_width=True,
        )

    if clear_btn:
        st.info("Click 'Process Files' with new uploads to replace files.")

    if process_btn:
        if users_file is None or transactions_file is None:
            st.error("⚠️ Please upload both files before processing.")
        else:
            # Save files
            with st.spinner("💾 Saving uploaded files..."):
                users_saved = save_uploaded_file(users_file, RAW_USERS_FILE)
                transactions_saved = save_uploaded_file(
                    transactions_file, RAW_DATA_TRANSACTIONS_FILE
                )

            if not (users_saved and transactions_saved):
                st.error("Failed to save files. Please try again.")
            else:
                st.success("✅ Files saved successfully!")

                # Run pipeline
                progress_placeholder = st.empty()
                status_placeholder = st.empty()

                steps = [
                    ("Running validation...", run_validation),
                    ("Cleaning data...", run_cleaning),
                    ("Generating revenue report...", generate_revenue_report),
                    ("Generating ranking report...", generate_ranking_report),
                    ("Generating management report...", generate_management_report),
                ]

                all_success = True

                for i, (step_name, step_func) in enumerate(steps):
                    progress = (i + 1) / len(steps)
                    progress_placeholder.progress(progress, text=step_name)

                    try:
                        result = step_func()
                        if step_name.startswith("Running validation") and not result:
                            status_placeholder.error(
                                "❌ Validation failed. Please check your data."
                            )
                            all_success = False
                            break
                    except Exception as e:
                        status_placeholder.error(f"❌ Error in {step_name}: {e}")
                        all_success = False
                        break

                if all_success:
                    progress_placeholder.progress(
                        1.0, text="✅ Pipeline completed!"
                    )
                    st.success(
                        "🎉 All reports generated successfully! Check 'View Reports' tab."
                    )
                    st.balloons()

    # File info
    st.divider()
    st.subheader("📋 Current Files in System")

    col_users, col_trans = st.columns(2)

    with col_users:
        if RAW_USERS_FILE.exists():
            st.info(f"✅ Users file exists: `{RAW_USERS_FILE.name}`")
            try:
                user_rows = len(pd.read_excel(RAW_USERS_FILE))
                st.caption(f"Records: {user_rows:,}")
            except:
                pass
        else:
            st.warning("📁 No users file found")

    with col_trans:
        if RAW_DATA_TRANSACTIONS_FILE.exists():
            st.info(f"✅ Transactions file exists: `{RAW_DATA_TRANSACTIONS_FILE.name}`")
            try:
                trans_rows = len(pd.read_excel(RAW_DATA_TRANSACTIONS_FILE))
                st.caption(f"Records: {trans_rows:,}")
            except:
                pass
        else:
            st.warning("📁 No transactions file found")


elif page == "View Reports":
    st.header("📊 Generated Reports")
    st.markdown("View and download your merchant performance reports.")

    reports = {
        "💰 Revenue Report": REVENUE_REPORT_FILE,
        "🏆 Merchant Ranking": RANKING_REPORT_FILE,
        "⚠️ Inactive Merchants": INACTIVITY_REPORT_FILE,
        "📈 Management Summary": MANAGEMENT_REPORT_FILE,
    }

    available_reports = {}
    for name, filepath in reports.items():
        if filepath.exists():
            available_reports[name] = filepath

    if not available_reports:
        st.warning(
            "📁 No reports found. Please upload files and process them first."
        )
    else:
        st.success(f"Found {len(available_reports)} report(s)")
        st.divider()

        # Create tabs for each report
        tab_list = list(available_reports.keys())
        tabs = st.tabs(tab_list)

        for tab, (report_name, filepath) in zip(tabs, available_reports.items()):
            with tab:
                df = load_report(filepath)

                if df is not None:
                    # Display stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Records", len(df))
                    with col2:
                        st.metric("Columns", len(df.columns))
                    with col3:
                        st.metric("File", filepath.name)

                    st.divider()

                    # Display dataframe
                    st.dataframe(df, use_container_width=True, height=400)

                    # Download button
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label=f"⬇️ Download {report_name}",
                            data=f.read(),
                            file_name=filepath.name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                        )

    st.divider()
    st.info(
        "💡 **Tip:** Use the 'Upload & Process' tab to generate fresh reports with updated data."
    )
