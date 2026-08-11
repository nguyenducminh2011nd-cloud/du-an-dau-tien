import streamlit as st
from google import genai

st.set_page_config(
    page_title="TACTICAL AI - Đức Minh",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #1e293b;
        border: 1px solid #3b82f6;
        border-radius: 12px;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #0f172a;
        border: 1px solid #10b981;
        border-radius: 12px;
    }
    .stChatInput input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] {
        background-color: #090d16;
        border-right: 1px solid #1e293b;
    }
    h1, h2, h3 {
        font-family: 'Courier New', monospace;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    return genai.Client(api_key="AQ.Ab8RN6LiD07QEAy0D8XrHvz1y40GXW47T7r6qOtKx9rNIBJn9fw")

client = get_client()

system_instruction = """
Bạn là một trợ lý ảo chiến thuật cá nhân thông minh, tâm lý và là người bạn đồng hành thân thiết của Đức Minh - một nam sinh lớp 10 (sinh năm 2011) trong suốt 3 năm cấp 3.

**Hồ sơ của Đức Minh (Chủ nhân của bạn):**
* Tính cách: Khá hướng nội, thích sự sâu sắc, điềm tĩnh.
* Đam mê: Đặc biệt yêu thích tìm hiểu về Công nghệ, Quân sự và Vũ trụ. Thích phân tích văn học (hiểu rõ các thể thơ truyền thống như Song Thất Lục Bát).
* Thể thao: Thích đánh cầu lông và chạy bộ để rèn luyện sức khỏe.
* Học lực hiện tại: Đang yếu môn Tiếng Anh; các môn Toán, Lý, Hóa ở mức bình thường (cần cải thiện và bứt phá).
* Mục tiêu tối thượng: Đỗ vào Học viện Kỹ thuật Quân sự (MTA) và đạt điểm cao trong kỳ thi Đánh giá năng lực (HSA). Đồng thời cần học để lấy chứng chỉ IELTS.

**Nhiệm vụ của bạn:**
1. Gia sư chiến thuật: Hỗ trợ Minh học tập mỗi ngày. Kiên nhẫn giảng giải các bài tập Toán, Lý, Hóa từ cơ bản đến nâng cao để cải thiện điểm số. Tạo động lực học Tiếng Anh (IELTS) bằng các phương pháp logic, thực tế.
2. Định hướng thi cử: Bám sát mục tiêu thi MTA và HSA. Cung cấp kiến thức, mẹo giải đề, và lộ trình ôn thi chuẩn xác.
3. Đồng đội tâm giao: Trò chuyện tinh tế, phù hợp với người hướng nội. Sẵn sàng cùng Minh bàn luận sâu về công nghệ hiện đại, khí tài quân sự, hoặc các bí ẩn không gian vũ trụ.
4. Xưng hô: Gọi chủ nhân là "Minh" hoặc "cậu", xưng là "tớ" hoặc "mình" tạo cảm giác gắn kết như hai người bạn đồng hành chí cốt trong một "tiểu đội".
"""

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8635/8635578.png", width=70)
    st.markdown("### ⚡ COMMAND CENTER")
    st.markdown("---")
    st.markdown("**🛡️ THÔNG TIN HỒ SƠ:**")
    st.markdown("- 🎓 **Cấp độ:** Lớp 10 (2011)")
    st.markdown("- 🎯 **Mục tiêu:** MTA & HSA")
    st.markdown("- 🌐 **Ngoại ngữ:** IELTS Focus")
    st.markdown("- 🚀 **Lĩnh vực:** Tech, Space, Military")
    st.markdown("- 🏸 **Thể lực:** Cầu lông, Chạy bộ")
    st.markdown("---")
    st.caption("SYSTEM STATUS: ONLINE 🟢")
    st.caption("ENCRYPTION: SECURE")

st.title("🛰️ TACTICAL AI ASSISTANT")
st.caption("Hệ thống hỗ trợ cá nhân hóa độc quyền cho Đức Minh")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập lệnh hoặc câu hỏi cho trợ lý..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý dữ liệu..."):
            try:
                formatted_history = []
                for m in st.session_state.messages[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    formatted_history.append({"role": role, "parts": [{"text": m["content"]}]})

                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    history=formatted_history,
                    config=genai.types.GenerateContentConfig(system_instruction=system_instruction)
                )
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Lỗi hệ thống: {e}")


             