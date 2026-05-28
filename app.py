# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import random
from faker import Faker

st.set_page_config(page_title="نظام التدقيق الشرعي", layout="wide")
fake = Faker('ar_JO')

conn = sqlite3.connect("bank_system.db", check_same_thread=False)
cursor = conn.cursor()

# إنشاء الجداول
cursor.execute("""CREATE TABLE IF NOT EXISTS Customers (
    full_name TEXT, national_id TEXT PRIMARY KEY, account_number TEXT UNIQUE, 
    birth_date TEXT, gender TEXT, account_type TEXT, account_balance REAL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Contracts (
    contract_number TEXT PRIMARY KEY, account_number TEXT, finance_type TEXT, 
    contract_amount REAL, is_fraud INTEGER, violation_type TEXT, sharia_analysis TEXT)""")
conn.commit()

# دالة التدقيق
def sharia_audit_engine(f_type, amount):
    if amount > 500000: return 1, "مخالفة: غياب التمليك", "شبهة تمويل وهمي"
    if f_type == "مرابحة" and amount < 1000: return 1, "مخالفة: صورية العقد", "قيمة ضئيلة"
    return 0, "سليم", "المعاملة متوافقة شرعياً"

# الواجهة
st.title("🏦 نظام التدقيق الشرعي الرقمي")
tab1, tab2, tab3 = st.tabs(["📊 سجل العمليات", "👤 ملف العميل", "⚖️ نتائج التدقيق"])

with tab1:
    if st.button("إضافة عملية"):
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
    if st.button("تسجيل عميل جديد"):
        cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?)", 
                       (fake.name(), str(random.randint(9000000000, 9999999999)), str(random.randint(100000, 999999)), "1990-01-01", "ذكر", "توفير", random.uniform(1000, 700000)))
        conn.commit(); st.rerun()
    st.dataframe(pd.read_sql_query("SELECT * FROM Customers", conn), use_container_width=True)

with tab3:
    search = st.text_input("أدخل رقم الحساب للتدقيق:")
    if st.button("تحليل شرعي"):
        cust = pd.read_sql_query("SELECT * FROM Customers WHERE account_number = ?", conn, params=(search.strip(),))
        cont = pd.read_sql_query("SELECT * FROM Contracts WHERE account_number = ?", conn, params=(search.strip(),))
        
        if not cust.empty:
            st.table(cust)
            if not cont.empty:
                for _, row in cont.iterrows():
                    # استخدام .get لتجنب KeyError
                    f_type = row.get('finance_type', 'N/A')
                    violation = row.get('violation_type', 'غير محدد')
                    is_f = row.get('is_fraud', 0)
                    analysis = row.get('sharia_analysis', 'لا يوجد تحليل')
                    
                    color = "red" if is_f == 1 else "green"
                    st.markdown(f"---")
                    st.markdown(f"### العقد: {f_type} | الحالة: :{color}[{violation}]")
                    st.write(f"**التفسير:** {analysis}")
            else: st.warning("لا توجد عقود لهذا العميل.")
        else: st.error("رقم الحساب غير موجود.")
