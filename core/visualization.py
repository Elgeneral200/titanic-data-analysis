# core/visualization.py
"""
Data Visualization Module (Dark Theme)

Provides professional data visualization functions for data analysis including:
- Dataset overview dashboard (metrics + summaries)
- Missing value analysis
- Numerical and categorical visualizations
- Advanced analysis (outliers, scatter matrix, distribution by category)
with a cohesive, modern dark theme and consistent color system.

Author: Data Cleaning Tool Team
Version: 2.3.1
"""

from __future__ import annotations

from typing import Dict, List

import pandas as pd
import plotly.express as px
import streamlit as st

# Dark theme constants
DARK_BG_PRIMARY = "#0b1220"  # App background
DARK_BG_PANEL = "#0f172a"    # Plot area background
DARK_BG_SURFACE = "#111827"  # Paper background
TEXT_COLOR = "#e5e7eb"
GRID_COLOR = "#334155"

# Accessible, high-contrast colorway for discrete data (consistent across charts)
COLORWAY = [
    "#60a5fa",  # blue
    "#f59e0b",  # amber
    "#22c55e",  # green
    "#f472b6",  # pink
    "#a78bfa",  # violet
    "#06b6d4",  # cyan
    "#84cc16",  # lime
    "#f97316",  # orange
    "#ef4444",  # red
    "#94a3b8",  # slate
]

# Set Plotly defaults for dark theme and consistent palettes
px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = COLORWAY
px.defaults.color_continuous_scale = "Cividis"  # colorblind-friendly sequential

# Professional color accents
PROFESSIONAL_COLORS = {
    "primary": "#60a5fa",
    "secondary": "#f59e0b",
    "success": "#22c55e",
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "info": "#06b6d4",
    "purple": "#a78bfa",
    "pink": "#f472b6",
    "gray": "#94a3b8",
    "lime": "#84cc16",
}


def _apply_dark_layout(fig, height: int | None = None, hovermode: str | None = "x unified") -> None:
    """
    Apply consistent dark layout to a Plotly figure.

    Args:
        fig: Plotly figure to style.
        height: Optional figure height.
        hovermode: Hover interaction mode (default 'x unified').
    """
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=DARK_BG_SURFACE,
        plot_bgcolor=DARK_BG_PANEL,
        font=dict(color=TEXT_COLOR, size=12),
        margin=dict(l=50, r=50, t=50, b=50),
        hovermode=hovermode,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color=TEXT_COLOR),
        ),
        bargap=0.05,
    )
    if height is not None:
        fig.update_layout(height=height)
    fig.update_xaxes(
        gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR)
    )
    fig.update_yaxes(
        gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR)
    )


def _enhance_bars(fig) -> None:
    """
    Enhance bar/histogram visibility on dark background with outlines and labels.

    Applies only to valid trace types (bar, histogram) to avoid errors with other traces.

    Args:
        fig: Plotly figure.
    """
    # For bar traces: add outline, opacity, and text font color
    fig.update_traces(
        selector=dict(type="bar"),
        marker_line_color=GRID_COLOR,
        marker_line_width=1.2,
        opacity=0.95,
        textfont=dict(color=TEXT_COLOR),
    )
    # For histogram traces: add outline and opacity (no textfont on histogram)
    fig.update_traces(
        selector=dict(type="histogram"),
        marker_line_color=GRID_COLOR,
        marker_line_width=1.2,
        opacity=0.95,
    )


def create_data_overview_dashboard(df: pd.DataFrame, column_types: Dict[str, str]) -> None:
    """
    Create a professional dataset overview dashboard (dark themed).

    Shows a gradient header and key metrics (rows, columns, numerical/categorical count,
    total missing with percentage), followed by concise summaries of column types.

    Args:
        df: Input DataFrame to analyze.
        column_types: Dictionary mapping column names to 'num' or 'cat'.
    """
    st.markdown(
        """
    <div style="
        background: linear-gradient(135deg, #0ea5e9 0%, #1d4ed8 100%);
        padding: 18px; border-radius: 12px; margin-bottom: 16px;
        border: 1px solid rgba(255,255,255,0.12);">
        <h3 style="color: #e5e7eb; margin: 0;">📊 Dataset Overview</h3>
        <p style="color: #e5e7eb; opacity: 0.85; margin: 6px 0 0 0;">Comprehensive analysis of your data</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📏 Total Rows", f"{len(df):,}")
    with col2:
        st.metric("📊 Total Columns", f"{len(df.columns):,}")
    with col3:
        num_cols = sum(1 for t in column_types.values() if t == "num")
        st.metric("🔢 Numerical", f"{num_cols}")
    with col4:
        cat_cols = sum(1 for t in column_types.values() if t == "cat")
        st.metric("🏷️ Categorical", f"{cat_cols}")
    with col5:
        missing_total = int(df.isna().sum().sum())
        total_cells = int(len(df) * max(1, len(df.columns)))
        missing_pct = (missing_total / total_cells) * 100 if total_cells else 0.0
        st.metric("❓ Missing", f"{missing_total:,}", delta=f"{missing_pct:.1f}%")

    st.markdown("---")
    _display_column_type_summary(df, column_types)


def _display_column_type_summary(df: pd.DataFrame, column_types: Dict[str, str]) -> None:
    """
    Display a concise summary of numerical and categorical columns.

    Args:
        df: DataFrame to analyze.
        column_types: Mapping of columns to 'num' or 'cat'.
    """
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div style="background: #0f172a; padding: 16px; border-radius: 10px; 
                    border-left: 4px solid #60a5fa; border: 1px solid #334155;">
            <h4 style="color: #60a5fa; margin-top: 0;">🔢 Numerical Columns</h4>
        """,
            unsafe_allow_html=True,
        )
        num_columns = [c for c, t in column_types.items() if t == "num" and c in df.columns]
        if num_columns:
            for col in num_columns[:8]:
                missing_pct = (df[col].isna().sum() / len(df) * 100) if len(df) else 0.0
                unique_pct = (df[col].nunique() / len(df) * 100) if len(df) else 0.0
                st.write(f"• {col} — {missing_pct:.1f}% missing, {unique_pct:.1f}% unique")
            if len(num_columns) > 8:
                st.write(f"... and {len(num_columns) - 8} more")
        else:
            st.write("No numerical columns detected")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
        <div style="background: #0f172a; padding: 16px; border-radius: 10px; 
                    border-left: 4px solid #f59e0b; border: 1px solid #334155;">
            <h4 style="color: #f59e0b; margin-top: 0;">🏷️ Categorical Columns</h4>
        """,
            unsafe_allow_html=True,
        )
        cat_columns = [c for c, t in column_types.items() if t == "cat" and c in df.columns]
        if cat_columns:
            for col in cat_columns[:8]:
                unique_count = df[col].nunique(dropna=True)
                most_common = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
                st.write(f"• {col} — {unique_count} unique, top: {str(most_common)[:15]}")
            if len(cat_columns) > 8:
                st.write(f"... and {len(cat_columns) - 8} more")
        else:
            st.write("No categorical columns detected")
        st.markdown("</div>", unsafe_allow_html=True)


def create_compact_missing_overview(df: pd.DataFrame) -> None:
    """
    Create a compact overview of missing values in the dataset (dark theme).

    Args:
        df: Input DataFrame to analyze.
    """
    if df.empty:
        st.warning("⚠️ Cannot analyze missing values: DataFrame is empty")
        return

    missing_data = df.isna().sum()
    missing_percent = (missing_data / len(df)) * 100 if len(df) else 0.0

    if missing_data.sum() == 0:
        st.success("✅ No missing values detected in your dataset!")
        return

    col1, col2 = st.columns(2)

    with col1:
        total_missing = int(missing_data.sum())
        coverage = float((total_missing / (len(df) * len(df.columns))) * 100) if len(df.columns) else 0.0
        st.metric(label="🔍 Total Missing Values", value=f"{total_missing:,}", delta=f"{coverage:.1f}% of dataset")

        missing_cols = missing_percent[missing_percent > 0].sort_values(ascending=True)
        if len(missing_cols) > 0:
            fig = px.bar(
                x=missing_cols.values,
                y=missing_cols.index,
                orientation="h",
                title="Missing Values by Column (%)",
                color=missing_cols.values,
            )
            _enhance_bars(fig)
            _apply_dark_layout(fig, height=360)
            fig.update_xaxes(title="Missing Percentage (%)")
            fig.update_yaxes(title="Columns", categoryorder="array", categoryarray=list(missing_cols.index))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        sample_size = min(1000, len(df))
        sample_df = df.sample(sample_size) if len(df) > sample_size else df
        missing_matrix = sample_df.isna().astype(int)

        # Two-tone scale: background vs missing
        missing_scale = [(0.0, DARK_BG_PANEL), (1.0, PROFESSIONAL_COLORS["warning"])]

        fig = px.imshow(
            missing_matrix.T,
            aspect="auto",
            color_continuous_scale=missing_scale,
            title="Missing Values Pattern",
        )
        _apply_dark_layout(fig, height=360)
        fig.update_xaxes(title=f"Rows ({'sampled' if len(df) > sample_size else 'all'})")
        fig.update_yaxes(title="Columns")
        st.plotly_chart(fig, use_container_width=True)


def create_numerical_visualizations(df: pd.DataFrame, num_columns: List[str]) -> None:
    """
    Create professional visualizations for numerical columns with optimized layout.

    Args:
        df: Input DataFrame.
        num_columns: List of numerical column names to visualize.
    """
    if not num_columns:
        st.info("📊 No numerical columns available for visualization.")
        return

    col_select, viz_select = st.columns([2, 1])

    with col_select:
        selected_cols = st.multiselect(
            "📈 Select numerical columns to visualize:",
            num_columns,
            default=num_columns[: min(4, len(num_columns))],
            help="Choose up to 6 columns for optimal display",
        )

    with viz_select:
        viz_type = st.selectbox(
            "📊 Visualization Type:",
            ["Distribution", "Box Plot", "Correlation Matrix", "Summary Stats"],
            help="Choose the type of analysis",
        )

    if not selected_cols:
        st.warning("Please select at least one column to visualize.")
        return

    _create_numerical_plots(df, selected_cols, viz_type)


def _create_numerical_plots(df: pd.DataFrame, selected_cols: List[str], viz_type: str) -> None:
    """Internal function to dispatch numerical plots."""
    if viz_type == "Distribution":
        _create_distribution_plots(df, selected_cols)
    elif viz_type == "Box Plot":
        _create_box_plots(df, selected_cols)
    elif viz_type == "Correlation Matrix":
        _create_correlation_matrix(df, selected_cols)
    elif viz_type == "Summary Stats":
        _create_summary_stats(df, selected_cols)


def _create_distribution_plots(df: pd.DataFrame, selected_cols: List[str]) -> None:
    """Create distribution plots (dark themed, clear)."""
    num_plots = len(selected_cols)

    if num_plots == 1:
        fig = px.histogram(
            df,
            x=selected_cols[0],
            nbins=30,
            title=f"Distribution of {selected_cols[0]}",
            color_discrete_sequence=[PROFESSIONAL_COLORS["primary"]],
            opacity=0.9,
            marginal="rug",
        )
        _enhance_bars(fig)
        _apply_dark_layout(fig, height=360)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    elif num_plots == 2:
        col1, col2 = st.columns(2)
        for i, col in enumerate(selected_cols):
            with col1 if i == 0 else col2:
                fig = px.histogram(
                    df,
                    x=col,
                    nbins=25,
                    title=f"{col}",
                    color_discrete_sequence=[
                        PROFESSIONAL_COLORS["primary"] if i == 0 else PROFESSIONAL_COLORS["secondary"]
                    ],
                    opacity=0.9,
                )
                _enhance_bars(fig)
                _apply_dark_layout(fig, height=320)
                fig.update_layout(showlegend=False, title_font_size=12)
                st.plotly_chart(fig, use_container_width=True)
    else:
        cols = st.columns(2)
        colors = [
            PROFESSIONAL_COLORS["primary"],
            PROFESSIONAL_COLORS["secondary"],
            PROFESSIONAL_COLORS["success"],
            PROFESSIONAL_COLORS["warning"],
            PROFESSIONAL_COLORS["purple"],
            PROFESSIONAL_COLORS["pink"],
        ]
        for i, col in enumerate(selected_cols):
            with cols[i % 2]:
                fig = px.histogram(
                    df,
                    x=col,
                    nbins=20,
                    title=f"{col}",
                    color_discrete_sequence=[colors[i % len(colors)]],
                    opacity=0.9,
                )
                _enhance_bars(fig)
                _apply_dark_layout(fig, height=300)
                fig.update_layout(showlegend=False, title_font_size=11)
                st.plotly_chart(fig, use_container_width=True)


def _create_box_plots(df: pd.DataFrame, selected_cols: List[str]) -> None:
    """Create box plots (dark themed)."""
    num_plots = len(selected_cols)

    if num_plots == 1:
        fig = px.box(
            df,
            y=selected_cols[0],
            title=f"Box Plot: {selected_cols[0]}",
            color_discrete_sequence=[PROFESSIONAL_COLORS["success"]],
            points="outliers",
        )
        _apply_dark_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True)

    elif num_plots == 2:
        col1, col2 = st.columns(2)
        for i, col in enumerate(selected_cols):
            with col1 if i == 0 else col2:
                fig = px.box(
                    df,
                    y=col,
                    title=f"{col}",
                    color_discrete_sequence=[
                        PROFESSIONAL_COLORS["success"] if i == 0 else PROFESSIONAL_COLORS["warning"]
                    ],
                    points="outliers",
                )
                _apply_dark_layout(fig, height=320)
                st.plotly_chart(fig, use_container_width=True)

    else:
        df_melted = df[selected_cols].melt(var_name="Column", value_name="Value")
        fig = px.box(
            df_melted,
            x="Column",
            y="Value",
            title="Box Plots Comparison",
            color="Column",
            color_discrete_sequence=COLORWAY,
            points=False,
        )
        _apply_dark_layout(fig, height=420)
        fig.update_layout(showlegend=False)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)


def _create_correlation_matrix(df: pd.DataFrame, selected_cols: List[str]) -> None:
    """Create correlation matrix visualization (dark themed, high-contrast)."""
    if len(selected_cols) > 1:
        corr_matrix = df[selected_cols].corr(numeric_only=True)
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title="Correlation Matrix",
        )
        _apply_dark_layout(fig, height=460, hovermode=None)
        st.plotly_chart(fig, use_container_width=True)
        _display_correlation_insights(corr_matrix)
    else:
        st.warning("⚠️ Select at least 2 columns for correlation analysis.")


def _display_correlation_insights(corr_matrix: pd.DataFrame) -> None:
    """Display correlation insights in a professional layout."""
    st.markdown("#### 🔍 Correlation Insights")

    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.5:
                corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))

    if corr_pairs:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Strong Positive Correlations (>0.5):**")
            for a, b, v in sorted(corr_pairs, key=lambda x: x[2], reverse=True):
                if v > 0.5:
                    st.write(f"• {a} ↔ {b}: {v:.3f}")
        with col2:
            st.markdown("**Strong Negative Correlations (<-0.5):**")
            for a, b, v in sorted(corr_pairs, key=lambda x: x[2]):
                if v < -0.5:
                    st.write(f"• {a} ↔ {b}: {v:.3f}")
    else:
        st.info("No strong correlations (>0.5 or <-0.5) found between selected columns.")


def _create_summary_stats(df: pd.DataFrame, selected_cols: List[str]) -> None:
    """Create professional summary statistics display."""
    st.markdown("#### 📊 Statistical Summary")
    stats_df = df[selected_cols].describe()

    for col in selected_cols:
        with st.expander(f"📈 {col} Statistics", expanded=len(selected_cols) <= 2):
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.metric("Mean", f"{stats_df.loc['mean', col]:.2f}")
            with metric_cols[1]:
                st.metric("Std Dev", f"{stats_df.loc['std', col]:.2f}")
            with metric_cols[2]:
                st.metric("Min", f"{stats_df.loc['min', col]:.2f}")
            with metric_cols[3]:
                st.metric("Max", f"{stats_df.loc['max', col]:.2f}")


def create_categorical_visualizations(df: pd.DataFrame, cat_columns: List[str]) -> None:
    """
    Create professional visualizations for categorical columns with optimized layout (dark theme).

    Args:
        df: Input DataFrame containing the data.
        cat_columns: List of categorical column names to visualize.
    """
    if not cat_columns:
        st.info("🏷️ No categorical columns available for visualization.")
        return

    col_select, viz_select = st.columns([2, 1])

    with col_select:
        selected_cols = st.multiselect(
            "🏷️ Select categorical columns to visualize:",
            cat_columns,
            default=cat_columns[: min(4, len(cat_columns))],
            help="Choose columns to analyze",
        )

    with viz_select:
        viz_type = st.selectbox(
            "📊 Visualization Type:",
            ["Value Counts", "Top Categories", "Category Distribution"],
            help="Choose analysis type",
        )

    if not selected_cols:
        st.warning("Please select at least one column to visualize.")
        return

    _create_categorical_plots(df, selected_cols, viz_type)


def _create_categorical_plots(df: pd.DataFrame, selected_cols: List[str], viz_type: str) -> None:
    """Internal function to create categorical plots (dark themed)."""
    if viz_type == "Value Counts":
        _create_value_count_plots(df, selected_cols)
    elif viz_type == "Top Categories":
        _create_top_categories_display(df, selected_cols)
    elif viz_type == "Category Distribution":
        _create_category_distribution_plots(df, selected_cols)


def _create_value_count_plots(df: pd.DataFrame, selected_cols: List[str]) -> None:
    """Create value count bar charts (dark themed, labeled)."""
    num_plots = len(selected_cols)

    if num_plots == 1:
        col = selected_cols[0]
        top_values = df[col].value_counts().head(15)
        fig = px.bar(
            x=top_values.values,
            y=top_values.index,
            orientation="h",
            title=f"Value Counts: {col}",
            color=top_values.values,
        )
        fig.update_traces(text=top_values.values, textposition="outside")
        _enhance_bars(fig)
        _apply_dark_layout(fig, height=440)
        fig.update_xaxes(title="Count")
        fig.update_yaxes(title="Categories", categoryorder="total ascending")
        fig.update_layout(margin=dict(r=70))
        st.plotly_chart(fig, use_container_width=True)

    elif num_plots == 2:
        col1, col2 = st.columns(2)
        for i, col in enumerate(selected_cols):
            with col1 if i == 0 else col2:
                top_values = df[col].value_counts().head(10)
                fig = px.bar(
                    x=top_values.values,
                    y=top_values.index,
                    orientation="h",
                    title=f"{col}",
                    color_discrete_sequence=[
                        PROFESSIONAL_COLORS["primary"] if i == 0 else PROFESSIONAL_COLORS["secondary"]
                    ],
                )
                fig.update_traces(text=top_values.values, textposition="outside")
                _enhance_bars(fig)
                _apply_dark_layout(fig, height=360)
                fig.update_xaxes(title="Count")
                fig.update_yaxes(title="", categoryorder="total ascending")
                fig.update_layout(margin=dict(r=60))
                st.plotly_chart(fig, use_container_width=True)
    else:
        cols = st.columns(2)
        colors = [
            PROFESSIONAL_COLORS["primary"],
            PROFESSIONAL_COLORS["secondary"],
            PROFESSIONAL_COLORS["success"],
            PROFESSIONAL_COLORS["warning"],
        ]
        for i, col in enumerate(selected_cols):
            with cols[i % 2]:
                top_values = df[col].value_counts().head(8)
                fig = px.bar(
                    x=top_values.values,
                    y=top_values.index,
                    orientation="h",
                    title=f"{col}",
                    color_discrete_sequence=[colors[i % len(colors)]],
                )
                fig.update_traces(text=top_values.values, textposition="outside")
                _enhance_bars(fig)
                _apply_dark_layout(fig, height=320)
                fig.update_xaxes(title="Count")
                fig.update_yaxes(title="", categoryorder="total ascending")
                fig.update_layout(margin=dict(r=50))
                st.plotly_chart(fig, use_container_width=True)


def _create_top_categories_display(df: pd.DataFrame, selected_cols: List[str]) -> None:
    """Create professional metrics display for top categories (dark themed)."""
    num_cols = len(selected_cols)
    cols = st.columns(num_cols if num_cols <= 3 else 3)

    for i, col in enumerate(selected_cols):
        with cols[i % len(cols)]:
            if not df[col].empty:
                counts = df[col].value_counts()
                if counts.empty:
                    continue
                top_value = counts.index[0]
                top_count = int(counts.iloc[0])
                total = int(len(df[col].dropna()))
                percentage = (top_count / total * 100) if total else 0
                st.metric(
                    label=f"🏆 Top in {col}",
                    value=str(top_value)[:20] + "..." if len(str(top_value)) > 20 else str(top_value),
                    delta=f"{top_count:,} ({percentage:.1f}%)",
                )
                st.caption(f"Total unique: {counts.index.nunique():,}")


def _create_category_distribution_plots(df: pd.DataFrame, selected_cols: List[str]) -> None:
    """Create category distribution plots (dark themed)."""
    num_plots = len(selected_cols)

    if num_plots == 1:
        col = selected_cols[0]
        top_values = df[col].value_counts().head(8)
        fig = px.pie(
            values=top_values.values,
            names=top_values.index,
            title=f"Distribution: {col}",
            color_discrete_sequence=COLORWAY,
            hole=0.35,
        )
        _apply_dark_layout(fig, height=420)
        fig.update_traces(textinfo="percent+label", textfont=dict(color=TEXT_COLOR))
        st.plotly_chart(fig, use_container_width=True)

    elif num_plots == 2:
        col1, col2 = st.columns(2)
        for i, col in enumerate(selected_cols):
            with col1 if i == 0 else col2:
                top_values = df[col].value_counts().head(6)
                fig = px.pie(
                    values=top_values.values,
                    names=top_values.index,
                    title=f"{col}",
                    color_discrete_sequence=COLORWAY,
                    hole=0.35,
                )
                _apply_dark_layout(fig, height=360)
                fig.update_traces(textinfo="percent+label", textfont=dict(color=TEXT_COLOR))
                st.plotly_chart(fig, use_container_width=True)
    else:
        cols = st.columns(2)
        for i, col in enumerate(selected_cols):
            with cols[i % 2]:
                top_values = df[col].value_counts().head(5)
                total = int(df[col].count())
                percentages = (top_values / total * 100).round(1) if total else top_values
                fig = px.bar(
                    x=percentages.values,
                    y=percentages.index,
                    orientation="h",
                    title=f"{col} (%)",
                    color_discrete_sequence=[PROFESSIONAL_COLORS["primary"]],
                )
                fig.update_traces(text=percentages.values, textposition="outside")
                _enhance_bars(fig)
                _apply_dark_layout(fig, height=260)
                fig.update_xaxes(title="Percentage (%)")
                st.plotly_chart(fig, use_container_width=True)


def create_advanced_analysis(df: pd.DataFrame, column_types: Dict[str, str]) -> None:
    """
    Advanced exploratory analysis:
    - Outlier analysis across numerical columns
    - Scatter matrix (sampled)
    - Distribution by category comparison

    Args:
        df: Input DataFrame.
        column_types: Mapping of columns to 'num' or 'cat'.
    """
    num_cols = [c for c, t in column_types.items() if t == "num" and c in df.columns]
    cat_cols = [c for c, t in column_types.items() if t == "cat" and c in df.columns]

    # 1) Outlier analysis
    st.markdown("### 📌 Outlier Analysis (IQR method)")
    if num_cols:
        summary = []
        for c in num_cols:
            series = df[c].dropna()
            if series.empty:
                summary.append((c, 0.0, 0))
                continue
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = ((series < lower) | (series > upper)).sum()
            pct = (outliers / len(series) * 100) if len(series) else 0.0
            summary.append((c, pct, outliers))
        out_df = pd.DataFrame(summary, columns=["Column", "Outlier %", "Outlier Count"]).sort_values(
            "Outlier %", ascending=False
        )
        top_out = out_df.head(8)
        if not top_out.empty:
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.bar(
                    top_out,
                    x="Outlier %",
                    y="Column",
                    orientation="h",
                    color="Outlier %",
                    title="Top Outlier Rates by Column",
                )
                fig.update_traces(text=top_out["Outlier %"].round(1), textposition="outside")
                _enhance_bars(fig)
                _apply_dark_layout(fig, height=360)
                fig.update_layout(margin=dict(r=70))
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.dataframe(top_out, use_container_width=True, height=360)
        else:
            st.info("No numerical data to analyze outliers.")
    else:
        st.info("No numerical columns available.")

    st.markdown("---")

    # 2) Scatter matrix (sampled)
    st.markdown("### 🔬 Scatter Matrix")
    if len(num_cols) >= 2:
        sm_cols = num_cols[:5]
        sample_n = min(1000, len(df))
        sample_df = df.sample(sample_n, random_state=42) if len(df) > sample_n else df
        fig = px.scatter_matrix(sample_df, dimensions=sm_cols, color=None, title="Scatter Matrix (sampled)")
        _apply_dark_layout(fig, height=520, hovermode=None)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Need at least 2 numerical columns for a scatter matrix.")

    st.markdown("---")

    # 3) Distribution by category
    st.markdown("### 🧩 Distribution by Category")
    if num_cols and cat_cols:
        c1, c2, c3 = st.columns([1.5, 1.5, 1])
        with c1:
            num_col = st.selectbox("Numerical Column", num_cols, key="adv_num_col")
        with c2:
            cat_col = st.selectbox("Category Column", cat_cols, key="adv_cat_col")
        with c3:
            plot_mode = st.selectbox("Plot", ["Box", "Violin"], key="adv_plot_mode")

        if plot_mode == "Box":
            fig = px.box(
                df,
                x=cat_col,
                y=num_col,
                color=cat_col,
                color_discrete_sequence=COLORWAY,
                title=f"{num_col} by {cat_col}",
                points="outliers",
            )
        else:
            fig = px.violin(
                df,
                x=cat_col,
                y=num_col,
                color=cat_col,
                color_discrete_sequence=COLORWAY,
                title=f"{num_col} by {cat_col}",
                box=True,
                points=False,
            )
        _apply_dark_layout(fig, height=460)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one numerical and one categorical column to compare distributions.")


# Legacy wrappers for backward compatibility
def plot_missing_heatmap(df: pd.DataFrame) -> None:
    """Legacy function - redirects to new implementation."""
    create_compact_missing_overview(df)


def plot_missing_bar(df: pd.DataFrame) -> None:
    """Legacy function - redirects to new implementation."""
    create_compact_missing_overview(df)


def plot_correlation(df: pd.DataFrame) -> None:
    """Legacy function - redirects to new implementation."""
    num_cols = df.select_dtypes("number").columns.tolist()
    if num_cols:
        create_numerical_visualizations(df, num_cols)


def plot_distribution(df: pd.DataFrame, column: str) -> None:
    """Legacy function - redirects to new implementation."""
    if column in df.columns:
        create_numerical_visualizations(df, [column])