import streamlit as st
from google import genai

# 1. Cấu hình giao diện tổng thể
st.set_page_config(
    page_title="MTA Tactical AI - Đức Minh",
    page_icon="🛰️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. CSS tùy chỉnh giao diện
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #1f2937;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #f9fafb;
        border-radius: 12px;
        border: 1px solid #d1d5db;
        color: #1e3a8a;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #f9fafb;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        color: #111827;
    }
    .stTextInput input {
        background-color: #f9fafb !important;
        color: #111827 !important;
        border: 1px solid #9ca3af !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] {
        background-color: #f3f4f6;
        border-right: 1px solid #e5e7eb;
    }
    h1, h2, h3 {
        color: #111827;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Khởi tạo Client Gemini tương thích hoàn toàn với khóa AQ.
@st.cache_resource
def get_client():
    api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)

client = get_client()

# 4. Hồ sơ hệ thống (System Instruction)
system_instruction = """
Bạn là một trợ lý ảo chiến thuật cá nhân thông minh, tâm lý và là người bạn đồng hành thân thiết của Đức Minh – một nam sinh lớp 10.

**Hồ sơ của Đức Minh (Chủ nhân):**
* Tính cách: Hướng nội, thích sự sâu sắc, điềm tĩnh.
* Đam mê: Đặc biệt yêu thích tìm hiểu về Công nghệ, Quân sự và Vũ trụ. Thích phân tích văn học (hiểu rõ các thể thơ truyền thống như Song Thất Lục Bát).
* Thể thao: Thích đánh cầu lông và chạy bộ để rèn luyện sức khỏe.
* Học lực hiện tại: Đang yếu môn Tiếng Anh; các môn Toán, Lý, Hóa ở mức bình thường (cần cải thiện và bứt phá).
* Mục tiêu tối thượng: Đỗ vào Học viện Kỹ thuật Quân sự (MTA) và đạt điểm cao trong kỳ thi Đánh giá năng lực (HSA). Đồng thời cần học tốt tiếng Anh để chuẩn bị cho IELTS.

**Nhiệm vụ của bạn:**
1. Gia sư chiến thuật: Hỗ trợ Minh học tập mỗi ngày. Kiên nhẫn giảng giải các bài tập Toán, Lý, Hóa từ cơ bản đến nâng cao để cải thiện điểm số.
2. Định hướng thi cử: Bám sát mục tiêu thi MTA và HSA. Cung cấp kiến thức, mẹo giải đề, và lộ trình ôn thi chuẩn xác.
3. Đồng đội tâm giao: Trợ lý mang phong cách trạm không gian/quân sự, sẵn sàng cùng Minh bàn luận về công nghệ hiện đại, khí tài quân sự, hoặc chia sẻ áp lực học tập.
4. Xưng hô: Gọi chủ nhân là "Minh" hoặc "cậu", xưng là "tớ" hoặc "mình" tạo cảm giác gắn kết như hai người bạn đồng hành chí cốt.
"""

# 5. Thanh sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3065/3065405.png", width=80)
    st.markdown("### 🛰️ TRẠM KHÔNG GIAN MTA")
    st.markdown("---")
    st.markdown("**🛡️ HỒ SƠ CHỈ HUY:**")
    st.markdown("- 👤 **Chủ nhân:** Đức Minh (2011)")
    st.markdown("- 🎓 **Cấp độ:** Lớp 10")
    st.markdown("- 🎖️ **Mục tiêu:** MTA & HSA")
    st.markdown("- 🌐 **Ngoại ngữ:** IELTS Focus")
    st.markdown("- 🛰️ **Lĩnh vực:** Công nghệ, Vũ trụ, Quân sự")
    st.markdown("- 🎾 **Thể lực:** Cầu lông, Chạy bộ")
    st.markdown("---")
    st.caption("MTA MISSION CONTROL: ONLINE 🟢")

# 6. Giao diện Chat chính
st.title("🛰️ MTA SPACE & TACTICAL ASSISTANT")
st.caption("Hệ thống trợ lý ảo cá nhân hóa dành riêng cho Đức Minh – Hướng tới Học viện Kỹ thuật Quân sự (MTA)")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập yêu cầu bài tập hoặc câu hỏi về vũ trụ, quân sự cho trợ lý..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang kết nối trạm không gian..."):
            try:
                # Gộp System Instruction vào nội dung gửi cho Client mới
                full_prompt = f"{system_instruction}\n\nChủ nhân Đức Minh nói: {prompt}"
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=full_prompt,
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Lỗi kết nối trạm: {e}")
