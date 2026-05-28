# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import random
from faker import Faker

# إعداد الصفحة
st.set_page_config(page_title="نظام التدقيق الشرعي", layout="wide")
fake = Faker('ar_JO')

# إعداد قاعدة البيانات
conn = sqlite3.connect("bank_system.db", check_same_thread=False)
cursor = conn.cursor()

# إنشاء الجداول بالهيكلية المطلوبة
cursor.execute("""CREATE TABLE IF NOT EXISTS Customers (
    full_name TEXT, 
    national_id TEXT PRIMARY KEY, 
    account_number TEXT UNIQUE, 
    birth_date TEXT, 
    gender TEXT, 
    account_type TEXT, 
    account_balance REAL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Contracts (
    contract_number TEXT PRIMARY KEY, 
    account_number TEXT, 
    finance_type TEXT, 
    contract_amount REAL, 
    status TEXT,
    is_fraud INTEGER,
    reason TEXT)""")
conn.commit()

# دالة التفسير المالي والشرعي
def analyze_contract(f_type, amount):
    if amount > 500000:
        return 1, "مخالفة: المبلغ يتجاوز السقف (مخاطر غسيل أموال)."
    if f_type == "مرابحة" and amount < 1000:
        return 1, "مخالفة: قيمة المرابحة لا تغطي التكاليف التشغيلية."
    return 0, "سليم: المعاملة متوافقة مع الضوابط الشرعية."

# الواجهة
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 تسجيل دخول الموظفين")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if user == "admin" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
else:
    st.title("🏦 نظام التدقيق الشرعي البنكي")
    tab1, tab2 = st.tabs(["📊 البيانات والعملاء", "🔍 بحث تفصيلي"])

    with tab1:
        if st.button("توليد عميل وبيانات مالية"):
            acc = str(random.randint(100000, 999999))
            nat_id = str(random.randint(9000000000, 9999999999))
            # إضافة عميل
            cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?)", 
                           (fake.name(), nat_id, acc, "1990-01-01", "ذكر", "توفير", random.uniform(1000, 700000)))
            # إضافة عقد
            f_type = random.choice(["مرابحة", "مضاربة", "إجارة"])
            amt = random.uniform(500, 600000)
            is_f, res = analyze_contract(f_type, amt)
            cursor.execute("INSERT OR IGNORE INTO Contracts VALUES (?,?,?,?,?,?,?)", 
                           (str(random.randint(1000,9999)), acc, f_type, amt, "مشتبه به" if is_f else "سليم", is_f, res))
            conn.commit()
            st.rerun()
        st.subheader("قاعدة بيانات العملاء")
        st.dataframe(pd.read_sql_query("SELECT * FROM Customers", conn), use_container_width=True)

    with tab2:
        search = st.text_input("أدخل رقم الحساب:")
        if st.button("بحث"):
            cust = pd.read_sql_query("SELECT * FROM Customers WHERE account_number = ?", conn, params=(search.strip(),))
            cont = pd.read_sql_query("SELECT * FROM Contracts WHERE account_number = ?", conn, params=(search.strip(),))
            if not cust.empty:
                st.subheader("بيانات العميل")
                st.table(cust)
                st.subheader("التحليل الشرعي للعقود")
                st.dataframe(cont)
            else:
                st.error("رقم الحساب غير موجود.")
