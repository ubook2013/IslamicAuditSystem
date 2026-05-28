# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import random
from faker import Faker

# إعداد الصفحة
st.set_page_config(page_title="Islamic Audit System", layout="wide")
fake = Faker()

# إعداد قاعدة البيانات - ثابتة لا تُمسح
conn = sqlite3.connect("islamic_audit_system.db", check_same_thread=False)
cursor = conn.cursor()

# إنشاء الجداول فقط عند عدم وجودها
cursor.execute("CREATE TABLE IF NOT EXISTS Customers (account_number TEXT PRIMARY KEY, full_name TEXT, residence TEXT, gender TEXT, national_id TEXT, branch TEXT, birth_date TEXT, nationality TEXT, phone TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS Islamic_Contracts (contract_number TEXT PRIMARY KEY, account_number TEXT, finance_type TEXT, supplier_name TEXT, contract_amount REAL, contract_status TEXT, is_fraud INTEGER, suspicion_reason TEXT)")
conn.commit()

# دالة كشف الاحتيال
def detect_fraud(finance_type, amount, supplier):
    if amount > 500000:
        return 1, "High Amount - Risk of Money Laundering"
    if finance_type == "Murabaha" and supplier == "None":
        return 1, "Missing Supplier in Murabaha - Sharia Violation"
    return 0, "Compliant"

# تسجيل الدخول
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
else:
    st.title("🏦 Islamic Banking Audit System")
    tab1, tab2 = st.tabs(["📊 Dashboard", "🔍 Search Customer"])
    
    with tab1:
        st.subheader("Data Management")
        if st.button("Generate Random Data"):
            acc = str(random.randint(100000, 999999))
            cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?,?,?)", 
                           (acc, fake.name(), "Amman", "Male", "12345", "Main Branch", "1990-01-01", "Jordanian", "0790000000"))
            
            f_types = ["Mudaraba", "Murabaha", "Ijara"]
            f_type = random.choice(f_types)
            amt = random.uniform(100, 600000)
            supplier = "Supplier_A" if random.random() > 0.3 else "None"
            is_fraud, reason = detect_fraud(f_type, amt, supplier)
            
            cursor.execute("INSERT OR IGNORE INTO Islamic_Contracts VALUES (?,?,?,?,?,?,?,?)", 
                           (str(random.randint(1000000, 9999999)), acc, f_type, supplier, amt, "Fraud" if is_fraud else "Safe", is_fraud, reason))
            conn.commit()
            st.rerun()
            
        df = pd.read_sql_query("SELECT * FROM Islamic_Contracts", conn)
        st.dataframe(df, use_container_width=True)

    with tab2:
        acc_num = st.text_input("Enter Account Number:")
        if st.button("Search"):
            cust = pd.read_sql_query(f"SELECT * FROM Customers WHERE account_number='{acc_num}'", conn)
            cont = pd.read_sql_query(f"SELECT * FROM Islamic_Contracts WHERE account_number='{acc_num}'", conn)
            if not cust.empty:
                st.subheader("Customer Info")
                st.table(cust)
                st.subheader("Contracts Analysis")
                st.dataframe(cont)
            else:
                st.error("Account number not found. Make sure you generated data first.")
