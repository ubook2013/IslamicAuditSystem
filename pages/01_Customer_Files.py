import streamlit as st
import sqlite3
import pandas as pd
from faker import Faker

st.set_page_config(page_title="ملف العميل", layout="wide")
conn = sqlite3.connect("bank_system.db", check_same_thread=False)

st.title("👤 ملف العميل التفصيلي")
if st.button("تسجيل عميل جديد"):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?)", 
                   (Faker('ar_JO').name(), "123", "999", "1990", "ذكر", "توفير", 1000))
    conn.commit(); st.rerun()

st.dataframe(pd.read_sql_query("SELECT * FROM Customers", conn), use_container_width=True)
