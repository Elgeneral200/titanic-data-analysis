# app.py
"""
Professional Data Cleaning & Analysis Tool

A comprehensive Streamlit application for data cleaning, analysis, and visualization
with multilingual support (English/Arabic) and professional UI/UX design.

Author: Data Cleaning Tool Team
Version: 2.3.1
"""

from typing import Any, Dict, Optional, Tuple

import io
import pandas as pd
import streamlit as st

from core import file_handler, preprocessing, visualization

# Page configuration
st.set_page_config(
    page_title="🧼 Data Cleaning Tool",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://docs.streamlit.io",
        "Report a bug": "https://github.com/streamlit/streamlit/issues",
        "About": "Professional Data Cleaning Tool v2.3.1",
    },
)

# Global dark theme styling (no pure whites)
st.markdown(
    """
<style>
    :root {
        --primary-color: #3b82f6;     /* Bright blue for accents */
        --accent-color: #22d3ee;      /* Cyan accent */
        --success-color: #10b981;     /* Emerald */
        --warning-color: #f59e0b;     /* Amber */
        --danger-color: #ef4444;      /* Red */
        --info-color: #38bdf8;        /* Sky */
        --bg-primary: #0b1220;        /* App background */
        --bg-panel: #0f172a;          /* Panels / shells */
        --bg-surface: #111827;        /* Cards / containers */
        --bg-elev: #1f2937;           /* Elevated surfaces */
        --border-color: #334155;      /* Borders */
        --text-color: #e5e7eb;        /* Primary text */
        --text-muted: #94a3b8;        /* Muted text */
    }

    /* App background */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-primary);
        color: var(--text-color);
    }

    /* Main content wrapper */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* Sidebar dark */
    [data-testid="stSidebar"] {
        background-color: var(--bg-panel);
        color: var(--text-color);
        border-right: 1px solid var(--border-color);
    }

    /* Metrics styled as dark cards */
    [data-testid="metric-container"] {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
        margin: 6px 0;
        color: var(--text-color);
    }

    /* Dark tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: var(--bg-panel);
        border-radius: 8px;
        padding: 6px;
        border: 1px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: var(--bg-surface);
        border-radius: 6px;
        border: 1px solid var(--border-color);
        color: var(--text-color) !important;
        font-weight: 600;
        transition: all 0.15s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--bg-elev);
        color: var(--text-color) !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: #0b1220 !important;
        border-color: var(--primary-color);
        box-shadow: 0 2px 6px rgba(59,130,246,0.35);
    }

    /* Dark containers */
    .main-container {
        padding: 16px;
        background-color: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        margin: 12px 0;
        color: var(--text-color);
    }

    /* RTL support for Arabic */
    .rtl {
        direction: rtl;
        text-align: right;
    }

    /* Section header */
    .section-header {
        color: var(--text-color);
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 10px;
        margin-bottom: 16px;
    }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 9px 18px;
        font-weight: 600;
        color: var(--text-color);
        background: linear-gradient(180deg, var(--bg-elev), var(--bg-surface));
        transition: all 0.15s;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(0,0,0,0.35);
        background: linear-gradient(180deg, var(--bg-elev), var(--bg-elev));
    }

    /* Alerts on dark */
    .stAlert {
        background-color: var(--bg-surface);
        color: var(--text-color);
        border-left: 4px solid var(--info-color);
        border-top: 1px solid var(--border-color);
        border-right: 1px solid var(--border-color);
        border-bottom: 1px solid var(--border-color);
        border-radius: 8px;
    }

    /* Inputs / selects */
    [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
        color: var(--text-color) !important;
        background-color: var(--bg-surface) !important;
    }
    [data-baseweb="select"] > div {
        background-color: var(--bg-surface) !important;
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }
    .stTextInput > div > div, .stSelectbox > div > div, .stMultiSelect > div > div, .stSlider > div {
        background-color: var(--bg-surface) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }

    /* Expander dark */
    [data-testid="stExpander"] details {
        background: var(--bg-surface);
        color: var(--text-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    [data-testid="stExpander"] summary {
        color: var(--text-color);
    }

    /* Tables and DataFrames dark */
    [data-testid="stTable"] table, [data-testid="stTable"] thead, [data-testid="stTable"] tbody, 
    [data-testid="stTable"] tr, [data-testid="stTable"] th, [data-testid="stTable"] td {
        background-color: var(--bg-surface) !important;
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }

    [data-testid="stDataFrame"] {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    [data-testid="stDataFrame"] div {
        color: var(--text-color) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Language packs (shortened here for brevity; unchanged content from v2.3)
languages = {
    "English": {
        "title": "🧼 Data Cleaning & Analysis Tool",
        "subtitle": "Professional No-Code Data Processing Platform",
        "about": "A professional no-code tool to inspect, clean, and export datasets with advanced type management.",
        "step1": "🏷️ Column Types",
        "step2": "🔍 Data Preview",
        "step3": "🧹 Data Cleaning",
        "step4": "📊 Visualizations",
        "step5": "⬇️ Export Results",
        "upload": "Upload Your File",
        "drag_drop": "Drag and drop file here or click to browse",
        "file_types": "Supported: CSV, Excel, JSON, SQLite",
        "table_name": "SQLite Table Name",
        "file_uploaded": "✅ File uploaded successfully!",
        "file_reset": "🔁 Dataset reset to original upload",
        "column_types": "Column Type Management",
        "auto_detect": "🤖 Auto-detect Column Types",
        "manual_override": "✏️ Manual Type Override",
        "apply_types": "Apply Type Changes",
        "numerical": "Numerical",
        "categorical": "Categorical",
        "type_legend": "Type Legend",
        "num_desc": "**num**: Numerical data for mathematical operations",
        "cat_desc": "**cat**: Categorical data for grouping/classification",
        "current_distribution": "Current Distribution",
        "select_columns_drop": "Select columns to drop",
        "drop_selected": "Drop Selected",
        "drop_cols": "🗑️ Drop Columns",
        "reset": "🔄 Reset Dataset",
        "convert_col": "🔄 Convert Column Type",
        "column_label": "Select Column",
        "convert_to": "Convert To",
        "convert_now": "Apply Conversion",
        "converted": " converted to ",
        "convert_section_title": "Data Type Conversion",
        "cleaning_strategy": "Cleaning Strategy",
        "target_columns": "Target Columns (empty = all)",
        "clean_now": "Apply Cleaning",
        "file_cleaned": "✅ Data cleaned successfully!",
        "const_val": "Fill Value",
        "missing_treatment": "Missing Value Treatment",
        "cleaning_summary": "Cleaning Summary",
        "total_missing": "Total Missing Values",
        "most_missing": "Most Missing Column",
        "preview": "Data Preview",
        "data_overview": "Data Overview",
        "view_mode": "View Mode",
        "top_rows": "Top Rows",
        "random_sample": "Random Sample",
        "full_table": "Full Table",
        "rows_to_show": "Rows to Display",
        "quick_stats": "Quick Statistics",
        "num_summary": "Numerical Columns Summary",
        "missing_summary": "Missing Values Summary",
        "no_missing": "No missing values!",
        "show_column_info": "Show column info",
        "no_numerical_selected": "No numerical columns selected",
        "visualizations": "Data Visualizations",
        "missing_data": "Missing Data Analysis",
        "numerical_analysis": "Numerical Analysis",
        "categorical_analysis": "Categorical Analysis",
        "advanced_analysis": "Advanced Analysis",
        "viz_type": "Visualization Type",
        "select_columns": "Select columns to visualize",
        "distribution": "Distribution",
        "box_plot": "Box Plot",
        "correlation": "Correlation Matrix",
        "value_counts": "Value Counts",
        "top_categories": "Top Categories",
        "export_title": "Export Results",
        "export_format": "Export Format",
        "final_summary": "Final Dataset Summary",
        "memory_usage": "Memory Usage",
        "download_csv": "⬇️ Download CSV File",
        "download_excel": "⬇️ Download Excel File",
        "download_config": "⬇️ Download Configuration",
        "column_types_summary": "Column Types Summary",
        "rows": "Rows",
        "columns": "Columns",
        "missing_values": "Missing Values",
        "unique_values": "Unique Values",
        "data_type": "Data Type",
        "no_data": "No data available",
        "loading": "Loading...",
        "error": "Error",
        "success": "Success",
        "warning": "Warning",
        "info": "Information",
        "welcome_title": "Welcome to the Professional Data Cleaning Tool! 👋",
        "welcome_desc": "Transform your raw data into clean, analysis-ready datasets",
        "feature1_title": "🎯 Smart Type Detection",
        "feature1_desc": "Automatic numerical/categorical detection with manual override capabilities",
        "feature2_title": "📊 Professional Visualizations",
        "feature2_desc": "Interactive charts with side-by-side layouts and optimized performance",
        "feature3_title": "🚀 Enterprise Features",
        "feature3_desc": "Multilingual support, large dataset handling, and export configurations",
        "get_started": "Get started by uploading a file in the sidebar! →",
    },
    "العربية": {
        "title": "🧼 أداة تنظيف وتحليل البيانات",
        "subtitle": "منصة معالجة البيانات الاحترافية بدون كود",
        "about": "أداة احترافية بدون كود لفحص وتنظيف وتصدير مجموعات البيانات مع إدارة متقدمة للأنواع.",
        "step1": "🏷️ أنواع الأعمدة",
        "step2": "🔍 معاينة البيانات",
        "step3": "🧹 تنظيف البيانات",
        "step4": "📊 التصورات البيانية",
        "step5": "⬇️ تصدير النتائج",
        "upload": "ارفع ملفك",
        "drag_drop": "اسحب وأفلت الملف هنا أو انقر للتصفح",
        "file_types": "المدعوم: CSV، Excel، JSON، SQLite",
        "table_name": "اسم جدول SQLite",
        "file_uploaded": "✅ تم رفع الملف بنجاح!",
        "file_reset": "🔁 تمت إعادة ضبط البيانات للملف الأصلي",
        "column_types": "إدارة أنواع الأعمدة",
        "auto_detect": "🤖 اكتشاف أنواع الأعمدة تلقائياً",
        "manual_override": "✏️ تعديل الأنواع يدوياً",
        "apply_types": "تطبيق تغييرات الأنواع",
        "numerical": "رقمي",
        "categorical": "فئوي",
        "type_legend": "دليل الأنواع",
        "num_desc": "**num**: بيانات رقمية للعمليات الحسابية",
        "cat_desc": "**cat**: بيانات فئوية للتجميع والتصنيف",
        "current_distribution": "التوزيع الحالي",
        "select_columns_drop": "اختر الأعمدة للحذف",
        "drop_selected": "حذف المحدد",
        "drop_cols": "🗑️ حذف الأعمدة",
        "reset": "🔄 إعادة ضبط البيانات",
        "convert_col": "🔄 تحويل نوع العمود",
        "column_label": "اختر العمود",
        "convert_to": "تحويل إلى",
        "convert_now": "تطبيق التحويل",
        "converted": " تم تحويله إلى ",
        "convert_section_title": "تحويل نوع البيانات",
        "cleaning_strategy": "استراتيجية التنظيف",
        "target_columns": "الأعمدة المستهدفة (فارغ = الكل)",
        "clean_now": "تطبيق التنظيف",
        "file_cleaned": "✅ تم تنظيف البيانات بنجاح!",
        "const_val": "قيمة الملء",
        "missing_treatment": "معالجة القيم المفقودة",
        "cleaning_summary": "ملخص التنظيف",
        "total_missing": "إجمالي القيم المفقودة",
        "most_missing": "العمود الأكثر فقداناً",
        "preview": "معاينة البيانات",
        "data_overview": "نظرة عامة على البيانات",
        "view_mode": "نمط العرض",
        "top_rows": "الصفوف الأولى",
        "random_sample": "عينة عشوائية",
        "full_table": "الجدول كاملاً",
        "rows_to_show": "الصفوف للعرض",
        "quick_stats": "إحصائيات سريعة",
        "num_summary": "ملخص الأعمدة الرقمية",
        "missing_summary": "ملخص القيم المفقودة",
        "no_missing": "لا توجد قيم مفقودة!",
        "show_column_info": "عرض معلومات الأعمدة",
        "no_numerical_selected": "لا توجد أعمدة رقمية محددة",
        "visualizations": "التصورات البيانية",
        "missing_data": "تحليل البيانات المفقودة",
        "numerical_analysis": "التحليل الرقمي",
        "categorical_analysis": "التحليل الفئوي",
        "advanced_analysis": "تحليلات متقدمة",
        "viz_type": "نوع التصور",
        "select_columns": "اختر الأعمدة للتصور",
        "distribution": "التوزيع",
        "box_plot": "المخطط الصندوقي",
        "correlation": "مصفوفة الارتباط",
        "value_counts": "عدد القيم",
        "top_categories": "الفئات الأولى",
        "export_title": "تصدير النتائج",
        "export_format": "صيغة التصدير",
        "final_summary": "ملخص البيانات النهائي",
        "memory_usage": "استخدام الذاكرة",
        "download_csv": "⬇️ تحميل ملف CSV",
        "download_excel": "⬇️ تحميل ملف Excel",
        "download_config": "⬇️ تحميل التكوين",
        "column_types_summary": "ملخص أنواع الأعمدة",
        "rows": "الصفوف",
        "columns": "الأعمدة",
        "missing_values": "القيم المفقودة",
        "unique_values": "القيم الفريدة",
        "data_type": "نوع البيانات",
        "no_data": "لا توجد بيانات متاحة",
        "loading": "جاري التحميل...",
        "error": "خطأ",
        "success": "نجح",
        "warning": "تحذير",
        "info": "معلومات",
        "welcome_title": "مرحباً بك في أداة تنظيف البيانات الاحترافية! 👋",
        "welcome_desc": "حوّل بياناتك الخام إلى مجموعات بيانات نظيفة وجاهزة للتحليل",
        "feature1_title": "🎯 اكتشاف ذكي للأنواع",
        "feature1_desc": "اكتشاف تلقائي للبيانات الرقمية/الفئوية مع إمكانية التعديل اليدوي",
        "feature2_title": "📊 تصورات احترافية",
        "feature2_desc": "مخططات تفاعلية مع تخطيطات جنب إلى جنب وأداء محسّن",
        "feature3_title": "🚀 ميزات متقدمة",
        "feature3_desc": "دعم متعدد اللغات، معالجة مجموعات البيانات الكبيرة، وتكوينات التصدير",
        "get_started": "ابدأ برفع ملف في الشريط الجانبي! ←",
    },
}


def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.

    Sets up default values for column types, change tracking, and other
    application state variables.
    """
    if "column_types" not in st.session_state:
        st.session_state.column_types = {}
    if "type_changes_applied" not in st.session_state:
        st.session_state.type_changes_applied = False


def setup_language_selection() -> Tuple[Dict[str, str], str]:
    """
    Set up language selection interface and return language configuration.

    Returns:
        Tuple[Dict[str, str], str]: Selected language dictionary and language key.
    """
    lang_options = {"🇺🇸 English": "English", "🇸🇦 العربية": "العربية"}
    selected_lang = st.sidebar.selectbox("🌐 Language / اللغة", list(lang_options.keys()))
    lang = lang_options[selected_lang]
    TXT = languages[lang]

    # Apply RTL for Arabic
    if lang == "العربية":
        st.markdown('<div class="rtl">', unsafe_allow_html=True)

    return TXT, lang


def render_header(TXT: Dict[str, str]) -> None:
    """
    Render the professional application header.

    Args:
        TXT: Language configuration dictionary.
    """
    st.markdown(
        f"""
    <div class="section-header">
        <h1 style="margin-bottom: 8px;">{TXT['title']}</h1>
        <p style="font-size: 1.1em; color: var(--text-muted);">{TXT['subtitle']}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_sidebar_upload(TXT: Dict[str, str]) -> Optional[Any]:
    """
    Render the file upload section in the sidebar.

    Args:
        TXT: Language configuration dictionary.

    Returns:
        Uploaded file object or None.
    """
    with st.sidebar:
        st.markdown(
            f"""
        <div style="background: linear-gradient(135deg, #0ea5e9 0%, #1d4ed8 100%); 
                    padding: 18px; border-radius: 10px; margin-bottom: 18px;">
            <h3 style="color: #e5e7eb; margin: 0;">📁 {TXT['upload']}</h3>
            <p style="color: #e5e7eb; opacity: 0.85; margin: 6px 0 0 0;">{TXT['file_types']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            TXT["upload"],
            type=["csv", "xlsx", "json", "db"],
            help=TXT["drag_drop"],
        )

        return uploaded_file


def process_uploaded_file(uploaded_file: Any, TXT: Dict[str, str]) -> bool:
    """
    Process the uploaded file and store in session state.

    Args:
        uploaded_file: Uploaded file object.
        TXT: Language configuration dictionary.

    Returns:
        bool: True if processing successful, False otherwise.
    """
    ext = uploaded_file.name.split(".")[-1].lower()

    try:
        with st.spinner(TXT["loading"]):
            if ext == "csv":
                df = file_handler.read_csv(uploaded_file)
            elif ext == "xlsx":
                df = file_handler.read_excel(uploaded_file)
            elif ext == "json":
                df = file_handler.read_json(uploaded_file)
            elif ext == "db":
                table_name = st.sidebar.text_input(TXT["table_name"])
                if not table_name:
                    st.sidebar.info("ℹ️ Please enter the table name to load data.")
                    return False
                df = file_handler.read_sqlite(uploaded_file, table_name)
            else:
                st.error(f"❌ {TXT['error']}: Unsupported file type")
                return False

            df.columns = df.columns.astype(str).str.strip().str.replace(" ", "_")

            st.session_state.df_original = df.copy()
            st.session_state.df = df

            if not st.session_state.column_types:
                st.session_state.column_types = preprocessing.detect_column_types(df)

            st.sidebar.success(TXT["file_uploaded"])
            return True

    except Exception as e:
        st.error(f"❌ {TXT['error']}: {e}")
        return False


def render_sidebar_controls(TXT: Dict[str, str], df: pd.DataFrame) -> None:
    """
    Render quick action controls in the sidebar.

    Args:
        TXT: Language configuration dictionary.
        df: Current DataFrame.
    """
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🛠️ Quick Actions")

        if st.button(f"🔄 {TXT['reset']}", use_container_width=True):
            st.session_state.df = st.session_state.df_original.copy()
            st.session_state.column_types = preprocessing.detect_column_types(st.session_state.df)
            st.success(TXT["file_reset"])
            st.rerun()

        with st.expander(TXT["drop_cols"]):
            drop_cols = st.multiselect(TXT["select_columns_drop"] + ":", df.columns)
            if drop_cols and st.button(TXT["drop_selected"], key="drop_btn"):
                st.session_state.df = st.session_state.df.drop(columns=drop_cols)
                for col in drop_cols:
                    st.session_state.column_types.pop(col, None)
                st.success(f"Dropped: {', '.join(drop_cols)}")
                st.rerun()


def render_column_types_tab(TXT: Dict[str, str], df: pd.DataFrame) -> None:
    """
    Render the column types management tab.

    Args:
        TXT: Language configuration dictionary.
        df: Current DataFrame.
    """
    st.markdown(
        f"""
    <div class="main-container">
        <h3 style="margin-top:0; color: var(--text-color);"> {TXT['column_types']} </h3>
        <p style="color: var(--text-muted);">{TXT['about']}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button(TXT["auto_detect"], use_container_width=True):
            st.session_state.column_types = preprocessing.detect_column_types(df)
            st.success("✅ Column types auto-detected!")
            st.rerun()

        st.markdown(f"#### {TXT['manual_override']}")

        with st.form("column_types_form"):
            type_changes: Dict[str, str] = {}
            num_cols = 3 if len(df.columns) > 9 else 2
            cols = st.columns(num_cols)

            for i, col in enumerate(df.columns):
                with cols[i % num_cols]:
                    current_type = st.session_state.column_types.get(col, "cat")
                    new_type = st.selectbox(
                        f"**{col}**",
                        ["num", "cat"],
                        index=0 if current_type == "num" else 1,
                        key=f"type_{col}",
                        help=f"Current: {current_type}",
                    )
                    type_changes[col] = new_type

            if st.form_submit_button(TXT["apply_types"], use_container_width=True):
                st.session_state.column_types.update(type_changes)
                st.session_state.type_changes_applied = True
                st.success("✅ Column types updated!")
                st.rerun()

    with col2:
        st.markdown(f"#### {TXT['current_distribution']}")
        num_cols = sum(1 for t in st.session_state.column_types.values() if t == "num")
        cat_cols = sum(1 for t in st.session_state.column_types.values() if t == "cat")

        st.metric(TXT["numerical"], num_cols, delta=f"{(num_cols / len(df.columns) * 100):.1f}%")
        st.metric(TXT["categorical"], cat_cols, delta=f"{(cat_cols / len(df.columns) * 100):.1f}%")

        st.markdown(f"#### {TXT['type_legend']}")
        st.info(TXT["num_desc"])
        st.info(TXT["cat_desc"])


def render_preview_tab(TXT: Dict[str, str], df: pd.DataFrame) -> None:
    """
    Render the data preview tab.

    Args:
        TXT: Language configuration dictionary.
        df: Current DataFrame.
    """
    visualization.create_data_overview_dashboard(df, st.session_state.column_types)

    st.markdown("---")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        view_mode = st.radio(
            f"🔍 {TXT['view_mode']}:",
            [TXT["top_rows"], TXT["random_sample"], TXT["full_table"]],
            horizontal=True,
        )

    with col2:
        if view_mode != TXT["full_table"]:
            n_rows = st.slider(TXT["rows_to_show"], 5, min(1000, len(df)), 20)

    with col3:
        show_info = st.checkbox(TXT["show_column_info"], value=True)

    if view_mode == TXT["top_rows"]:
        st.dataframe(df.head(n_rows), use_container_width=True, height=400)
    elif view_mode == TXT["random_sample"]:
        st.dataframe(df.sample(min(n_rows, len(df))), use_container_width=True, height=400)
    else:
        if len(df) > 5000:
            st.warning(f"⚠️ {TXT['warning']}: Large dataset may affect performance")
        st.dataframe(df, use_container_width=True, height=500)

    if show_info:
        with st.expander(f"📊 {TXT['quick_stats']}", expanded=True):
            col_l, col_r = st.columns(2)

            with col_l:
                st.markdown(f"**{TXT['num_summary']}:**")
                num_cols = [c for c, t in st.session_state.column_types.items() if t == "num" and c in df.columns]
                if num_cols:
                    st.dataframe(df[num_cols].describe(), use_container_width=True)
                else:
                    st.info(TXT["no_numerical_selected"])

            with col_r:
                st.markdown(f"**{TXT['missing_summary']}:**")
                missing_summary = preprocessing.check_missing_values(df, percent=True)
                missing_df = missing_summary[missing_summary > 0].to_frame("Missing %")
                if not missing_df.empty:
                    st.dataframe(missing_df, use_container_width=True)
                else:
                    st.success(f"✅ {TXT['no_missing']}")


def render_cleaning_tab(TXT: Dict[str, str], df: pd.DataFrame) -> None:
    """
    Render the data cleaning tab.

    Args:
        TXT: Language configuration dictionary.
        df: Current DataFrame.
    """
    st.markdown(
        f"""
    <div class="main-container">
        <h3 class="section-header">🧹 {TXT['step3']}</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(f"#### {TXT['missing_data']}")
    visualization.create_compact_missing_overview(df)

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        with st.expander(f"🔄 {TXT['convert_section_title']}", expanded=False):
            conv_col1, conv_col2, conv_col3 = st.columns(3)

            with conv_col1:
                col_to_convert = st.selectbox(TXT["column_label"], df.columns)

            with conv_col2:
                new_dtype = st.selectbox(
                    TXT["convert_to"],
                    ["str", "int", "float", "bool", "datetime"],
                )

            with conv_col3:
                st.write("")
                st.write("")
                if st.button(TXT["convert_now"], key="convert_btn", use_container_width=True):
                    try:
                        st.session_state.df = preprocessing.convert_data_type(
                            st.session_state.df, col_to_convert, new_dtype
                        )
                        st.success(f"✅ {col_to_convert}{TXT['converted']}{new_dtype}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Conversion failed: {e}")

        st.markdown(f"#### {TXT['missing_treatment']}")
        clean_col1, clean_col2, clean_col3 = st.columns(3)

        with clean_col1:
            strategy = st.selectbox(
                TXT["cleaning_strategy"],
                ["drop", "mean", "median", "mode", "constant"],
                help="Choose the best strategy for your data type",
            )

        with clean_col2:
            target_cols = st.multiselect(
                TXT["target_columns"],
                df.columns,
                default=[],
                help="Leave empty to apply to all columns",
            )

        with clean_col3:
            fill_value: Optional[Any] = None
            if strategy == "constant":
                fill_value_raw = st.text_input(TXT["const_val"])
                if fill_value_raw != "":
                    try:
                        if "." in fill_value_raw:
                            fill_value = float(fill_value_raw)
                        else:
                            fill_value = int(fill_value_raw)
                    except ValueError:
                        fill_value = fill_value_raw

            st.write("")
            if st.button(f"🧹 {TXT['clean_now']}", key="clean_btn", use_container_width=True):
                try:
                    st.session_state.df = preprocessing.process_missing_values(
                        st.session_state.df,
                        strategy=strategy,
                        columns=target_cols if target_cols else None,
                        fill_value=fill_value,
                        column_types=st.session_state.column_types,
                    )
                    st.success(f"✅ {TXT['file_cleaned']}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Cleaning failed: {e}")

    with col2:
        st.markdown(
            f"""
        <div class="main-container">
            <h4>{TXT['cleaning_summary']}</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        total_missing = df.isna().sum().sum()
        st.metric(TXT["total_missing"], f"{total_missing:,}")

        if total_missing > 0:
            most_missing_col = df.isna().sum().idxmax()
            most_missing_pct = (df.isna().sum().max() / len(df)) * 100
            st.metric(TXT["most_missing"], most_missing_col, f"{most_missing_pct:.1f}%")
        else:
            st.success(f"✅ {TXT['no_missing']}")


def render_visualizations_tab(TXT: Dict[str, str], df: pd.DataFrame) -> None:
    """
    Render the visualizations tab.

    Args:
        TXT: Language configuration dictionary.
        df: Current DataFrame.
    """
    st.markdown(
        f"""
    <div class="main-container">
        <h3 class="section-header">📊 {TXT['visualizations']}</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

    num_columns = [c for c, t in st.session_state.column_types.items() if t == "num" and c in df.columns]
    cat_columns = [c for c, t in st.session_state.column_types.items() if t == "cat" and c in df.columns]

    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs(
        [
            f"🔍 {TXT['missing_data']}",
            f"📈 {TXT['numerical_analysis']}",
            f"🏷️ {TXT['categorical_analysis']}",
            f"🧠 {TXT['advanced_analysis']}",
        ]
    )

    with viz_tab1:
        st.markdown(f"#### {TXT['missing_data']}")
        visualization.create_compact_missing_overview(df)

    with viz_tab2:
        st.markdown(f"#### {TXT['numerical_analysis']}")
        visualization.create_numerical_visualizations(df, num_columns)

    with viz_tab3:
        st.markdown(f"#### {TXT['categorical_analysis']}")
        visualization.create_categorical_visualizations(df, cat_columns)

    with viz_tab4:
        visualization.create_advanced_analysis(df, st.session_state.column_types)


def render_export_tab(TXT: Dict[str, str], df: pd.DataFrame) -> None:
    """
    Render the export tab.

    Args:
        TXT: Language configuration dictionary.
        df: Current DataFrame.
    """
    st.markdown(
        f"""
    <div class="main-container">
        <h3 class="section-header">⬇️ {TXT['export_title']}</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"#### {TXT['final_summary']}")

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            st.metric(TXT["rows"], f"{len(df):,}")
        with metric_col2:
            st.metric(TXT["columns"], f"{len(df.columns):,}")
        with metric_col3:
            st.metric(TXT["missing_values"], f"{df.isna().sum().sum():,}")
        with metric_col4:
            memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
            st.metric(TXT["memory_usage"], f"{memory_mb:.1f} MB")

        st.markdown("---")

        export_format = st.radio(f"📁 {TXT['export_format']}:", ["CSV", "Excel"], horizontal=True)

        @st.cache_data
        def generate_download_data(dataframe: pd.DataFrame, format_type: str):
            """
            Generate downloadable data buffer for CSV or Excel exports.

            Args:
                dataframe: DataFrame to export.
                format_type: 'CSV' or 'Excel'.

            Returns:
                Tuple[bytes|io.BytesIO, str, str]: data, mime type, and filename.
            """
            if format_type == "CSV":
                return dataframe.to_csv(index=False).encode("utf-8"), "text/csv", "cleaned_data.csv"
            else:
                buffer = io.BytesIO()
                dataframe.to_excel(buffer, index=False, engine="openpyxl")
                buffer.seek(0)
                return (
                    buffer,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "cleaned_data.xlsx",
                )

        data, mime_type, filename = generate_download_data(df, export_format)

        if export_format == "CSV":
            st.download_button(
                label=TXT["download_csv"],
                data=data,
                file_name=filename,
                mime=mime_type,
                use_container_width=True,
            )
        else:
            st.download_button(
                label=TXT["download_excel"],
                data=data,
                file_name=filename,
                mime=mime_type,
                use_container_width=True,
            )

    with col2:
        st.markdown(
            f"""
        <div class="main-container">
            <h4>{TXT['column_types_summary']}</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )

        type_summary = pd.DataFrame(
            {
                TXT["columns"]: list(st.session_state.column_types.keys()),
                "Type": list(st.session_state.column_types.values()),
                TXT["data_type"]: [str(df[col].dtype) for col in st.session_state.column_types.keys()],
            }
        )
        st.dataframe(type_summary, use_container_width=True, height=300)

        config_data = {
            "column_types": st.session_state.column_types,
            "original_shape": st.session_state.df_original.shape,
            "final_shape": df.shape,
            "language": TXT["title"],
        }

        config_json = pd.Series(config_data).to_json()
        st.download_button(
            label=TXT["download_config"],
            data=config_json,
            file_name="cleaning_config.json",
            mime="application/json",
            use_container_width=True,
        )


def render_welcome_screen(TXT: Dict[str, str]) -> None:
    """
    Render the welcome screen when no file is uploaded.

    Args:
        TXT: Language configuration dictionary.
    """
    st.markdown(
        f"""
    <div style="text-align: center; padding: 32px; background: var(--bg-panel); border-radius: 10px; border: 1px solid var(--border-color);">
        <h2 style="color: var(--text-color);">{TXT['welcome_title']}</h2>
        <p style="font-size: 1.1em; color: var(--text-muted);">{TXT['welcome_desc']}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    card_style = (
        "background: var(--bg-surface); padding: 24px; border-radius: 10px; "
        "box-shadow: 0 4px 10px rgba(0,0,0,0.3); height: 200px; border: 1px solid var(--border-color);"
    )

    with col1:
        st.markdown(
            f"""
        <div style="{card_style}">
            <h3 style="color: var(--info-color);">{TXT['feature1_title']}</h3>
            <p style="color: var(--text-muted);">{TXT['feature1_desc']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div style="{card_style}">
            <h3 style="color: var(--primary-color);">{TXT['feature2_title']}</h3>
            <p style="color: var(--text-muted);">{TXT['feature2_desc']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div style="{card_style}">
            <h3 style="color: var(--success-color);">{TXT['feature3_title']}</h3>
            <p style="color: var(--text-muted);">{TXT['feature3_desc']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
    <div style="text-align: center; margin-top: 28px; font-size: 1.05em; color: var(--text-muted);">
        <p>{TXT['get_started']}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """
    Main application function that orchestrates the entire Streamlit app.

    Flow:
    - Session state initialization
    - Language selection
    - File upload and processing
    - Tab navigation and rendering
    - Welcome screen for new users
    """
    initialize_session_state()
    TXT, lang = setup_language_selection()
    render_header(TXT)

    uploaded_file = render_sidebar_upload(TXT)

    if uploaded_file:
        process_uploaded_file(uploaded_file, TXT)

    if "df" in st.session_state:
        df = st.session_state.df

        if len(df) > 50_000:
            st.warning(
                f"⚠️ {TXT['warning']}: Large dataset detected ({len(df):,} rows). Some operations may be slower."
            )

        render_sidebar_controls(TXT, df)

        tab1, tab2, tab3, tab4, tab5 = st.tabs([TXT["step1"], TXT["step2"], TXT["step3"], TXT["step4"], TXT["step5"]])

        with tab1:
            render_column_types_tab(TXT, df)
        with tab2:
            render_preview_tab(TXT, df)
        with tab3:
            render_cleaning_tab(TXT, df)
        with tab4:
            render_visualizations_tab(TXT, df)
        with tab5:
            render_export_tab(TXT, df)
    else:
        render_welcome_screen(TXT)

    if lang == "العربية":
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()