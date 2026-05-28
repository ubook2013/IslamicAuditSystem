import streamlit as st
import sqlite3
import pandas as pd
import random
from faker import Faker

st.set_page_config(page_title="سجل العمليات", layout="wide")
conn = sqlite3.connect("bank_system.db", check_same_thread=False)

st.title("📊 سجل العمليات المالية")
if st.button("توليد عملية مالية"):
    accs = pd.read_sql_query("SELECT account_number FROM Customers", conn)
    if not accs.empty:
        acc = random.choice(accs['account_number'].tolist())
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO Contracts VALUES (?,?,?,?,?,?,?)", 
                       (str(random.randint(1000,9999)), acc, "مرابحة", 600000, 1, "مخالفة غياب تمليك", "شبهة غسيل أموال"))
        conn.commit(); st.rerun()

st.dataframe(pd.read_sql_query("SELECT * FROM Contracts", conn), use_container_width=True)
