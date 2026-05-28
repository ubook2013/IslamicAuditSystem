import streamlit as st
import sqlite3
from faker import Faker

st.set_page_config(page_title="ملف العميل", layout="wide")
conn = sqlite3.connect("bank_system.db", check_same_thread=False)
fake = Faker('ar_JO')

st.title("👤 ملف العميل التفصيلي")

if st.button("تسجيل عميل جديد في النظام"):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Customers (full_name, national_id, account_number, birth_date, gender, account_type, account_balance) VALUES (?,?,?,?,?,?,?)", 
                   (fake.name(), str(random.randint(1000000000, 9999999999)), str(random.randint(100000, 999999)), "1990-01-01", "ذكر", "توفير", 5000))
    conn.commit()
    st.rerun()

st.dataframe(pd.read_sql_query("SELECT * FROM Customers", conn), use_container_width=True)
