import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

st.set_page_config(page_title="ECUS & MSDS ERP", layout="wide", page_icon="🚢")

# --- DATABASE INIT ---
@st.cache_resource
def init_db():
    conn = sqlite3.connect('app.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS exchange_rates (currency TEXT PRIMARY KEY, rate REAL, updated_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chemicals (cas_code TEXT, name TEXT, restriction_level TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- SIDEBAR ---
st.sidebar.markdown("### 🚢 EXIM CO. ERP (Web)")
st.sidebar.markdown("*v1.2.0 - Streamlit Edition*")

menu = st.sidebar.radio("Điều hướng", [
    "📊 Dashboard",
    "📄 Xử lý Chứng từ AI",
    "🚢 Theo dõi Logistics",
    "☁️ Hướng dẫn Deploy"
])

# --- DASHBOARD ---
if menu == "📊 Dashboard":
    st.header("📊 Dashboard Giám sát Lưu lượng")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Declarations", "42", "+12%")
    col2.metric("Chemical Risks (High)", "4", "-1", delta_color="inverse")
    col3.metric("Free Time Warnings", "8")
    col4.metric("BCQT Deadline", "74 Days")

    st.subheader("Phân luồng Hải quan")
    chart_data = pd.DataFrame({
        "Luồng": ["Xanh", "Vàng", "Đỏ"],
        "Tỷ lệ": [65, 25, 10]
    })
    st.bar_chart(chart_data.set_index("Luồng"))

# --- EXTRACT ---
elif menu == "📄 Xử lý Chứng từ AI":
    st.header("📄 Zero-Trust Document Processing")
    
    doc_type = st.selectbox("Mẫu văn bản", ["Invoice/PL", "C/O", "Bill of Lading", "Tờ khai HQ"])
    uploaded_file = st.file_uploader("Upload PDF/Docx/Excel (Max 50MB)", type=["pdf", "docx", "xlsx"])
    
    if uploaded_file:
        st.success(f"File {uploaded_file.name} uploaded an toàn.")
        st.info("Mô phỏng dữ liệu trích xuất (Trên Web cần chạy backend hoặc python packages)")
        
        df = pd.DataFrame({
            "Mô tả hàng hóa": ["Ethylene Glycol 99% Pure", "Toluene Diisocyanate (TDI)", "Polypropylene Granules"],
            "HS Code": ["2905.31.00", "2929.10.10", "3902.10.30"],
            "Mã CAS": ["107-21-1", "26471-62-5", "9003-07-0"],
            "Qty": [500, 120, 2400],
            "Risk": ["ANNEX V", "RESTRICTED", "CLEAR"]
        })
        
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Kiểm toán MSDS"):
                st.warning("Phát hiện 1 mã Hóa chất Hạn chế (RESTRICTED).")
        with col2:
            if st.button("📥 Xuất Excel ECUS"):
                st.success("Tạo file Excel thành công!")

# --- LOGISTICS ---
elif menu == "🚢 Theo dõi Logistics":
    st.header("🚢 Cảnh báo Hạn trả vỏ Container")
    
    df_cont = pd.DataFrame({
        "B/L Number": ["MSCUB1234567", "SUDU889001"],
        "Hãng tàu": ["MSC", "Maersk"],
        "Free Time": [(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")],
        "Trạng thái": ["Sắp hết hạn DEM", "An toàn"]
    })
    
    def color_status(val):
        color = 'red' if val == 'Sắp hết hạn DEM' else 'green'
        return f'color: {color}'
        
    st.dataframe(df_cont.style.applymap(color_status, subset=['Trạng thái']), use_container_width=True)

# --- DEPLOY ---
elif menu == "☁️ Hướng dẫn Deploy":
    st.header("☁️ Đưa App lên Internet (Vercel / Streamlit)")
    
    st.markdown("""
    ### 1. Dùng Streamlit Community Cloud (Phù hợp với Python)
    - Tải mã nguồn workspace này về máy, đẩy lên **GitHub**.
    - Truy cập [share.streamlit.io](https://share.streamlit.io/).
    - Kết nối với GitHub, chọn repository và chọn file **`streamlit_app.py`**.
    - Nhấn Deploy. App sẽ chạy Online hoàn toàn miễn phí.
    
    ### 2. Dùng Vercel (Phù hợp với Web React)
    - Trong workspace này, ứng dụng React (Vite) đã được viết tại `src/App.tsx`.
    - Lên **GitHub** đăng tải code.
    - Đăng nhập [Vercel](https://vercel.com/), chọn **Add New Project**.
    - Chọn repository GitHub. Vercel tự động nhận diện framework **Vite**.
    - Nhấn Deploy. Xong!
    """)
