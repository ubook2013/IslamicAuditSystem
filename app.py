# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import random
from faker import Faker

# إعداد الصفحة
st.set_page_config(page_title="نظام التدقيق الشرعي البنكي", layout="wide")
fake = Faker('ar_JO')

# إعداد قاعدة البيانات
conn = sqlite3.connect("islamic_audit_system.db", check_same_thread=False)
cursor = conn.cursor()

# إنشاء الجداول
cursor.execute("CREATE TABLE IF NOT EXISTS Customers (account_number TEXT PRIMARY KEY, full_name TEXT, residence TEXT, gender TEXT, national_id TEXT, branch TEXT, birth_date TEXT, nationality TEXT, phone TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS Islamic_Contracts (contract_number TEXT PRIMARY KEY, account_number TEXT, finance_type TEXT, supplier_name TEXT, contract_amount REAL, contract_status TEXT, is_fraud INTEGER, suspicion_reason TEXT)")
conn.commit()

# دالة كشف الاحتيال المحدثة
def detect_fraud(finance_type, amount, supplier):
    if amount > 500000:
        return 1, "المبلغ يتجاوز السقف المسموح به - مخاطر عالية"
    if finance_type == "مرابحة" and not supplier:
        return 1, "غياب بيانات المورد في عقد المرابحة - مخالفة شرعية"
    return 0, "سليم"

# تسجيل الدخول
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("تسجيل دخول الموظفين")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if user == "admin" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
else:
    tab1, tab2 = st.tabs(["لوحة المراقبة", "البحث عن عميل"])
    with tab1:
        if st.button("توليد بيانات"):
            acc = str(random.randint(100000, 999999))
            cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?,?,?)", 
                           (acc, fake.name(), fake.city(), "ذكر", "12345", "عمان", "1990-01-01", "أردني", "0790000000"))
            
            # تجنب استخدام الحروف العربية في الكود قدر الإمكان لتفادي مشاكل الترميز
            types = ["Mudaraba", "Murabaha", "Ijara"]
            f_type = random.choice(types)
            amt = random.uniform(100, 600000)
            is_fraud, reason = detect_fraud(f_type, amt, None)
            cursor.execute("INSERT OR IGNORE INTO Islamic_Contracts VALUES (?,?,?,?,?,?,?,?)", 
                           (str(random.randint(1000000, 9999999)), acc, f_type, "Supplier", amt, "Fraud" if is_fraud else "Safe", is_fraud, reason))
            conn.commit()
            st.rerun()
        df = pd.read_sql_query("SELECT * FROM Islamic_Contracts", conn)
        st.dataframe(df)
