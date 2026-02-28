import streamlit as st
import pandas as pd
import os
from datetime import date
import calendar

st.set_page_config(page_title="Mobile Vibe Calendar", page_icon="📱")

# --- 檔案儲存設定 ---
DATA_FILE = "todo_data.csv"

# 讀取現有資料
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df['日期'] = pd.to_datetime(df['日期']).dt.date
else:
    df = pd.DataFrame(columns=["日期", "事項", "狀態"])

st.title("📱 我的行動工作站")

# --- 新增功能 ---
with st.expander("➕ 新增事項"):
    with st.form("todo_form", clear_on_submit=True):
        input_date = st.date_input("選擇日期", date.today())
        task = st.text_input("要做什麼？")
        if st.form_submit_button("同步到雲端"):
            new_row = pd.DataFrame([[input_date, task, "未完成"]], columns=["日期", "事項", "狀態"])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("已同步！")
            st.rerun()

# --- 顯示清單 ---
st.subheader("📅 待辦行程")
st.dataframe(df.sort_values("日期"), use_container_width=True, hide_index=True)

if st.button("清空所有紀錄"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        st.rerun()