import streamlit as st
import sqlite3
import pandas as pd
import random
from faker import Faker

# دالة إنشاء قاعدة البيانات (تأكد من استدعائها دائماً)
def init_db():
    conn = sqlite3.connect("bank_system.db")
    cursor = conn.cursor()
    # إنشاء الجداول إذا لم تكن موجودة
    cursor.execute("""CREATE TABLE IF NOT EXISTS Customers (
        full_name TEXT, national_id TEXT PRIMARY KEY, account_number TEXT UNIQUE, 
        birth_date TEXT, gender TEXT, account_type TEXT, account_balance REAL)""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS Contracts (
        contract_number TEXT PRIMARY KEY, account_number TEXT, finance_type TEXT, 
        contract_amount REAL, is_fraud INTEGER, violation_type TEXT, sharia_analysis TEXT)""")
    conn.commit()
    return conn

# الاتصال بالقاعدة
conn = init_db()

st.title("نظام التدقيق الشرعي")

# التأكد من أن الجدول يحتوي على بيانات قبل قراءة Pandas
try:
    accs = pd.read_sql_query("SELECT account_number FROM Customers", conn)
except:
    st.error("قاعدة البيانات غير مهيأة، يرجى إعادة تشغيل التطبيق.")
    st.stop()
