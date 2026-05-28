import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="نتائج التدقيق", layout="wide")
conn = sqlite3.connect("bank_system.db", check_same_thread=False)

st.title("⚖️ نتائج التدقيق الشرعي الرقمي")
search = st.text_input("أدخل رقم الحساب:")

if st.button("تحليل"):
    cust = pd.read_sql_query("SELECT * FROM Customers WHERE account_number = ?", conn, params=(search,))
    cont = pd.read_sql_query("SELECT * FROM Contracts WHERE account_number = ?", conn, params=(search,))
    
    if not cust.empty:
        st.subheader("بيانات العميل")
        st.table(cust)
        st.subheader("أسباب التدقيق (لماذا هذا العقد مشبوه؟)")
        for _, row in cont.iterrows():
            st.error(f"العقد: {row['finance_type']}")
            st.write(f"**نوع المخالفة:** {row['violation_type']}")
            st.write(f"**التفسير الشرعي للتدقيق:** {row['sharia_analysis']}")
    else: st.error("رقم الحساب غير موجود.")
