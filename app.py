import streamlit as st
import pandas as pd
import re
from io import BytesIO
from supabase import create_client, Client

import streamlit as st
import time

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="User Login",
    page_icon="👤",
    layout="centered"
)

# CSS สำหรับจัดแต่งหน้าตา
st.markdown("""
<style>
    /* พื้นหลังแบบ gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* ซ่อน header และ footer ของ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* สไตล์สำหรับกล่อง login */
    .login-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 2rem auto;
    }
    
    /* สไตล์สำหรับไอคอนผู้ใช้ */
    .user-icon {
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .user-icon-circle {
        width: 80px;
        height: 80px;
        background-color: #4a5568;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    /* สไตล์สำหรับหัวข้อ */
    .login-title {
        text-align: center;
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    /* สไตล์สำหรับ input fields */
    .stTextInput > div > div > input {
        border-radius: 5px;
        border: 1px solid #e2e8f0;
        padding: 0.75rem;
    }
    
    /* สไตล์สำหรับปุ่ม login */
    .login-button {
        width: 100%;
        background-color: #4299e1;
        color: white;
        padding: 0.75rem;
        border: none;
        border-radius: 5px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        margin-top: 1rem;
    }
    
    .login-button:hover {
        background-color: #3182ce;
    }
    
    /* สไตล์สำหรับลิงก์ Forgot Password */
    .forgot-password {
        text-align: center;
        margin-top: 1rem;
    }
    
    .forgot-password a {
        color: #a0aec0;
        text-decoration: none;
        font-size: 0.9rem;
    }
    
    .forgot-password a:hover {
        color: #4299e1;
    }
</style>
""", unsafe_allow_html=True)

# ฟังก์ชันตรวจสอบการ login
def authenticate(username, password):
    # ใส่ logic การตรวจสอบผู้ใช้ที่นี่
    # ตัวอย่างนี้ใช้ username: admin, password: password123
    return username == "admin" and password == "password123"

# สร้าง session state สำหรับเก็บสถานะ login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# หากล็อกอินสำเร็จแล้ว
if st.session_state.logged_in:
    st.success("🎉 เข้าสู่ระบบสำเร็จ!")
    st.write("ยินดีต้อนรับเข้าสู่ระบบ!")
    
    if st.button("ออกจากระบบ"):
        st.session_state.logged_in = False
        st.rerun()
else:
    # สร้างหน้า login
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # ไอคอนผู้ใช้
    st.markdown("""
    <div class="user-icon">
        <div class="user-icon-circle">
            <svg width="40" height="40" fill="white" viewBox="0 0 24 24">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # หัวข้อ
    st.markdown('<h2 class="login-title">User Login</h2>', unsafe_allow_html=True)
    
    # ฟอร์ม login
    with st.form("login_form"):
        username = st.text_input(
            "Username", 
            placeholder="Username",
            label_visibility="collapsed"
        )
        
        password = st.text_input(
            "Password", 
            type="password",
            placeholder="••••••",
            label_visibility="collapsed"
        )
        
        # ปุ่ม login
        login_clicked = st.form_submit_button("Log In", use_container_width=True)
        
        if login_clicked:
            if username and password:
                if authenticate(username, password):
                    st.session_state.logged_in = True
                    st.success("เข้าสู่ระบบสำเร็จ!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            else:
                st.error("กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
    
    # ลิงก์ Forgot Password
    st.markdown("""
    <div class="forgot-password">
        <a href="#" onclick="alert('ติดต่อผู้ดูแลระบบเพื่อรีเซ็ตรหัสผ่าน')">Forgot Password?</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # แสดงข้อมูล demo
    st.markdown("---")
    st.info("**Demo Account:**\n- Username: admin\n- Password: password123")

# --- Custom CSS ---
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        margin: 1rem;
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Filter cards */
    .filter-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.18);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    
    /* Results card */
    .results-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: linear-gradient(90deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.7);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255,107,107,0.4);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,107,107,0.6);
    }
    
    /* Upload section */
    .upload-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
    }
    
    .upload-section .stFileUploader {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        backdrop-filter: blur(5px);
    }
    
    /* Warning and success messages */
    .stAlert {
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Plotly chart container */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Emoji enhancement */
    .emoji-large {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Card hover effects */
    .hover-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .hover-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Excel Filter App - Supabase", layout="wide", page_icon="📊")

# Custom title with styling
st.markdown('<h1 class="main-title">📊 ข้อมูล - งบประมาณ ปี 2561-2568 จาก Supabase</h1>', unsafe_allow_html=True)

# --- เชื่อมต่อ Supabase ---
SUPABASE_URL = st.secrets["supabase_url"]
SUPABASE_KEY = st.secrets["supabase_key"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "budgets"

# --- โหลดข้อมูลจาก Supabase ---
@st.cache_data(ttl=0, show_spinner="📡 กำลังโหลดข้อมูลจาก Supabase...")
def load_data():
    page_size = 1000
    offset = 0
    all_data = []

    while True:
        response = supabase.table(TABLE_NAME).select("*").range(offset, offset + page_size - 1).execute()
        batch = response.data
        if not batch:
            break
        all_data.extend(batch)
        if len(batch) < page_size:
            break
        offset += page_size

    return pd.DataFrame(all_data)

# Loading animation
with st.spinner('🎨 กำลังโหลดข้อมูล...'):
    df = load_data()

# --- ตรวจสอบคอลัมน์ ---
required_columns = ["ลำดับ", "โครงการ", "รูปแบบงบประมาณ", "ปีงบประมาณ", "หน่วยงาน",
                    "สถานที่", "หมู่ที่", "ตำบล", "อำเภอ", "จังหวัด"]
if not all(col in df.columns for col in required_columns):
    st.error("❌ ตาราง Supabase ไม่มีคอลัมน์ที่ต้องการ หรือชื่อคอลัมน์ไม่ถูกต้อง")
    st.stop()

# --- ฟังก์ชัน ---
def extract_number(s):
    match = re.search(r"\d+", str(s))
    return int(match.group()) if match else float('inf')

def get_options(df, col_name):
    opts = df[col_name].dropna().unique().tolist()
    if col_name == "ปีงบประมาณ":
        opts = sorted([str(x) for x in opts])
    elif col_name == "หน่วยงาน":
        opts = sorted(opts, key=extract_number)
    else:
        opts.sort()
    return ["ทั้งหมด"] + opts

filtered_for_options = df.copy()

# --- ส่วนตัวกรอง ---
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown("### 🎯 เลือกเงื่อนไขการกรองข้อมูล")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.markdown('<div class="emoji-large">💰</div>', unsafe_allow_html=True)
    budget_options = get_options(filtered_for_options, "รูปแบบงบประมาณ")
    selected_budget = st.selectbox("รูปแบบงบประมาณ", budget_options, key="budget_select")
    if selected_budget != "ทั้งหมด":
        filtered_for_options = filtered_for_options[filtered_for_options["รูปแบบงบประมาณ"] == selected_budget]

with col2:
    st.markdown('<div class="emoji-large">📅</div>', unsafe_allow_html=True)
    year_options = get_options(filtered_for_options, "ปีงบประมาณ")
    selected_year = st.selectbox("ปีงบประมาณ", year_options, key="year_select")
    if selected_year != "ทั้งหมด":
        filtered_for_options = filtered_for_options[filtered_for_options["ปีงบประมาณ"].astype(str) == selected_year]

with col3:
    st.markdown('<div class="emoji-large">📌</div>', unsafe_allow_html=True)
    project_options = get_options(filtered_for_options, "โครงการ")
    selected_project = st.selectbox("โครงการ", project_options, key="project_select")
    if selected_project != "ทั้งหมด":
        filtered_for_options = filtered_for_options[filtered_for_options["โครงการ"] == selected_project]

with col4:
    st.markdown('<div class="emoji-large">🏢</div>', unsafe_allow_html=True)
    department_options = get_options(filtered_for_options, "หน่วยงาน")
    default_departments = st.session_state.get("dept_select", ["ทั้งหมด"])
    valid_defaults = [d for d in default_departments if d in department_options]
    if not valid_defaults:
        valid_defaults = ["ทั้งหมด"]
    selected_departments = st.multiselect("หน่วยงาน", department_options, default=valid_defaults, key="dept_select")
    if "ทั้งหมด" not in selected_departments:
        filtered_for_options = filtered_for_options[filtered_for_options["หน่วยงาน"].isin(selected_departments)]

st.markdown('</div>', unsafe_allow_html=True)

# --- กรองข้อมูล ---
filtered_df = df.copy()

if selected_budget != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["รูปแบบงบประมาณ"] == selected_budget]

if selected_year != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["ปีงบประมาณ"].astype(str) == selected_year]

if selected_project != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["โครงการ"] == selected_project]

if "ทั้งหมด" not in selected_departments:
    filtered_df = filtered_df[filtered_df["หน่วยงาน"].isin(selected_departments)]

# Results display with beautiful styling
if not filtered_df.empty:
    st.markdown(
        f'<div class="results-card hover-card">'
        f'🎉 <strong>พบข้อมูลทั้งหมด {len(filtered_df):,} แห่ง</strong>'
        f'</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="results-card" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);">'
        '⚠️ <strong>ไม่พบข้อมูลที่ตรงกับเงื่อนไขที่เลือก</strong>'
        '</div>',
        unsafe_allow_html=True
    )

# Enhanced tabs
tab_table, tab_chart = st.tabs(["📄 ตารางข้อมูล", "📊 กราฟสรุป"])

with tab_table:
    if not filtered_df.empty:
        st.markdown("### 📋 รายละเอียดข้อมูลที่กรองแล้ว")
        filtered_df_display = filtered_df.drop(columns=["id"], errors="ignore")
        st.dataframe(filtered_df_display, use_container_width=True, height=500)
    else:
        st.markdown(
            '<div style="text-align: center; padding: 3rem; color: #666;">'
            '<h3>📭 ไม่มีข้อมูลที่จะแสดง</h3>'
            '<p>กรุณาปรับเงื่อนไขการกรองใหม่</p>'
            '</div>',
            unsafe_allow_html=True
        )

import plotly.express as px

with tab_chart:
    if not filtered_df.empty:
        st.markdown("### 📈 สถิติและแนวโน้ม")
        
        chart_data = (
            filtered_df.groupby(["ปีงบประมาณ", "รูปแบบงบประมาณ"])
            .size()
            .reset_index(name="จำนวนโครงการ")
        )

        fig = px.bar(
            chart_data,
            x="ปีงบประมาณ",
            y="จำนวนโครงการ",
            color="รูปแบบงบประมาณ",
            barmode="group",
            text_auto=True,
            title="📊 จำนวนโครงการตามรูปแบบงบประมาณในแต่ละปี",
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=80, b=100),
            legend=dict(
                title="",
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
            xaxis_title="ปีงบประมาณ",
            yaxis_title="จำนวนโครงการ",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=18,
            title_x=0.5
        )

        fig.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            textfont_size=12
        )

        st.plotly_chart(fig, use_container_width=True)
        
        # Additional stats
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            total_projects = len(filtered_df)
            st.markdown(
                f'<div style="background: linear-gradient(45deg, #ff6b6b, #ee5a52); '
                f'padding: 1rem; border-radius: 10px; text-align: center; color: white;">'
                f'<h3>🎯</h3><h2>{total_projects:,}</h2><p>โครงการทั้งหมด</p></div>',
                unsafe_allow_html=True
            )
        
        with col_stat2:
            unique_departments = filtered_df['หน่วยงาน'].nunique()
            st.markdown(
                f'<div style="background: linear-gradient(45deg, #4ecdc4, #44a08d); '
                f'padding: 1rem; border-radius: 10px; text-align: center; color: white;">'
                f'<h3>🏢</h3><h2>{unique_departments}</h2><p>หน่วยงาน</p></div>',
                unsafe_allow_html=True
            )
        
        with col_stat3:
            unique_provinces = filtered_df['จังหวัด'].nunique()
            st.markdown(
                f'<div style="background: linear-gradient(45deg, #667eea, #764ba2); '
                f'padding: 1rem; border-radius: 10px; text-align: center; color: white;">'
                f'<h3>🗺️</h3><h2>{unique_provinces}</h2><p>จังหวัด</p></div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            '<div style="text-align: center; padding: 3rem; color: #666;">'
            '<h3>📊 ไม่มีข้อมูลที่จะแสดงในกราฟ</h3>'
            '<p>กรุณาปรับเงื่อนไขการกรองใหม่</p>'
            '</div>',
            unsafe_allow_html=True
        )

# --- Excel Download & Upload Section ---
def to_excel_bytes(df_to_export):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_to_export.to_excel(writer, index=False)
    return output.getvalue()

st.markdown("---")
st.markdown("### 🔄 จัดการข้อมูล")

col_up, spacer, col_dl = st.columns([2, 1, 2])

with col_dl:
    if not filtered_df.empty:
        st.markdown("#### 📥 ดาวน์โหลดข้อมูล")
        st.download_button(
            label="💾 ดาวน์โหลดข้อมูลที่กรองเป็น Excel",
            data=to_excel_bytes(filtered_df),
            file_name=f"filtered_data_{len(filtered_df)}_records.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with col_up:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("#### 📤 อัปโหลดข้อมูลใหม่")
    st.markdown("เลือกไฟล์ Excel เพื่อเพิ่มข้อมูลเข้าสู่ระบบ")
    
    uploaded_file = st.file_uploader("🗂️ เลือกไฟล์ Excel", type=["xlsx"], key="file_uploader")
    
    if uploaded_file:
        try:
            with st.spinner('⏳ กำลังประมวลผลไฟล์...'):
                uploaded_df = pd.read_excel(uploaded_file)
                missing_cols = [col for col in required_columns if col not in uploaded_df.columns]
                
                if missing_cols:
                    st.error(f"❌ คอลัมน์เหล่านี้หายไปจากไฟล์ที่อัปโหลด: {', '.join(missing_cols)}")
                else:
                    # Insert data to Supabase
                    supabase.table(TABLE_NAME).insert(uploaded_df.to_dict(orient="records")).execute()
                    
                    project_names = uploaded_df['โครงการ'].dropna().unique().tolist()
                    sample_projects = ", ".join(project_names[:3])
                    more_text = "..." if len(project_names) > 3 else ""
                    
                    st.success(f"✅ เพิ่มข้อมูล {len(uploaded_df):,} แถวลงใน Supabase สำเร็จแล้ว")
                    st.info(f"📌 โครงการที่เพิ่ม:\n{sample_projects}{more_text}")
                    
                    # Clear cache to show updated data
                    st.cache_data.clear()
                    st.balloons()  # 🎈
                    st.rerun()
                    
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดขณะอ่านไฟล์: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; padding: 1rem;">'
    '<p>💻 ระบบจัดการข้อมูลงบประมาณ | สร้างด้วย Streamlit & Supabase</p>'
    '</div>',
    unsafe_allow_html=True
)
