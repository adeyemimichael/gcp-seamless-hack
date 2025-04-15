
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import time

# -- Google Sheets Authentication
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

def authenticate_google_sheets():
    try:
        creds = Credentials.from_service_account_file(
            'credentials/dataset-hackathon.json', scopes=SCOPES
        )
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Authentication failed: {e}")
        return None

client = authenticate_google_sheets()
if not client:
    st.stop()

# -- Load Google Sheet
sheet = client.open('PYUSD Transaction Log')
worksheet = sheet.get_worksheet(0)
pyusd_df = pd.DataFrame(worksheet.get_all_records())

# -- Preprocessing
pyusd_df['block_date'] = pd.to_datetime(pyusd_df['block_date'])
pyusd_df['from_label'] = pyusd_df['from_address'].map({
    '0x264bd8291fae1d75db2c5f573b07faa6715997b5': 'Paxos 4 (Hildobby)',
    '0x2893b326816ed864c4bccddeaa4a006c8367c229': 'Paxos Treasury (Hildobby)',
}).fillna('Unknown')

pyusd_df['from_address_link'] = pyusd_df['from_address'].apply(lambda x: f"[{x}](https://etherscan.io/address/{x})")

daily_volume = pyusd_df.groupby('block_date')['pyusd_amount'].sum().reset_index()

# -- Navigation
st.set_page_config(page_title="PYUSD Dashboard", layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navbar
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "home"
with col2:
    if st.button("📄 Transactions"):
        st.session_state.page = "transactions"
with col3:
    if st.button("🏷 Tags"):
        st.session_state.page = "tags"

# -- Sidebar Filter
st.sidebar.header("🛠️ Filter Options")
start_date = st.sidebar.date_input("Start Date", pyusd_df['block_date'].min())
end_date = st.sidebar.date_input("End Date", pyusd_df['block_date'].max())
wallet_filter = st.sidebar.text_input("Filter by Wallet Address")

filtered_df = pyusd_df[
    (pyusd_df['block_date'] >= pd.to_datetime(start_date)) &
    (pyusd_df['block_date'] <= pd.to_datetime(end_date))
]
if wallet_filter:
    filtered_df = filtered_df[filtered_df['from_address'].str.contains(wallet_filter, na=False)]

filtered_volume = filtered_df.groupby('block_date')['pyusd_amount'].sum().reset_index()

# -- Page Content
if st.session_state.page == "home":
    st.title("📊 PYUSD Ethereum Transfers Dashboard")
    st.subheader("📈 Daily Volume")
    st.line_chart(filtered_volume.set_index('block_date'))

    st.subheader("📊 Volume Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered_volume, x='block_date', y='pyusd_amount', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

elif st.session_state.page == "transactions":
    st.subheader("🔎 Wallet Transfers (Filtered)")
    display_columns = ['from_address_link', 'from_label', 'pyusd_amount', 'block_date']
    st.dataframe(filtered_df[display_columns])

    # Download as CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_pyusd.csv", "text/csv")

elif st.session_state.page == "tags":
    st.subheader("🏷 Wallet Summary")
    wallet_summary = filtered_df.groupby('from_address').agg(
        total_transactions=('pyusd_amount', 'count'),
        total_value=('pyusd_amount', 'sum')
    ).reset_index().sort_values(by='total_value', ascending=False)
    st.dataframe(wallet_summary)

# -- Google Sheet Update
if st.button("🔁 Update Google Sheet with Current Data"):
    set_with_dataframe(worksheet, pyusd_df)
    st.success("✅ Sheet updated!")

# -- Auto Refresh every 60s
if st.sidebar.checkbox("🔄 Auto-refresh (every 120 seconds)"):
    time.sleep(120)
    st.experimental_rerun()
