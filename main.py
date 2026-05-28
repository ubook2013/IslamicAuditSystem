import streamlit as st
import sqlite3
import pandas as pd
import random

st.set_page_config(page_title="نظام التدقيق الشرعي", layout="wide")

# تهيئة قاعدة البيانات
conn = sqlite3.connect("bank_system.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Customers (name TEXT, acc TEXT PRIMARY KEY)")
c.execute("CREATE TABLE IF NOT EXISTS Contracts (acc TEXT, type TEXT, amount REAL, status TEXT, reason TEXT)")
conn.commit()

st.title("📊 سجل العمليات المالية")

# محرك توليد البيانات
if st.button("🚀 توليد بيانات وعقود عشوائية"):
    # توليد عميل
    acc_num = str(random.randint(100000, 999999))
    c.execute("INSERT OR IGNORE INTO Customers VALUES (?,?)", (f"عميل {random.randint(1,100)}", acc_num))
    # توليد عقد مشتبه به
    c.execute("INSERT INTO Contracts VALUES (?,?,?,?,?)", 
              (acc_num, random.choice(["مرابحة", "مضاربة"]), random.uniform(1000, 700000), "مشتبه به", "شبهة صورية العقد"))
    conn.commit()
    st.rerun()

st.subheader("سجل العمليات الخام")
df = pd.read_sql("SELECT * FROM Contracts", conn)
st.dataframe(df, use_container_width=True)
