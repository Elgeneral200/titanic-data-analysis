import streamlit as st
import pandas as pd
from core import file_handler, preprocessing, visualization

st.set_page_config(page_title="Data Cleaning Tool", layout="wide")
st.title("🧼 Internal Data Cleaning & Analysis Tool")

st.markdown("Upload your dataset to explore and fix missing data interactively.")

uploaded_file = st.file_uploader("📁 Upload file (CSV, Excel, JSON, SQLite)", type=['csv', 'xlsx', 'json', 'db'])

df = None
cleaned_df = None

if uploaded_file:
    file_suffix = uploaded_file.name.split('.')[-1]

    try:
        if file_suffix == 'csv':
            df = file_handler.read_csv(uploaded_file)
        elif file_suffix == 'xlsx':
            df = file_handler.read_excel(uploaded_file)
        elif file_suffix == 'json':
            df = file_handler.read_json(uploaded_file)
        elif file_suffix == 'db':
            table_name = st.text_input("Enter table name from the SQLite database:")
            if table_name:
                df = file_handler.read_sqlite(uploaded_file, table_name)
        else:
            st.error("❌ Unsupported file type.")
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

    st.subheader("📊 Data Preview")
    st.dataframe(df.head(30), use_container_width=True)

    st.subheader("❓ Missing Data Overview")
    st.dataframe(preprocessing.check_missing_values(df, percent=True).to_frame("Missing (%)"))

    with st.expander("🗺️ Show Missing Value Heatmap", expanded=False):
        visualization.plot_missing_heatmap(df)

    st.markdown("---")
    st.subheader("⚙️ Clean Missing Data")

    strategy = st.selectbox("Choose Strategy", ["drop", "mean", "median", "mode", "constant"])
    fill_value = None

    if strategy == "constant":
        fill_input = st.text_input("Enter fill value (string or number):")
        if fill_input:
            if fill_input.replace('.', '', 1).isdigit():
                fill_value = float(fill_input) if '.' in fill_input else int(fill_input)
            else:
                fill_value = fill_input

    if strategy != "constant" or (strategy == "constant" and fill_value is not None):
        cleaned_df = preprocessing.process_missing_values(df, strategy=strategy, fill_value=fill_value)
        st.success("✅ Data cleaned successfully.")

        st.subheader("🔍 Cleaned Data Preview")
        st.dataframe(cleaned_df.head(30), use_container_width=True)

        # Download cleaned file
        st.subheader("📥 Download Cleaned Data")
        csv_data = cleaned_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv_data, file_name="cleaned_data.csv", mime="text/csv")