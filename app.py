import streamlit as st
import pandas as pd
from core import file_handler, preprocessing, visualization

st.set_page_config(page_title="Data Cleaning Tool", layout="wide")
st.title("🧼 Internal Data Cleaning & Analysis Tool")

st.markdown("Upload a dataset to clean, visualize, and export it with zero code.")

uploaded_file = st.file_uploader("📁 Upload your data file", type=["csv", "xlsx", "json", "db"])

df = None
cleaned_df = None

if uploaded_file:
    ext = uploaded_file.name.split('.')[-1]

    try:
        if ext == "csv":
            df = file_handler.read_csv(uploaded_file)
        elif ext == "xlsx":
            df = file_handler.read_excel(uploaded_file)
        elif ext == "json":
            df = file_handler.read_json(uploaded_file)
        elif ext == "db":
            table_name = st.text_input("Enter table name from SQLite DB")
            if table_name:
                df = file_handler.read_sqlite(uploaded_file, table_name)
    except Exception as e:
        st.error(f"❌ Failed to read file: {e}")
        st.stop()

    st.subheader("📊 Data Preview")
    st.dataframe(df.head(30), use_container_width=True)

    st.subheader("📈 Descriptive Statistics")
    with st.expander("👉 Show summary"):
        st.markdown("### 📐 Numeric Columns:")
        st.dataframe(df.describe().T)

        st.markdown("### 📋 Top Categorical Values:")
        for col in df.select_dtypes(include="object").columns:
            st.markdown(f"**{col}**")
            st.dataframe(df[col].value_counts().head(5).to_frame("Count"))

    st.subheader("🕳️ Missing Value Summary")
    st.dataframe(preprocessing.check_missing_values(df, percent=True).to_frame("Missing (%)"))

    with st.expander("🗺️ Missing Values Heatmap"):
        visualization.plot_missing_heatmap(df)

    st.subheader("🔁 Convert Column Type")
    col = st.selectbox("Select column to convert", df.columns)
    new_type = st.selectbox("Convert to", ["str", "float", "int", "bool"])

    try:
        df = preprocessing.convert_data_type(df, col, new_type)
        st.success(f"Column '{col}' converted to {new_type}")
    except Exception as e:
        st.error(f"Conversion failed: {e}")

    st.subheader("⏳ Time-Series Cleaning")
    time_col = st.selectbox("Select date column for forward fill", ["None"] + df.columns.tolist())

    if time_col != "None":
        with st.expander("⚙️ Optional: Set date format"):
            fmt = st.text_input("Format (e.g. %Y-%m-%d)", "")
        if fmt:
            df[time_col] = pd.to_datetime(df[time_col], format=fmt, errors="coerce")
        else:
            df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
        df = df.sort_values(by=time_col)
        df = df.ffill()
        st.success("Forward fill applied.")

    df_before = df.copy()

    st.header("🧼 Clean Missing Values")
    strategy = st.selectbox("Choose strategy", ["drop", "mean", "median", "mode", "constant"])
    const_val = None
    if strategy == "constant":
        val_input = st.text_input("Constant fill value:")
        if val_input.replace('.', '', 1).isdigit():
            const_val = float(val_input) if '.' in val_input else int(val_input)
        else:
            const_val = val_input

    if st.button("🚀 Clean Now"):
        cleaned_df = preprocessing.process_missing_values(df, strategy=strategy, fill_value=const_val)

        st.success("✅ Cleaning completed")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🪞 **Before**")
            st.dataframe(df_before.head(30))
        with col2:
            st.markdown("✅ **After**")
            st.dataframe(cleaned_df.head(30))

        st.subheader("💾 Download")
        csv = cleaned_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")