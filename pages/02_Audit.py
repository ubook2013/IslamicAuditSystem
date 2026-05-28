import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("bank_system.db", check_same_thread=False)

st.title("⚖️ التدقيق الشرعي الرقمي")
search = st.text_input("رقم حساب العميل للبحث:")

if st.button("تحقق من العميل"):
    cust = pd.read_sql(f"SELECT * FROM Customers WHERE acc='{search}'", conn)
    cont = pd.read_sql(f"SELECT * FROM Contracts WHERE acc='{search}'", conn)
    
    if not cust.empty:
        st.write("العميل:", cust.iloc[0]['name'])
        if not cont.empty:
            st.dataframe(cont)
        else:
            st.info("لا توجد عقود مسجلة لهذا العميل.")
    else:
        st.error("العميل غير موجود.")
