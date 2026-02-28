import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# --- 1. 頁面外觀設定 ---
st.set_page_config(page_title="My Vibe App", page_icon="📅")

# 隱藏 Streamlit 標記 (讓它像專業 App)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. 連結 Google Sheets ---
def get_gspread_client():
    # 設定權限範圍
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # 從 Streamlit Secrets 讀取你剛才貼的那串 TOML 鑰匙
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    return gspread.authorize(creds)

try:
    gc = get_gspread_client()
    # 這裡請確保填入你 Google Sheets 網址中那串長長的 ID
    SHEET_ID = "1OJ-3ZTCWDEEuytSmkuUdUg8tuyv37Vs_xxxxxxx" 
    sh = gc.open_by_key(SHEET_ID)
    worksheet = sh.get_worksheet(0)
except Exception as e:
    st.error(f"連線失敗，請檢查 Secrets 設定：{e}")
    st.stop()

# --- 3. 網頁介面 ---
st.title("🛡️ 永恆記憶工作站")

# 新增資料表單
with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        new_date = st.date_input("日期", date.today())
    with col2:
        new_task = st.text_input("待辦事項 (輸入完按存入)")
    
    if st.form_submit_button("存入雲端"):
        if new_task:
            # 直接寫入 Google Sheets
            worksheet.append_row([str(new_date), new_task, "未完成"])
            st.success("✅ 已同步到 Google Sheets！")
            st.rerun()

st.divider()

# 讀取並顯示資料
st.subheader("📊 雲端即時清單")
data = worksheet.get_all_records()
if data:
    df = pd.DataFrame(data)
    # 讓表格更漂亮：隱藏 index、自動填滿寬度
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.write("目前雲端尚無資料，快去新增一筆吧！")
