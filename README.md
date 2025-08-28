
# 🧼 Interactive Data Cleaning & Analysis Tool

A multilingual, high-performance web app for non-coders and data professionals to **clean, explore, and export datasets** — all with a click.

---

## 🚀 Key Features

- 📂 Upload datasets in CSV, Excel, JSON, or SQLite
- 🌍 Fully Multilingual UI (English & Arabic)
- 🧼 Fill missing values with drop, mean, median, mode, or constant
- 🔄 Convert column types (string, float, int, bool)
- 🧺 Drop columns pre-cleaning
- 📈 Descriptive stats of all numeric columns
- 📊 Visualize missing data (heatmap, bar chart)
- 📌 View numeric column distributions
- 🔗 Correlation analysis heatmap
- ⚡ Optimized for large datasets (50k+ rows)
- 🔍 Choose between top rows, full table, or paginated preview
- 💾 Download cleaned datasets in CSV or Excel

---

## 📁 Project Structure

```
interactive_data_tool/
├── app.py                         # Main Streamlit app
├── core/
│   ├── file_handler.py            # Load/save files
│   ├── preprocessing.py           # Cleaning logic
│   ├── visualization.py           # Plotting (heatmaps, bars, dists)
├── requirements.txt               # Python dependencies
└── README.md
```

---

## 📦 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/interactive-data-cleaner.git
cd interactive-data-cleaner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Getting Started

```bash
streamlit run app.py
```

- The app will open in your browser
- Navigate through steps in the sidebar to upload, clean, and export your dataset

---

## 🧭 Available Steps in the UI

1. 📁 **Upload File**: CSV, Excel (`.xlsx`), JSON, or SQLite
2. 🧺 **Drop / Convert / Clean**: Drop columns, change data types, handle null values
3. 🔍 **Preview & Visualize**:
   - Different preview modes (top N, full, paginated)
   - Missing value summary, bar charts
   - Heatmaps, distributions, correlation
4. 📥 **Download Cleaned File**

---

## 🌐 Supported Languages

- ✅ English (default)
- ✅ Arabic (full translation)

You can expand the `languages` dictionary in `app.py` to add French, Spanish, etc.

---

## ⚙️ Requirements

```
streamlit==1.35.0
pandas==2.2.2
matplotlib==3.8.4
seaborn==0.13.2
plotly==5.22.0
openpyxl==3.1.2
```

---

## 🛰 Deployment

### ▶️ Deploy to [Streamlit Cloud](https://share.streamlit.io)

1. Push this repo to GitHub  
2. Go to Streamlit Cloud  
3. Select your repo > set `app.py` as main file  
4. Done! Public or invite-only access supported

---

### 🐳 Optional Docker Deployment

```
FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 📌 Example Use Cases

- Internal team tools for cleaning messy CSVs
- Help non-technical users clean + preview datasets
- Pre-clean before ML pipelines
- Teaching data cleaning in classrooms

---

## 🛣 Future Features

- [ ] Column renaming
- [ ] Save/load cleaning profiles
- [ ] Add French, Spanish, etc.
- [ ] Pandas-profiling reporting
- [ ] Secure login for private datasets

---

## 👤 Author

**Your Name**  : Muhammad Fathi Kamal 
[LinkedIn](www.linkedin.com/in/muhammad-fathi-526745287)  


---

## 📄 License

MIT License – free to use, extend, and share!

---

## ⭐ Found this helpful?

Give it a star ⭐ on GitHub — or connect with me on LinkedIn!
```

---

## ✅ How to Use This

- Paste into a new file in your repo: `README.md`
- Replace:
  - `yourusername` with your GitHub username
  - Your email + LinkedIn
  - Optional features with checkmarks if done
- Add screenshots or GIFs to show the tool in action (recommended!)

---