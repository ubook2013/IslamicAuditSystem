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

# إنشاء جداول منفصلة (بيانات العملاء | العمليات المالية للتدقيق)
cursor.execute("""CREATE TABLE IF NOT EXISTS Customers (
    full_name TEXT, national_id TEXT PRIMARY KEY, account_number TEXT UNIQUE, 
    birth_date TEXT, gender TEXT, account_type TEXT, account_balance REAL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Contracts (
    contract_number TEXT PRIMARY KEY, account_number TEXT, finance_type TEXT, 
    contract_amount REAL, status TEXT, is_fraud INTEGER, reason TEXT)""")
conn.commit()

# دالة التحليل
def analyze(f_type, amount):
    if amount > 500000: return 1, "مخالفة: المبلغ يتجاوز سقف التمويل (غسيل أموال)."
    if f_type == "مرابحة" and amount < 1000: return 1, "مخالفة: العملية غير مجدية اقتصادياً."
    return 0, "سليم: متوافق شرعياً."

# تسجيل الدخول
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.title("🔐 تسجيل دخول المدقق الشرعي")
    if st.text_input("كلمة المرور", type="password") == "1234":
        if st.button("دخول"): st.session_state.logged_in = True; st.rerun()
else:
    st.title("🏦 نظام التدقيق الشرعي والمالي")
    tab1, tab2 = st.tabs(["📊 سجل العمليات (للتدقيق)", "🔍 ملف العميل التفصيلي"])

    with tab1:
        if st.button("إضافة عملية تمويل جديدة (للعملاء الموجودين)"):
            # جلب حساب عشوائي موجود
            existing_accs = pd.read_sql_query("SELECT account_number FROM Customers", conn)
            if not existing_accs.empty:
                acc = random.choice(existing_accs['account_number'].tolist())
                f_type = random.choice(["مرابحة", "مضاربة", "مشاركة", "استصناع", "إجارة"])
                amt = random.uniform(500, 600000)
                is_f, res = analyze(f_type, amt)
                cursor.execute("INSERT OR REPLACE INTO Contracts VALUES (?,?,?,?,?,?,?)", 
                               (str(random.randint(1000,9999)), acc, f_type, amt, "مشتبه به 🚨" if is_f else "سليم ✅", is_f, res))
                conn.commit(); st.rerun()
            else: st.warning("قم بإنشاء عميل أولاً من صفحة البحث.")
        
        st.subheader("سجل العمليات المالية")
        st.dataframe(pd.read_sql_query("SELECT * FROM Contracts", conn), use_container_width=True)

    with tab2:
        st.subheader("إدارة بيانات العملاء")
        # زر لإضافة عميل جديد لأول مرة
        if st.button("تسجيل عميل جديد في النظام"):
            acc = str(random.randint(100000, 999999))
            cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?)", 
                           (fake.name(), str(random.randint(9000000000, 9999999999)), acc, "1990-01-01", "ذكر", "توفير", random.uniform(1000, 700000)))
            conn.commit(); st.rerun()
            
        search = st.text_input("بحث برقم الحساب:")
        if st.button("عرض ملف العميل"):
            cust = pd.read_sql_query("SELECT * FROM Customers WHERE account_number = ?", conn, params=(search.strip(),))
            cont = pd.read_sql_query("SELECT * FROM Contracts WHERE account_number = ?", conn, params=(search.strip(),))
            if not cust.empty:
                st.subheader("👤 بيانات العميل الشخصية")
                st.table(cust)
                st.subheader("📜 التاريخ المالي والتدقيق")
                st.dataframe(cont)
            else: st.error("رقم الحساب غير موجود.")
