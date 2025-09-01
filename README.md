# 🧼 Data Cleaning & Analysis Tool (Dark Theme)

A professional Streamlit application to upload, inspect, clean, visualize, assess data quality, and export datasets — with a cohesive dark theme, bilingual UI (English/Arabic), RTL support, pipelines (undo/redo, save/load, reapply), and modern, polished charts.

Version: 2.5.3

## Features

1) Data Ingestion
- CSV, Excel, JSON, SQLite (.db)
- SQLite table selection
- Auto-cleaned column names

2) Column Type Management
- Smart detection (num/cat)
- Manual override per column
- Type distribution metrics

3) Data Preview
- View modes: Top rows, Random sample, Full table
- Quick stats: numerical describe(), missing % per column
- Large dataset warning

4) Data Cleaning
- Missing strategies: drop, mean, median, mode, constant
- Type conversions: str, int, float, bool, datetime
- Missing overview (bar + heatmap)
- All actions recorded in pipeline

5) Visualizations (Unified Color Theme)
- Numerical: Distribution, Box Plot, Correlation Matrix, Summary Stats
- Categorical: Value Counts, Top categories, Distribution (%/pie)
- Advanced: Outliers (IQR), Scatter Matrix (sampled), Distribution by Category (box/violin)
- Side-by-side for two plots; grid for many
- Unified palette across all charts:
  - Discrete: shared COLORWAY
  - Continuous: Cividis
- Unique Streamlit keys for plots; stable keys for widget selections
- Smart sampling for heavy charts (e.g., histograms/box) to handle large datasets smoothly

6) Data Quality Rules + Report
- Rule types: Not Null, Unique, Unique across columns, Min/Max/Between, Allowed set, Regex, Dtype is
- KPIs: Pass rate, Failed rows, Columns with issues
- Details table; dark-themed HTML report
- Save/Load rule presets (JSON)
- Pipeline step “quality_check” recorded (no-op on replay)

7) Pipelines (Undo/Redo, Save/Load, Reapply)
- Record each transformation step (readable labels)
- Undo/redo recomputes from original dataset for consistency
- Save as JSON; load and reapply (optionally auto on upload)
- Sidebar “History & Pipelines” with single-line “Clear History” button (no brackets)

8) Export
- CSV, Excel, Parquet (Snappy)
- Config JSON export (pipeline, types, language, quality rules)

## Install

```bash
pip install -r requirements.txt
streamlit run app.py