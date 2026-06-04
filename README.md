# Chicago Traffic Crash Analytics

## Overview

This project provides a web-based dashboard that lets users run pre-built SQL analytical queries against a MySQL database containing Chicago traffic crash records. Results are displayed as interactive tables directly in the browser.

---

## 🛠️ Tech Stack
| Frontend / UI      | Streamlit               |
| Backend / Database | MySQL                   |
| Database Connector | mysql-connector-python  |

---

## 📁 Project Structure

```
traffic_crash_analytics_streamlit_app/
│
├── impl/
│   ├── app.py                          # Main Streamlit application
│   ├── queries.py                      # SQL queries and QUERY_MAP
│   └── data_ingestion/
│       └── load_csv_to_database.ipynb  # CSV → MySQL ingestion notebook
│
├── schema.sql                          # Database & table creation script
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/traffic_crash_analytics_streamlit_app.git
cd traffic_crash_analytics_streamlit_app
```

### 2. Install Dependencies

```bash
pip install streamlit pandas mysql-connector-python
```

### 3. Set Up the Database

Run the schema script against your MySQL instance:

```bash
mysql -u your_user -p < schema.sql
```

### 4. Ingest Data

- Download the Chicago Traffic Crashes CSV from [https://drive.google.com/file/d/1jAFsxF8ri--wYC1A-8k_Otdlf8xfcODN/view].
- Place it at `Testdata/Traffic_CrashesData.csv`.
- Open and run `impl/data_ingestion/load_csv_to_database.ipynb` in Jupyter.

### 5. Configure the Database Connection

Update the connection details in `impl/app.py`:

```python
def get_connection():
    return mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_schema"
    )
```

### 6. Run the App

```bash
cd impl
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

---

## 🗄️ Database Schema

**Database:** `traffic_data_us`  
**Table:** `Chicago_Traffic_Crashes`

## 📷 Usage

1. Launch the app with `streamlit run app.py`.
2. Select an analysis from the **dropdown menu**.
3. Click **Run Query**.
4. View the results in an interactive table with row/column counts.

## 📄 Data Source
[https://drive.google.com/file/d/1jAFsxF8ri--wYC1A-8k_Otdlf8xfcODN/view]

