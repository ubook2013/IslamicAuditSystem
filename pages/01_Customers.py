import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="بيانات العملاء التفصيلية", layout="wide")

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("bank_system.db", check_same_thread=False)

st.title("👤 ملفات العملاء التفصيلية")
st.write("هنا تظهر كافة البيانات التفصيلية للعملاء المسجلين في النظام.")

# عرض البيانات التفصيلية
try:
    # استعلام لجلب كافة الأعمدة من جدول العملاء
    query = "SELECT * FROM Customers"
    df_customers = pd.read_sql(query, conn)
    
    if not df_customers.empty:
        # تحسين عرض الجدول
        st.dataframe(df_customers, use_container_width=True)
        
        # إحصائية بسيطة
        st.success(f"إجمالي عدد العملاء في النظام: {len(df_customers)}")
    else:
        st.info("لا توجد بيانات عملاء مسجلة حالياً.")
        
except Exception as e:
    st.error(f"حدث خطأ في جلب بيانات العملاء: {e}")

conn.close()
