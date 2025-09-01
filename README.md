# 🧼 Data Cleaning & Analysis Tool (Dark Theme)

A professional Streamlit application to upload, inspect, clean, visualize, assess data quality, and export datasets — with a cohesive dark theme, bilingual UI (English/Arabic), RTL support, pipelines (undo/redo, save/load, reapply), and modern, polished charts.

Version: 2.5.1

---

## Features

### 1) Data Ingestion
- Upload CSV, Excel, JSON, and SQLite (.db)
- SQLite table selection in sidebar
- Auto-cleaned column names (strip/replace spaces with underscores)

### 2) Column Type Management
- Smart detection of numerical (“num”) and categorical (“cat”)
- Manual override per column (persisted during session)
- Type distribution metrics and legend

### 3) Data Preview
- View modes: Top rows, Random sample, Full table
- Quick stats:
  - Numerical describe() summary
  - Missing value percentage per column
- Large dataset warning

### 4) Data Cleaning
- Missing value strategies: drop, mean, median, mode, constant
- Data type conversions: str, int, float, bool, datetime (nullable where applicable)
- Missing analysis overview:
  - Bar of missing % per column
  - Heatmap of missing pattern
- All actions recorded into the pipeline

### 5) Visualizations (Dark Theme, Consistent Colorway)
- Numerical:
  - Distribution (histogram + rug), Box plot, Correlation matrix, Summary stats
- Categorical:
  - Value counts, Top categories (metric), Distribution (pie or % bars)
- Advanced Analysis:
  - Outlier detection (IQR) with ranked bar chart
  - Scatter matrix (sampled) for multivariate exploration
  - Distribution by category (box/violin)
- Side-by-side layout for two plots; grid for many
- Unique Streamlit keys prevent duplicate element errors

### 6) Data Quality Rules + Report
- Rule builder UI:
  - Not Null, Unique, Unique across columns
  - Min/Max/Between (numeric ranges)
  - Allowed set (comma-separated)
  - Regex match
  - Dtype is (string match on dtype)
- Run checks → KPIs:
  - Pass rate (%)
  - Failed rows (unique)
  - Columns with issues
- Results table, and downloadable dark-themed HTML report
- Save/Load rules as JSON
- Pipeline step “quality_check” recorded (no-op on replay)

### 7) Pipelines (Undo/Redo, Save/Load, Reapply)
- Every data-changing action is recorded as a step with readable labels
- Undo/redo recomputes from the original dataset to avoid drift
- Save pipeline as JSON; load and reapply later (or on new datasets)
- Optional auto-reapply on upload
- Sidebar “History & Pipelines” with a single-line “( Clear History )” button

### 8) Export
- CSV, Excel, and Parquet (Snappy)
- Configuration JSON export with:
  - Pipeline steps
  - Column types (original/final shapes)
  - Language info
  - Quality rules

---

## Installation

```bash
pip install -r requirements.txt