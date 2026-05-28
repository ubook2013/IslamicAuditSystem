import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="نظام التدقيق الشرعي", layout="wide")

# محاولة الاتصال وإنشاء الجداول
try:
    conn = sqlite3.connect("bank_system.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Customers (full_name TEXT, national_id TEXT PRIMARY KEY, account_number TEXT UNIQUE, birth_date TEXT, gender TEXT, account_type TEXT, account_balance REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Contracts (contract_number TEXT PRIMARY KEY, account_number TEXT, finance_type TEXT, contract_amount REAL, is_fraud INTEGER, violation_type TEXT, sharia_analysis TEXT)")
    conn.commit()
    
    st.title("نظام التدقيق الشرعي")
    
    # اختبار وجود بيانات
    customers = pd.read_sql_query("SELECT * FROM Customers", conn)
    contracts = pd.read_sql_query("SELECT * FROM Contracts", conn)
    
    st.write(f"عدد العملاء: {len(customers)}")
    st.write(f"عدد العقود: {len(contracts)}")
    
    if st.button("عرض الجداول"):
        st.subheader("بيانات العملاء")
        st.dataframe(customers)
        st.subheader("العقود")
        st.dataframe(contracts)

except Exception as e:
    st.error(f"حدث خطأ: {e}")
