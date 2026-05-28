import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("bank_system.db", check_same_thread=False)

st.title("👤 إدارة العملاء")
with st.form("add_customer"):
    name = st.text_input("اسم العميل")
    acc = st.text_input("رقم الحساب")
    if st.form_submit_button("إضافة"):
        conn.execute("INSERT OR IGNORE INTO Customers (name, acc) VALUES (?,?)", (name, acc))
        conn.commit()
        st.success("تم إضافة العميل!")

st.dataframe(pd.read_sql("SELECT * FROM Customers", conn))
