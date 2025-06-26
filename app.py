import streamlit as st
import pandas as pd
from supabase import create_client, Client
from io import BytesIO

# --- ตั้งค่า Supabase ---
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- ชื่อ Table ใน Supabase ---
TABLE_NAME = "budgets"

# --- ตั้งค่า Layout ---
st.set_page_config(page_title="📊 งบประมาณ 61-68", layout="wide")
st.title("📊 ระบบกรองข้อมูลงบประมาณ ปี 2561-2568")

# --- ดึงข้อมูลจาก Supabase ---
@st.cache_data(show_spinner=True)
def load_data():
    response = supabase.table(TABLE_NAME).select("*").execute()
    return pd.DataFrame(response.data)

# --- โหลดข้อมูล ---
df = load_data()

# --- ตรวจสอบคอลัมน์ที่ต้องมี ---
required_columns = ["ลำดับ", "โครงการ", "รูปแบบงบประมาณ", "ปีงบประมาณ", "หน่วยงาน", "สถานที่", "หมู่ที่", "ตำบล", "อำเภอ", "จังหวัด"]
if not all(col in df.columns for col in required_columns):
    st.error("❌ ข้อมูลไม่ครบหรือชื่อคอลัมน์ไม่ตรง")
    st.stop()

# --- Dropdown Filters ---
def get_options(df, col):
    opts = sorted(df[col].dropna().unique().astype(str).tolist())
    return ["ทั้งหมด"] + opts

col1, col2, col3 = st.columns(3)
with col1:
    selected_budget = st.selectbox("💰 รูปแบบงบประมาณ", get_options(df, "รูปแบบงบประมาณ"))
with col2:
    selected_year = st.selectbox("📅 ปีงบประมาณ", get_options(df, "ปีงบประมาณ"))
with col3:
    selected_project = st.selectbox("📌 โครงการ", get_options(df, "โครงการ"))

# --- Filtered View ---
filtered_df = df.copy()
if selected_budget != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["รูปแบบงบประมาณ"] == selected_budget]
if selected_year != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["ปีงบประมาณ"].astype(str) == selected_year]
if selected_project != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["โครงการ"] == selected_project]

# --- แสดงผลลัพธ์ ---
if not filtered_df.empty:
    st.markdown(f"<div style='font-size:24px; color:#3178c6; background-color:#d0e7ff; padding:10px; border-radius:6px;'>\n        📈 พบข้อมูลทั้งหมด {len(filtered_df)} รายการ</div>", unsafe_allow_html=True)
else:
    st.warning("⚠️ ไม่พบข้อมูลที่ตรงกับเงื่อนไขที่เลือก")

st.dataframe(filtered_df, use_container_width=True)

# --- ดาวน์โหลดข้อมูลเป็น Excel ---
def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

col_left, spacer, col_right = st.columns([1, 2, 1])

with col_left:
    st.markdown("#### 📤 อัปโหลด Excel เพื่อเพิ่มข้อมูลเข้า Supabase")
    uploaded_file = st.file_uploader("เลือกไฟล์ Excel", type=["xlsx"])
    if uploaded_file:
        try:
            uploaded_df = pd.read_excel(uploaded_file)
            missing = [col for col in required_columns if col not in uploaded_df.columns]
            if missing:
                st.error(f"❌ คอลัมน์หายไป: {', '.join(missing)}")
            else:
                data_to_insert = uploaded_df[required_columns].to_dict(orient="records")
                supabase.table(TABLE_NAME).insert(data_to_insert).execute()
                st.success(f"✅ เพิ่มข้อมูล {len(data_to_insert)} แถวเรียบร้อยแล้ว")
                st.cache_data.clear()
                st.rerun()
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

with col_right:
    if not filtered_df.empty:
        st.download_button(
            label="📥 ดาวน์โหลดข้อมูลที่กรองเป็น Excel",
            data=to_excel_bytes(filtered_df),
            file_name="filtered_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
