import streamlit as st
from google import genai

# 1. Cấu hình giao diện
st.set_page_config(
    page_title="MTA Tactical AI - Đức Minh",
    page_icon="🛰️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Khởi tạo Client
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

# 3. Hồ sơ hệ thống
system_instruction = """
Bạn là một trợ lý ảo chiến thuật cá nhân thông minh, tâm lý và là người bạn đồng hành thân thiết của Đức Minh – một nam sinh lớp 10.
Mục tiêu tối thượng của Minh: Đỗ vào Học viện Kỹ thuật Quân sự (MTA) và đạt điểm cao trong kỳ thi Đánh giá năng lực (HSA).
Xưng hô: Gọi chủ nhân là "Minh" hoặc "cậu", xưng là "tớ" hoặc "mình".
"""

# 4. Giao diện Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3065/3065405.png", width=80)
    st.markdown("### 🛰️ TRẠM KHÔNG GIAN MTA")
    st.markdown("---")
    st.markdown("**🛡️ HỒ SƠ CHỈ HUY:**")
    st.markdown("- 👤 **Chủ nhân:** Đức Minh (2011)")
    st.markdown("- 🎓 **Cấp độ:** Lớp 10")
    st.markdown("- 🎖️ **Mục tiêu:** MTA & HSA")
    st.markdown("- 🛰️ **Lĩnh vực:** Công nghệ, Vũ trụ, Quân sự")
    st.markdown("---")
    st.caption("MTA MISSION CONTROL: ONLINE 🟢")

# 5. Giao diện Chat chính
st.title("🛰️ MTA SPACE & TACTICAL ASSISTANT")
st.caption("Hệ thống trợ lý ảo cá nhân hóa dành riêng cho Đức Minh – Hướng tới Học viện Kỹ thuật Quân sự (MTA)")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập yêu cầu bài tập hoặc câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang kết nối trạm không gian..."):
            try:
                full_prompt = f"{system_instruction}\n\nChủ nhân Đức Minh nói: {prompt}"
                # Gọi đúng chuẩn tên model cho SDK mới
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Lỗi kết nối trạm: {e}")
