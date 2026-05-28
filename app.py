import streamlit as st
import sqlite3
import pandas as pd
import random

st.set_page_config(page_title="نظام التدقيق الشرعي", layout="wide")

# الاتصال بقاعدة البيانات الثابتة
def get_connection():
    return sqlite3.connect("bank_system.db", check_same_thread=False)

st.title("📊 سجل العمليات المالية والتدقيق")

# زر توليد بيانات تجريبية فورية
if st.button("توليد عملية مالية جديدة"):
    conn = get_connection()
    cursor = conn.cursor()
    # جلب حساب موجود
    accs = pd.read_sql_query("SELECT account_number FROM Customers", conn)
    if not accs.empty:
        acc = random.choice(accs['account_number'].tolist())
        # إدخال عملية عشوائية
        cursor.execute("INSERT OR REPLACE INTO Contracts (contract_number, account_number, finance_type, contract_amount, is_fraud, violation_type, sharia_analysis) VALUES (?,?,?,?,?,?,?)", 
                       (str(random.randint(1000,9999)), acc, random.choice(["مرابحة", "مضاربة", "إجارة"]), 
                        random.uniform(500, 600000), 1, "مخالفة غياب تمليك", "شبهة تمويل وهمي لعدم وجود أصل عيني"))
        conn.commit()
        st.success("تم إضافة عملية جديدة!")
    else:
        st.warning("يرجى إضافة عملاء أولاً في صفحة (ملف العميل).")

# عرض السجل
conn = get_connection()
st.dataframe(pd.read_sql_query("SELECT * FROM Contracts", conn), use_container_width=True)
