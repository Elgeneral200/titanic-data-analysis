# 🧪 Simple Data Analysis Toolkit

A beginner-friendly, modular Python toolkit for loading, cleaning, and analyzing tabular data using **pandas** and **matplotlib**.

Built with reusability, clarity, and simplicity in mind.

---

## 🚀 Features

- 📂 Read/Write from CSV, Excel, JSON, SQLite
- 🔍 Check data types and missing value stats
- 🧼 Clean missing data (drop, fill: mean/median/mode/constant/custom map)
- 📊 Simple visualizations (missing heatmap, correlation matrix)
- 🖥️ Basic CLI demo

---

## 📁 File Structure
Data Analysis Task_1/
├── file_handler.py # I/O: CSV, JSON, Excel, SQLite
├── preprocessing.py # Clean & transform missing or typed data
├── visualization.py # Minimal plotting (matplotlib)
├── main.py # Simple CLI interface
├── requirements.txt
└── README.md

## 🚀 How to Run the Project

This project provides a simple pipeline for handling missing values in a dataset.  
You can run the script using the following commands:

### 1. Basic Run
```bash
python main.py --input train.csv