import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="نظام التدقيق الشرعي", layout="wide")

# تهيئة قاعدة البيانات
conn = sqlite3.connect("bank_system.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Customers (name TEXT, acc TEXT PRIMARY KEY)")
c.execute("CREATE TABLE IF NOT EXISTS Contracts (acc TEXT, type TEXT, amount REAL, status TEXT, reason TEXT)")
conn.commit()

st.title("📊 سجل العمليات المالية")
df = pd.read_sql("SELECT * FROM Contracts", conn)
st.dataframe(df, use_container_width=True)
