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

# دالة كشف الاحتيال
def detect_fraud(finance_type, amount, supplier):
    if amount > 500000: return 1, "مبلغ ضخم وغير منطقي"
    if finance_type == "مرابحة" and not supplier: return 1, "عملية مرابحة بدون مورد"
    if finance_type == "مضاربة" and amount < 500: return 1, "قيمة مضاربة منخفضة"
    return 0, "لا يوجد"

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
                
                f_type = random.choice(["مضاربة", "استصناع", "مرابحة", "مشاركة", "إجارة"])
                amt = random.uniform(100, 600000)
                is_fraud, reason = detect_fraud(f_type, amt, "مورد")
                status = "مشتبه به 🚨" if is_fraud else "سليم ✅"
                
                cursor.execute("INSERT OR IGNORE INTO Islamic_Contracts VALUES (?,?,?,?,?,?,?,?)", 
                               (str(random.randint(1000000, 9999999)), acc, f_type, "مورد", amt, status, is_fraud, reason))
            
            conn.commit()
            st.success("تم إضافة البيانات بنجاح!")
            st.rerun() # هذا الأمر يضمن ظهور البيانات فوراً
            
        df = pd.read_sql_query("SELECT * FROM Islamic_Contracts", conn)
        if not df.empty:
            def style_fraud(row):
                return ['background-color: #ffcccc' if row['is_fraud'] == 1 else '' for _ in row]
            st.dataframe(df.style.apply(style_fraud, axis=1), use_container_width=True)
        else:
            st.info("لا توجد بيانات حالياً. اضغط على الزر أعلاه للبدء.")

    with tab2:
        acc_num = st.text_input("أدخل رقم الحساب للبحث:")
        if st.button("بحث"):
            cust = pd.read_sql_query(f"SELECT * FROM Customers WHERE account_number='{acc_num}'", conn)
            cont = pd.read_sql_query(f"SELECT * FROM Islamic_Contracts WHERE account_number='{acc_num}'", conn)
            if not cust.empty:
                st.subheader("👤 بيانات العميل")
                st.table(cust)
                st.subheader("📜 عقود العميل")
                st.dataframe(cont)
            else:
                st.error("رقم الحساب غير موجود")
