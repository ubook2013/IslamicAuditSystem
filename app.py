import streamlit as st
import sqlite3
import pandas as pd
import random
from faker import Faker

# إعداد الصفحة
st.set_page_config(page_title="نظام التدقيق الشرعي البنكي", layout="wide")
fake = Faker('ar_JO')

# إعداد قاعدة البيانات
conn = sqlite3.connect("islamic_audit_system.db", check_same_thread=False)
cursor = conn.cursor()

# إنشاء الجداول
cursor.execute("CREATE TABLE IF NOT EXISTS Customers (account_number TEXT PRIMARY KEY, full_name TEXT, residence TEXT, gender TEXT, national_id TEXT, branch TEXT, birth_date TEXT, nationality TEXT, phone TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS Islamic_Contracts (contract_number TEXT PRIMARY KEY, account_number TEXT, finance_type TEXT, supplier_name TEXT, contract_amount REAL, contract_status TEXT, is_fraud INTEGER, suspicion_reason TEXT)")
conn.commit()

# دالة كشف الاحتيال مع التحليل المالي والشرعي
def detect_fraud(finance_type, amount, supplier):
    if amount > 500000:
        return 1, "مخالفة ضوابط التمويل: المبلغ يتجاوز سقف التمويل المسموح به مما قد يشير إلى مخاطر ائتمانية عالية أو شبهة غسيل أموال."
    if finance_type == "مرابحة" and not supplier:
        return 1, "مخالفة شرعية: بيع المرابحة يتطلب تملك السلعة وقبضها من المورد، غياب بيانات المورد يبطل التمليك الشرعي."
    if finance_type == "مضاربة" and amount < 500:
        return 1, "مخالفة مالية: انخفاض مبلغ المضاربة عن الحد الأدنى التشغيلي يجعله غير مجدٍ اقتصادياً ويثير الشبهة."
    return 0, "المعاملة سليمة وتتوافق مع الضوابط المالية والشرعية المعتمدة."

# تسجيل الدخول
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 تسجيل دخول الموظفين")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if user == "admin" and pw == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")
else:
    st.title("🏦 نظام التدقيق الشرعي البنكي")
    tab1, tab2 = st.tabs(["📊 لوحة المراقبة", "🔍 البحث عن عميل"])
    
    with tab1:
        st.subheader("إدارة العمليات المالية")
        if st.button("توليد بيانات مالية عشوائية"):
            for _ in range(5):
                acc = str(random.randint(100000, 999999))
                cursor.execute("INSERT OR IGNORE INTO Customers VALUES (?,?,?,?,?,?,?,?,?)", 
                               (acc, fake.name(), fake.city(), "ذكر", "12345", "الفرع الرئيسي", "1990-01-01", "أردني", "0790000000"))
                
                f_type = random.choice(["مضاربة", "استصناع", "مراب
