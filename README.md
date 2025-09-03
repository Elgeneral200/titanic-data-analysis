# 🧼 Data Cleaning & Analysis Tool (Dark Theme)

A professional **Streamlit** application designed for seamless **data ingestion, inspection, cleaning, visualization, quality assessment, and export of datasets**.  

Featuring:  
- Cohesive **dark theme**  
- Bilingual UI (**English/Arabic**) with RTL support  
- Transformation pipelines (**undo/redo, save/load, reapply**)  
- Modern, polished charts  

**Version:** 2.5.3  

---

## 📑 Table of Contents
1. [Introduction](#-introduction)  
2. [Features](#-features)  
3. [Installation](#-installation)  
4. [Usage](#-usage)  
5. [Examples](#-examples)  
6. [Contribution](#-contribution)  
7. [License](#-license)  

---

## 📝 Introduction
This tool is built to **simplify and streamline** the process of data cleaning and analysis through an intuitive interface that supports **multiple file formats and databases**.  

It offers smart automation alongside manual controls to accommodate various skill levels, ensuring **high data quality and insightful visualizations** — all within a responsive, visually appealing **dark-themed UI**.  

---

## ⚡ Features

### 1) Data Ingestion
- **What it does:** Supports uploading CSV, Excel, JSON, and importing from SQLite (`.db`) with table selection.  
- **Why it matters:** Flexibility to bring data from diverse sources without format barriers.  
- **How to use:**  
  - Click **Upload** and select a file.  
  - For SQLite, choose the target table.  
  - Column names are auto-cleaned for consistency.  

---

### 2) Column Type Management
- **What it does:** Auto-detects column types (numerical, categorical), allows manual overrides, and shows type distribution.  
- **Why it matters:** Correct data types = accurate analysis & visualizations.  
- **How to use:**  
  - Review detected types.  
  - Override manually if necessary.  

---

### 3) Data Preview
- **What it does:** Offers views (top rows, random samples, full table) + quick stats & missing data %.  
- **Why it matters:** Quick understanding of dataset structure & quality.  
- **How to use:**  
  - Select preview mode.  
  - Inspect stats & missing values.  

---

### 4) Data Cleaning
- **What it does:** Missing data handling (drop, fill with mean/median/mode/constant), type conversions, and visualizations (bar charts, heatmaps).  
- **Why it matters:** Clean data = valid & reliable results.  
- **How to use:**  
  - Pick missing data strategy.  
  - Apply type conversions.  
  - Monitor changes in the pipeline (undo/redo supported).  

---

### 5) Visualizations
- **What it does:** Unified dark-theme charts: distribution, box plots, correlation, value counts, pie charts, scatter matrices, outlier detection.  
- **Why it matters:** Visual insights aid better interpretation.  
- **How to use:**  
  - Choose visualization type from sidebar.  
  - Customize params if needed.  

---

### 6) Data Quality Rules + Report
- **What it does:** Define rules (non-null, uniqueness, ranges), track pass/fail KPIs, generate HTML reports.  
- **Why it matters:** Detect anomalies & ensure high-quality data.  
- **How to use:**  
  - Define rules & save presets.  
  - Run checks & generate reports.  

---

### 7) Pipelines (Undo/Redo, Save/Load, Reapply)
- **What it does:** Records every transformation step; supports undo/redo, saving/loading pipelines.  
- **Why it matters:** Enhances reproducibility & flexibility.  
- **How to use:**  
  - Steps are auto-recorded.  
  - Undo/redo anytime.  
  - Save/load pipelines as JSON.  

---

### 8) Export
- **What it does:** Export cleaned data in CSV, Excel, Parquet (Snappy), and JSON (pipelines).  
- **Why it matters:** Easy sharing & reusability.  
- **How to use:**  
  - Click **Export** and choose format.  

---

## ⚙️ Installation
Make sure **Python** & **pip** are installed.  

```bash
pip install -r requirements.txt
streamlit run app.py
