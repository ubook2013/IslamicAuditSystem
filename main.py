import streamlit as st
import sqlite3
import pandas as pd
import random

st.set_page_config(page_title="نظام التدقيق الشرعي", layout="wide")

# تهيئة قاعدة البيانات
def get_db():
    conn = sqlite3.connect("bank_system.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Customers (name TEXT, acc TEXT PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS Contracts (acc TEXT, type TEXT, amount REAL, status TEXT, reason TEXT)")
    conn.commit()
    return conn

conn = get_db()

st.title("📊 سجل العمليات المالية والتدقيق")

if st.button("🚀 توليد بيانات (عمليات سليمة ومشبوهة)"):
    acc_num = str(random.randint(100000, 999999))
    conn.execute("INSERT OR IGNORE INTO Customers VALUES (?,?)", (f"عميل {random.randint(1,999)}", acc_num))
    
    # محرك التدقيق الشرعي الآلي
    f_type = random.choice(["مرابحة", "مضاربة", "إجارة"])
    amount = random.uniform(500, 800000)
    
    if amount > 500000 or (f_type == "مرابحة" and amount < 2000):
        status, reason = "🚨 مشتبه به", "مخالفة: غياب الأصل العيني أو صورية العقد"
    else:
        status, reason = "✅ سليم", "المعاملة متوافقة شرعياً"
        
    conn.execute("INSERT INTO Contracts VALUES (?,?,?,?,?)", (acc_num, f_type, amount, status, reason))
    conn.commit()
    st.rerun()

st.dataframe(pd.read_sql("SELECT * FROM Contracts", conn), use_container_width=True)
