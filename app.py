import streamlit as st
import pandas as pd
import io
from core import file_handler, preprocessing, visualization

# First line = page setup
st.set_page_config(page_title="🧼 Data Cleaning Tool", layout="wide")

# 🌐 Language support
languages = {
    "English": {
        "title": "🧼 Data Cleaning & Analysis Tool",
        "about": "A simple no-code tool to inspect, clean, and export datasets.",
        "upload": "📁 Upload Your File",
        "step1": "Step 1: File Upload",
        "step2": "Step 2: Explore & Clean",
        "step3": "Step 3: Download Results",
        "drop_cols": "🧺 Drop Columns",
        "reset": "🔁 Reset Dataset",
        "strategy": "Choose a method for filling missing values",
        "download": "⬇️ Download Cleaned Data",
        "convert_col": "🔄 Convert Column Type",
        "column_label": "Column",
        "convert_to": "Convert To",
        "convert_now": "Apply Conversion",
        "clean_now": "Clean Missing Values",
        "const_val": "Fill Value (only for 'constant')",
        "table_name": "SQLite Table Name",
        "format_label": "Download Format",
        "csv": "CSV",
        "excel": "Excel",
        "describe": "📈 Descriptive Statistics",
        "missing_summary": "🧃 Missing Value Summary",
        "missing_bar": "📊 Missing Values Percent (Bar Chart)",
        "missing_heatmap": "🗺️ Missing Values Heatmap",
        "correlation": "🔗 Correlation Heatmap",
        "distribution": "📌 Numeric Column Distribution",
        "choose_col": "Select numeric column",
        "file_uploaded": "✅ File uploaded successfully!",
        "file_reset": "🔁 Dataset reset to original upload",
        "file_cleaned": "✅ Data cleaned successfully!",
        "converted": " converted to ",
        "export_as": "Export Results",
        "preview": "🔍 Preview Your Dataset",
        "view_mode": "View Options",
        "top_rows": "👁 Top rows",
        "full_table": "📋 Full table (⚠️ slower)",
        "paginated": "📑 Paginated view",
        "rows_to_show": "Number of rows to show",
        "select_format": "Select Output Format"
    },
    "Arabic": {
        "title": "🧼 أداة تنظيف وتحليل البيانات",
        "about": "أداة سهلة بدون كود لاستكشاف وتنظيف وتحميل البيانات.",
        "upload": "📁 ارفع الملف",
        "step1": "الخطوة 1: رفع الملف",
        "step2": "الخطوة 2: الاستكشاف والتنظيف",
        "step3": "الخطوة 3: تحميل النتائج",
        "drop_cols": "🧺 حذف الأعمدة",
        "reset": "🔁 إعادة تعيين البيانات",
        "strategy": "اختر طريقة لمعالجة القيم المفقودة",
        "download": "⬇️ تحميل الملف المنظف",
        "convert_col": "🔄 تحويل نوع العمود",
        "column_label": "العمود",
        "convert_to": "تحويل إلى",
        "convert_now": "تنفيذ التحويل",
        "clean_now": "تنظيف القيم المفقودة",
        "const_val": "القيمة المستخدمة للملء (لطريقة الثابت)",
        "table_name": "اسم جدول SQLite",
        "format_label": "صيغة التحميل",
        "csv": "CSV",
        "excel": "Excel",
        "describe": "📈 الإحصائيات الوصفية",
        "missing_summary": "🧃 ملخص القيم المفقودة",
        "missing_bar": "📊 نسبة القيم المفقودة (رسم بياني)",
        "missing_heatmap": "🗺️ الخريطة الحرارية للقيم المفقودة",
        "correlation": "🔗 خريطة ارتباط الأعمدة",
        "distribution": "📌 توزيع الأعمدة الرقمية",
        "choose_col": "اختر عمودًا رقميًا",
        "file_uploaded": "✅ تم تحميل الملف بنجاح!",
        "file_reset": "🔁 تمت إعادة ضبط البيانات",
        "file_cleaned": "✅ تم تنظيف البيانات بنجاح!",
        "converted": " تم تحويله إلى ",
        "export_as": "تصدير النتائج",
        "preview": "🔍 معاينة البيانات",
        "view_mode": "خيارات العرض",
        "top_rows": "👁 الصفوف الأولى",
        "full_table": "📋 الجدول بالكامل (قد يتأخر)",
        "paginated": "📑 عرض متعدد الصفحات",
        "rows_to_show": "عدد الصفوف للعرض",
        "select_format": "اختر صيغة التصدير"
    }
}

# 🌐 Language toggle
lang = st.sidebar.selectbox("🌐 Language / اللغة", list(languages.keys()))
TXT = languages[lang]
st.title(TXT["title"])
st.sidebar.info(TXT["about"])

# Upload
st.sidebar.subheader(TXT["step1"])
uploaded_file = st.sidebar.file_uploader(TXT["upload"], type=["csv", "xlsx", "json", "db"])
file_format = st.sidebar.radio(TXT["format_label"], [TXT["csv"], TXT["excel"]])

# Upload & clean
if uploaded_file:
    ext = uploaded_file.name.split(".")[-1]
    try:
        if ext == "csv":
            df = file_handler.read_csv(uploaded_file)
        elif ext == "xlsx":
            df = file_handler.read_excel(uploaded_file)
        elif ext == "json":
            df = file_handler.read_json(uploaded_file)
        elif ext == "db":
            table_name = st.sidebar.text_input(TXT["table_name"])
            if table_name:
                df = file_handler.read_sqlite(uploaded_file, table_name)
        df.columns = df.columns.str.strip().str.replace(" ", "_")
        st.session_state.df_original = df.copy()
        st.session_state.df = df
        st.sidebar.success(TXT["file_uploaded"])
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.stop()

# After upload
if "df" in st.session_state:
    df = st.session_state.df
    row_count = df.shape[0]
    mem_usage = df.memory_usage(deep=True).sum()

    # Performance Warning
    if row_count > 50000 or mem_usage > 50_000_000:
        st.warning(f"⚠️ Dataset has {row_count} rows, may lag browser. Use preview or download only.")

    # Reset
    if st.sidebar.button(TXT["reset"]):
        st.session_state.df = st.session_state.df_original.copy()
        st.success(TXT["file_reset"])

    # Drop columns
    drop_cols = st.sidebar.multiselect(TXT["drop_cols"], df.columns)
    if drop_cols:
        st.session_state.df.drop(columns=drop_cols, inplace=True)
        st.sidebar.warning(f"Dropped: {drop_cols}")

    # Convert column
    with st.sidebar.expander(TXT["convert_col"]):
        col = st.selectbox(TXT["column_label"], df.columns)
        to_type = st.selectbox(TXT["convert_to"], ["str", "float", "int", "bool"])
        if st.button(TXT["convert_now"]):
            try:
                st.session_state.df = preprocessing.convert_data_type(df, col, to_type)
                st.sidebar.success(f"{col}{TXT['converted']}{to_type}")
            except Exception as e:
                st.sidebar.error(e)

    # Cleaning Strategy
    strategy = st.sidebar.selectbox(TXT["strategy"], ["drop", "mean", "median", "mode", "constant"])
    const_val = None
    if strategy == "constant":
        val_input = st.sidebar.text_input(TXT["const_val"])
        if val_input:
            const_val = float(val_input) if val_input.replace(".", "", 1).isdigit() else val_input
    if st.sidebar.button(TXT["clean_now"]):
        st.session_state.df = preprocessing.process_missing_values(
            st.session_state.df, strategy=strategy, fill_value=const_val
        )
        st.sidebar.success(TXT["file_cleaned"])

    # Main panel: Step 2
    df = st.session_state.df
    st.markdown(f"### {TXT['step2']}")

    # Preview modes
    st.subheader(TXT["preview"])
    with st.expander(TXT["view_mode"], expanded=True):
        view_mode = st.radio(" ", [TXT["top_rows"], TXT["full_table"], TXT["paginated"]])
        if view_mode == TXT["top_rows"]:
            n = st.slider(TXT["rows_to_show"], 10, min(1000, row_count), value=30)
            st.dataframe(df.head(n), use_container_width=True)
        elif view_mode == TXT["full_table"]:
            if row_count > 3000:
                st.warning("⚠️ Full table may freeze large sessions.")
            st.dataframe(df, use_container_width=True)
        else:
            st.data_editor(df.head(100), use_container_width=True, num_rows="dynamic")

    # Visuals
    with st.expander(TXT["missing_summary"]):
        st.dataframe(preprocessing.check_missing_values(df, percent=True).to_frame("% Missing"))

    with st.expander(TXT["missing_bar"]):
        visualization.plot_missing_bar(df)

    with st.expander(TXT["missing_heatmap"]):
        visualization.plot_missing_heatmap(df)

    with st.expander(TXT["correlation"]):
        visualization.plot_correlation(df)

    with st.expander(TXT["distribution"]):
        num_cols = df.select_dtypes("number").columns
        if len(num_cols):
            col = st.selectbox(TXT["choose_col"], num_cols)
            if col:
                visualization.plot_distribution(df, col)
        else:
            st.info("No numeric columns")

    # Step 3 - Download
    st.markdown(f"### {TXT['step3']}")
    st.markdown(f"#### {TXT['export_as']}")

    @st.cache_data
    def generate_download(df, format_):
        if format_ == TXT["csv"]:
            return df.to_csv(index=False).encode("utf-8"), "text/csv", "cleaned_data.csv"
        else:
            out = io.BytesIO()
            df.to_excel(out, index=False, engine="openpyxl")
            out.seek(0)
            return out, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "cleaned_data.xlsx"

    data, mime, name = generate_download(df, file_format)
    st.download_button(label=TXT["download"], data=data, file_name=name, mime=mime)