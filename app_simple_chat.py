# StudyMate - Simple Chat Version (No Conversation History)
import streamlit as st
import os
import time
from datetime import datetime
from backend import (
    get_all_pdf_text,
    get_txt_text,
    get_text_chunks,
    get_vector_store_from_texts,
    process_question
)

def save_uploaded_files(uploaded_files):
    temp_dir = "temp_uploaded_files"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    saved_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(file_path)
    return saved_paths

def main():
    st.set_page_config(
        page_title="StudyMate - AI Academic Assistant", 
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    # Sidebar
    with st.sidebar:
        st.title("🎓 StudyMate")
        st.markdown("*Your AI Academic Assistant*")
        st.markdown("---")

        # Dark mode toggle
        dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()

        st.markdown("---")

        # Upload section
        st.subheader("📄 Upload Study Materials")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=["pdf", "txt"],
            accept_multiple_files=True
        )

        if st.button("🚀 Process Documents", type="primary", use_container_width=True):
            if uploaded_files:
                with st.spinner("Processing..."):
                    saved_file_paths = save_uploaded_files(uploaded_files)
                    pdf_paths = [p for p in saved_file_paths if p.lower().endswith(".pdf")]
                    txt_paths = [p for p in saved_file_paths if p.lower().endswith(".txt")]
                    raw_text = ""
                    if pdf_paths:
                        raw_text += get_all_pdf_text(pdf_paths)
                    if txt_paths:
                        raw_text += get_txt_text(txt_paths)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        st.session_state.vector_store = get_vector_store_from_texts(text_chunks)
                        st.success("✅ Documents processed successfully!")
                        st.session_state.messages = []
                    else:
                        st.error("❌ Could not extract any text from the uploaded files.")
            else:
                st.warning("⚠️ Please upload at least one document before processing.")

        # Status indicator
        if st.session_state.vector_store:
            st.success("📚 Study materials ready!")

        st.markdown("---")

        # Chat History Section
        st.subheader("💬 Chat History")
        if st.session_state.messages:
            # Create a scrollable container for chat history
            with st.container():
                for i, message in enumerate(st.session_state.messages):
                    if "timestamp" not in message:
                        message["timestamp"] = datetime.now().strftime("%H:%M")

                    # Display message in sidebar with compact format
                    if message["role"] == "user":
                        st.markdown(f"""
                        <div style="background: #e3f2fd; padding: 0.5rem; border-radius: 8px; margin: 0.25rem 0;">
                            <small><strong>👤 You ({message['timestamp']}):</strong></small><br>
                            <small>{message['content'][:100]}{'...' if len(message['content']) > 100 else ''}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: #f3e5f5; padding: 0.5rem; border-radius: 8px; margin: 0.25rem 0;">
                            <small><strong>🤖 StudyMate ({message['timestamp']}):</strong></small><br>
                            <small>{message['content'][:100]}{'...' if len(message['content']) > 100 else ''}</small>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown("*No conversation yet. Start by asking a question!*")

        # Clear chat button
        if st.session_state.messages:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # Main content area
    st.header("💬 Chat with StudyMate")
    st.markdown("Ask any question about your uploaded study materials!")

    # Question input section - moved higher
    st.subheader("💭 Ask Your Question")
    user_question = st.chat_input("What would you like to know about your study materials?")

    # Chat display below question input
    if st.session_state.messages:
        st.markdown("---")
        st.subheader("📝 Current Conversation")
        for message in st.session_state.messages:
            if "timestamp" not in message:
                message["timestamp"] = datetime.now().strftime("%H:%M")

            with st.chat_message(message["role"]):
                st.markdown(f"{message['content']}")
                st.caption(f"⏰ {message['timestamp']}")
    else:
        st.markdown("---")
        st.info("💡 Start a conversation by asking a question above!")
    
    if user_question:
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user", 
            "content": user_question,
            "timestamp": timestamp
        })
        
        if st.session_state.vector_store:
            with st.spinner("🤔 StudyMate is thinking..."):
                response = process_question(user_question, st.session_state.vector_store)
            
            response_timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "timestamp": response_timestamp
            })
        else:
            if "test" in user_question.lower() or "hello" in user_question.lower():
                response = f"Hello! I received your message: '{user_question}'. Please upload and process your study materials to get answers about your documents."
            else:
                response = "⚠️ Please upload and process your study materials first before asking questions."
            
            response_timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "timestamp": response_timestamp
            })
        
        st.rerun()



if __name__ == "__main__":
    main()
