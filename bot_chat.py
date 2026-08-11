
  import streamlit as st
from google import genai

# Cấu hình giao diện
st.set_page_config(page_title="Trợ lý ảo cá nhân - MTA & Cấp 3", page_icon="🤖", layout="centered")

# Dùng cache_resource để giữ client luôn hoạt động
@st.cache_resource
def get_client():
    return genai.Client(api_key="AQ.Ab8RN6LId07QEAy0D8XrHvz1y40GXW47T7r6qOtKx9rNIBJn9fw")

client = get_client()

# Thanh sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("🎯 Góc Cạ Cứng")
    st.markdown("---")
    st.markdown("**Hồ sơ đồng hành:**")
    st.markdown("- 🎒 **Cấp 3:** Học sinh lớp 10")
    st.markdown("- 🎯 **Mục tiêu:** Thi vào MTA & HSA")
    st.markdown("- 🇬🇧 **Ngoại ngữ:** Chinh phục IELTS")
    st.markdown("- 🏸 **Thể thao:** Cầu lông")
    st.markdown("- 🚀 **Sở thích:** Công nghệ, Vũ trụ, Quân sự")
    st.markdown("---")
    st.caption("Trợ lý độc quyền 2026")

# Tiêu đề chính
st.title("🤖 Trợ lý ảo cá nhân độc quyền")
st.markdown("---")

system_instruction = """
Bạn là một trợ lý ảo cá nhân thông minh, gần gũi, là bạn đồng hành cùng chủ nhân (học sinh lớp 10) trong 3 năm cấp 3.
Ghi nhớ: Chủ nhân thích công nghệ, quân sự, vũ trụ, đang ôn thi HSA/MTA và học IELTS. 
Nhiệm vụ: Hỗ trợ bài tập, kèm Tiếng Anh, trò chuyện tâm sự.
"""

# Khởi tạo phiên chat
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": system_instruction}
    )

# Hiển thị tin nhắn cũ
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý tin nhắn mới
if user_input := st.chat_input("Nhắn gì đi cạ cứng ơi..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Cạ cứng đang suy nghĩ..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Ơ, có vẻ kết nối bị gián đoạn. Cậu thử tải lại trang (F5) nhé!")