import streamlit as st
from google import genai

# Cấu hình giao diện trang rộng (Wide Layout)
st.set_page_config(page_title="Gemini AI & Google Drive", layout="wide")

st.title("🤖 Ứng Dụng Gemini AI & Google Drive")

# Chia giao diện làm 2 khung (cột)
col1, col2 = st.columns(2)

# ================= KHUNG 1: CẤU HÌNH & GOOGLE DRIVE (BÊN TRÁI) =================
with col1:
    st.header("📁 Khung 1: Quản lý Google Drive & Cấu hình")
    
    # Ô nhập Gemini API Key
    api_key = st.text_input("Nhập Gemini API Key của bạn:", type="password")
    if not api_key:
        st.info("💡 Vui lòng nhập Gemini API Key để kích hoạt tính năng Chat.")
        
    st.divider()
    
    # Khai báo tệp/thư mục Google Drive
    st.subheader("Kết nối Tệp từ Google Drive")
    drive_input = st.text_input("Nhập File ID hoặc Đường dẫn Google Drive:")
    
    if st.button("Kết nối & Tải dữ liệu"):
        if drive_input:
            st.success(f"Đã ghi nhận File ID: {drive_input}")
        else:
            st.warning("Vui lòng nhập File ID hoặc link Google Drive.")

# ================= KHUNG 2: CHAT VỚI GEMINI AI (BÊN PHẢI) =================
with col2:
    st.header("💬 Khung 2: Trợ lý Chat Gemini AI")
    
    # Khởi tạo lịch sử chat trong session
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Hiển thị lại các tin nhắn cũ
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Ô nhập câu hỏi từ người dùng
    if prompt := st.chat_input("Nhập câu hỏi của bạn cho Gemini..."):
        # Lưu câu hỏi của người dùng vào lịch sử
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Xử lý phản hồi từ Gemini AI
        with st.chat_message("assistant"):
            if not api_key:
                response = "⚠️ Vui lòng nhập **Gemini API Key** ở Khung 1 bên trái để bắt đầu trò chuyện."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                try:
                    # Khởi tạo Client Gemini API
                    client = genai.Client(api_key=api_key)
                    
                    # Gọi mô hình Gemini để trả lời
                    res = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                    response = res.text
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    err_msg = f"❌ Lỗi kết nối Gemini API: {e}"
                    st.error(err_msg)
