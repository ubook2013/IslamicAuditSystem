# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import random
from faker import Faker

# إعداد الصفحة
st.set_page_config(page_title="نظام التدقيق الشرعي الرقمي", layout="wide")
fake = Faker('ar_JO')

# إعداد قاعدة البيانات
conn = sqlite3.connect("bank_system.db", check_same_thread=False)
cursor = conn.cursor()

# 1. إنشاء الجداول
cursor.execute("""CREATE TABLE IF NOT EXISTS Customers (
    full_name TEXT, national_id TEXT PRIMARY KEY, account_number TEXT UNIQUE, 
    birth_date TEXT, gender TEXT, account_type TEXT, account_balance REAL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Contracts (
    contract_number TEXT PRIMARY KEY, account_number TEXT, finance_type TEXT, 
    contract_amount REAL, is_fraud INTEGER, violation_type TEXT, sharia_analysis TEXT)""")
conn.commit()

# 2. محرك التدقيق (المنطق الشرعي)
def sharia_audit_engine(f_type, amount):
    if amount > 500000: return 1, "مخالفة: غياب التمليك والقبض", "شبهة تمويل وهمي (غسيل أموال)"
    if f_type == "مرابحة" and amount < 1000: return 1, "مخالفة: صورية العقد", "قيمة ضئيلة لا تغطي التكاليف"
    return 0, "سليم", "المعاملة متوافقة مع الضوابط الشرعية"

# 3. واجهة النظام (3 صفحات)
st.title("🏦 نظام التدقيق الشرعي الرقمي للبحث العلمي")
tab1, tab2, tab3 = st.tabs(["📊 سجل العمليات المالية", "👤 ملف العميل التفصيلي", "⚖️ نتائج التدقيق الشرعي"])

with tab1:
    st.subheader("سجل العمليات الخام (للتدقيق)")
    if st.button("إضافة عملية تمويل"):
        accs = pd.read_sql_query("SELECT account_number FROM Customers", conn)
        if not accs.empty:
            acc = random.choice(accs['account_number'].tolist())
            f_type = random.choice(["مرابحة", "مضاربة", "مشاركة"])
            amt = random.uniform(500, 600000)
            is_f, viol, reason = sharia_audit_engine(f_type, amt)
            cursor.execute("INSERT OR REPLACE INTO Contracts VALUES (?,?,?,?,?,?,?)", 
                           (str(random.randint(1000,9999)), acc, f_type, amt, is_f, viol, reason))
            conn.commit(); st.rerun()
    st.dataframe(pd.read_sql_query("SELECT * FROM Contracts", conn), use_container_width=True)

with tab2:
    st.subheader("إدارة بيانات العملاء")
    if st.button("تسجيل عميل جديد"):
        cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?)", 
                       (fake.name(), str(random.randint(9000000000, 9999999999)), str(random.randint(100000, 999999)), "1990-01-01", "ذكر", "توفير", random.uniform(1000, 700000)))
        conn.commit(); st.rerun()
    st.dataframe(pd.read_sql_query("SELECT * FROM Customers", conn), use_container_width=True)

with tab3:
    st.subheader("⚖️ نظام الكشف الشرعي الآلي")
    search = st.text_input("أدخل رقم الحساب للتدقيق:")
    if st.button("تحليل شرعي"):
        cust = pd.read_sql_query("SELECT * FROM Customers WHERE account_number = ?", conn, params=(search.strip(),))
        cont = pd.read_sql_query("SELECT * FROM Contracts WHERE account_number = ?", conn, params=(search.strip(),))
        if not cust.empty:
            st.success("تم العثور على العميل")
            st.table(cust)
            if not cont.empty:
                for _, row in cont.iterrows():
                    color = "red" if row['is_fraud'] else "green"
                    st.markdown(f"---")
                    st.markdown(f"### العقد: {row['finance_type']} | الحالة: :{color}[{row['violation_type']}]")
                    st.write(f"**التفسير الشرعي:** {row['sharia_analysis']}")
            else: st.warning("لا توجد عقود مسجلة لهذا العميل.")
        else: st.error("رقم الحساب غير موجود.")
