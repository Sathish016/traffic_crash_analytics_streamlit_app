import streamlit as st
import pandas as pd
import mysql.connector
import queries as q

def get_connection():
    return mysql.connector.connect(
        host="0.0.0.0",
        user="XXXX",
        password="XXXXXXX",
        database="XXXXXX"
    )

st.set_page_config(page_title="Traffic Crash Dashboard", layout="wide")

st.title("Chicago Traffic Crash Analytics")

selected_query = st.selectbox(
    "Choose Analysis Type",
    list(q.QUERY_MAP.keys())
)

st.write(f"### Selected: {selected_query}")

run_btn = st.button("Run Query")

if run_btn:
    try:
        conn = get_connection()

        query = q.QUERY_MAP[selected_query]

        df = pd.read_sql(query, conn)

        conn.close()

        st.success("Results fetched successfully.")

        st.dataframe(df, use_container_width=True)

        st.info(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")

    except Exception as e:
        st.error(f"Error: {e}")