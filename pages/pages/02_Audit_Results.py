import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="نتائج التدقيق", layout="wide")
conn = sqlite3.connect("bank_system.db", check_same_thread=False)

st.title("⚖️ نتائج التدقيق الشرعي الرقمي")
search = st.text_input("أدخل رقم الحساب للتحليل:")

if st.button("تحليل شرعي متقدم"):
    cust = pd.read_sql_query("SELECT * FROM Customers WHERE account_number = ?", conn, params=(search.strip(),))
    cont = pd.read_sql_query("SELECT * FROM Contracts WHERE account_number = ?", conn, params=(search.strip(),))
    
    if not cust.empty:
        st.subheader("بيانات العميل الشخصية")
        st.table(cust)
        if not cont.empty:
            st.subheader("نتائج التحليل الشرعي")
            for _, row in cont.iterrows():
                with st.expander(f"عقد رقم: {row['contract_number']} - حالة التدقيق: {'🚨 مشتبه به' if row['is_fraud'] else '✅ سليم'}"):
                    st.write(f"**نوع العقد:** {row['finance_type']}")
                    st.write(f"**المخالفة المكتشفة:** {row['violation_type']}")
                    st.info(f"**التحليل الشرعي:** {row['sharia_analysis']}")
        else: st.warning("لا توجد عقود مرتبطة بهذا العميل.")
    else: st.error("رقم الحساب غير موجود في قاعدة البيانات.")
