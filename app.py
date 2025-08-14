# StudyMate - Modern AI Academic Assistant
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

# Custom CSS for modern UI
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Variables */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #06b6d4;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-glass: rgba(255, 255, 255, 0.25);
        --border-color: #e5e7eb;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }

    /* Dark mode variables */
    [data-theme="dark"] {
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --bg-glass: rgba(31, 41, 55, 0.25);
        --border-color: #374151;
    }

    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 8rem; /* Extra space for fixed footer */
        max-width: 1200px;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom fonts */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism containers */
    .glass-container {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: var(--shadow-lg);
        padding: 2rem;
        margin: 1rem 0;
    }

    /* Neumorphism elements */
    .neuro-button {
        background: var(--bg-primary);
        border-radius: 15px;
        box-shadow: 8px 8px 16px #d1d9e6, -8px -8px 16px #ffffff;
        border: none;
        padding: 12px 24px;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .neuro-button:hover {
        box-shadow: 4px 4px 8px #d1d9e6, -4px -4px 8px #ffffff;
        transform: translateY(-2px);
    }

    /* Animated gradient backgrounds */
    .gradient-bg {
        background: var(--gradient-primary);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        animation: fadeInUp 0.5s ease-out;
    }

    .chat-message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
        flex-direction: row-reverse;
    }

    .chat-message.assistant {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
        margin-right: 2rem;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Profile icons */
    .profile-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 600;
        flex-shrink: 0;
    }

    .profile-icon.user {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }

    .profile-icon.assistant {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }

    /* Floating action button */
    .floating-btn {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: var(--gradient-accent);
        border: none;
        box-shadow: var(--shadow-xl);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
        transition: all 0.3s ease;
        z-index: 1000;
    }

    .floating-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 25px 35px -5px rgba(0, 0, 0, 0.2);
    }

    /* Loading animations */
    .loading-dots {
        display: inline-block;
    }

    .loading-dots::after {
        content: '';
        animation: dots 1.5s steps(5, end) infinite;
    }

    @keyframes dots {
        0%, 20% { content: ''; }
        40% { content: '.'; }
        60% { content: '..'; }
        80%, 100% { content: '...'; }
    }

    /* Upload area styling */
    .upload-area {
        border: 2px dashed var(--primary-color);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .upload-area:hover {
        border-color: var(--secondary-color);
        background: rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
    }

    /* Custom buttons */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: var(--gradient-primary);
        border-radius: 10px;
    }

    /* Expandable sections */
    .expandable-content {
        max-height: 200px;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }

    .expandable-content.expanded {
        max-height: none;
    }

    .expand-btn {
        background: none;
        border: none;
        color: var(--primary-color);
        cursor: pointer;
        font-weight: 500;
        margin-top: 0.5rem;
    }

    /* Fixed footer styling */
    .fixed-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border-top: 1px solid var(--border-color);
        padding: 1rem 0;
        text-align: center;
        opacity: 0.8;
        z-index: 999;
        box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Chat container with more height */
    .chat-container {
        min-height: 60vh;
        max-height: 70vh;
        overflow-y: auto;
        padding: 1rem;
        margin-bottom: 2rem;
        border-radius: 15px;
        background: var(--bg-glass);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-bottom: 10rem; /* More space on mobile for footer */
        }

        .chat-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
        }

        .floating-btn {
            bottom: 6rem; /* Above fixed footer */
            right: 1rem;
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
        }

        .chat-container {
            min-height: 50vh;
            max-height: 60vh;
        }

        .fixed-footer {
            padding: 0.75rem 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

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

# Helper functions for UI components
def render_chat_message(message, is_user=True):
    """Render a chat message with modern styling"""
    role = "user" if is_user else "assistant"
    icon = "👤" if is_user else "🤖"

    timestamp = message.get("timestamp", datetime.now().strftime("%H:%M"))

    st.markdown(f"""
    <div class="chat-message {role}">
        <div class="profile-icon {role}">{icon}</div>
        <div class="message-content">
            <div class="message-text">{message['content']}</div>
            <div class="message-time" style="font-size: 0.8rem; opacity: 0.7; margin-top: 0.25rem;">{timestamp}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_expandable_content(content, max_length=300):
    """Render content with expand/collapse functionality"""
    if len(content) <= max_length:
        return content

    short_content = content[:max_length] + "..."

    with st.expander("📖 Read full response"):
        st.markdown(content)

    return short_content

def render_loading_animation(text="Processing"):
    """Render a loading animation"""
    return st.markdown(f"""
    <div style="text-align: center; padding: 1rem;">
        <div class="loading-dots">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="StudyMate - AI Academic Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load custom CSS
    load_custom_css()

    # Initialize session state
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processing" not in st.session_state:
        st.session_state.processing = False

    # Sidebar with modern design
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
            <h1 style="margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-weight: 700;">StudyMate</h1>
            <p style="margin: 0.5rem 0; opacity: 0.8; font-style: italic;">Your AI Academic Assistant</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("---")

        # Upload section with modern styling
        st.markdown("""
        <div class="glass-container">
            <h3 style="margin-top: 0; color: var(--primary-color);">📄 Upload Study Materials</h3>
            <p style="opacity: 0.8; margin-bottom: 1rem;">Upload textbooks, lecture notes, research papers, or any study materials</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Choose files",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        # Process button with modern styling
        if uploaded_files:
            st.markdown("""
            <div class="upload-area" style="margin: 1rem 0;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📁</div>
                <p><strong>{} file(s) selected</strong></p>
                <p style="opacity: 0.7;">Ready to process your study materials</p>
            </div>
            """.format(len(uploaded_files)), unsafe_allow_html=True)

        process_btn = st.button(" Process Documents", type="primary", use_container_width=True)

        if process_btn:
            if uploaded_files:
                st.session_state.processing = True

                # Progress bar with animation
                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    status_text.markdown("📂 Saving uploaded files...")
                    progress_bar.progress(20)
                    time.sleep(0.5)

                    saved_file_paths = save_uploaded_files(uploaded_files)
                    pdf_paths = [p for p in saved_file_paths if p.lower().endswith(".pdf")]
                    txt_paths = [p for p in saved_file_paths if p.lower().endswith(".txt")]

                    status_text.markdown("📖 Extracting text from documents...")
                    progress_bar.progress(40)
                    time.sleep(0.5)

                    raw_text = ""
                    if pdf_paths:
                        raw_text += get_all_pdf_text(pdf_paths)
                    if txt_paths:
                        raw_text += get_txt_text(txt_paths)

                    if raw_text:
                        status_text.markdown("✂️ Creating text chunks...")
                        progress_bar.progress(60)
                        time.sleep(0.5)

                        text_chunks = get_text_chunks(raw_text)

                        status_text.markdown("🧠 Building knowledge base...")
                        progress_bar.progress(80)
                        time.sleep(0.5)

                        st.session_state.vector_store = get_vector_store_from_texts(text_chunks)

                        progress_bar.progress(100)
                        status_text.markdown("✅ Processing complete!")
                        time.sleep(1)

                        st.success("🎉 Documents processed successfully! You can now ask questions about your study materials.")
                        st.session_state.messages = []
                        st.balloons()
                    else:
                        st.error("❌ Could not extract any text from the uploaded files. Please check if the files are readable.")

                except Exception as e:
                    st.error(f"❌ Error processing documents: {str(e)}")

                finally:
                    st.session_state.processing = False
                    progress_bar.empty()
                    status_text.empty()
            else:
                st.warning("⚠️ Please upload at least one document before processing.")

        # Status indicator
        if st.session_state.vector_store:
            st.markdown("""
            <div class="glass-container" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%); border-color: #10b981;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
                    <h4 style="margin: 0; color: #10b981;">Study Materials Ready!</h4>
                    <p style="margin: 0.5rem 0; opacity: 0.8;">Your documents have been processed and indexed</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Tips section with modern styling
        st.markdown("""
        <div class="glass-container">
            <h4 style="margin-top: 0; color: var(--accent-color);">💡 Tips for Better Results</h4>
            <ul style="margin: 0; padding-left: 1.2rem; opacity: 0.9;">
                <li>Ask specific questions about your materials</li>
                <li>Use clear, complete sentences</li>
                <li>Reference specific topics or concepts</li>
                <li>Try different phrasings if needed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Clear chat button
        if st.session_state.messages:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()



    # Welcome section or chat display
    if not st.session_state.messages:
        # Welcome section in center
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; margin: 2rem 0;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🎓</div>
            <h1 style="color: #6366f1; font-size: 2.5rem; margin-bottom: 1rem; font-weight: 700;">
                Welcome to StudyMate
            </h1>
            <p style="font-size: 1.2rem; color: #6b7280; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Your AI-powered academic assistant is ready to help you understand your study materials.
                Upload your documents and start asking questions to enhance your learning experience.
            </p>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; padding: 1.5rem; border-radius: 15px;
                        max-width: 500px; margin: 0 auto; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem;">✨ Getting Started</h3>
                <p style="margin: 0; opacity: 0.9; line-height: 1.6;">
                    1. Upload your PDF or text files in the sidebar<br>
                    2. Click "Process Documents" to analyze your materials<br>
                    3. Ask any question about your study content below
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Detailed Chat History Section
        st.markdown("""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="color: #6366f1; font-size: 1.8rem; margin-bottom: 0.5rem; text-align: center;">
                💬 Chat History
            </h2>
            <p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">
                Review your conversation with StudyMate
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Create expandable sections for each Q&A pair
        qa_pairs = []
        current_question = None

        for message in st.session_state.messages:
            if "timestamp" not in message:
                message["timestamp"] = datetime.now().strftime("%H:%M")

            if message["role"] == "user":
                current_question = message
            elif message["role"] == "assistant" and current_question:
                qa_pairs.append((current_question, message))
                current_question = None

        # Display Q&A pairs in detailed format
        for i, (question, answer) in enumerate(qa_pairs, 1):
            with st.expander(f"📝 Question {i}: {question['content'][:60]}{'...' if len(question['content']) > 60 else ''}", expanded=True):
                # Question section
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                           padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">👤</span>
                        <strong style="color: #1976d2;">Your Question</strong>
                        <span style="margin-left: auto; font-size: 0.9rem; color: #666;">⏰ {question['timestamp']}</span>
                    </div>
                    <p style="margin: 0; font-size: 1rem; line-height: 1.5; color: #333;">
                        {question['content']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Answer section with dark theme
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
                           padding: 1rem; border-radius: 10px; border: 1px solid #4b5563;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">🤖</span>
                        <strong style="color: #60a5fa;">StudyMate's Answer</strong>
                        <span style="margin-left: auto; font-size: 0.9rem; color: #9ca3af;">⏰ {answer['timestamp']}</span>
                    </div>
                    <div style="margin: 0; font-size: 1rem; line-height: 1.6; color: #f3f4f6;">
                        {answer['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Add some spacing between Q&A pairs
                st.markdown("<br>", unsafe_allow_html=True)

        # Handle any remaining unpaired user message
        if current_question:
            with st.expander(f"📝 Latest Question: {current_question['content'][:60]}{'...' if len(current_question['content']) > 60 else ''}", expanded=True):
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                           padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">👤</span>
                        <strong style="color: #1976d2;">Your Question</strong>
                        <span style="margin-left: auto; font-size: 0.9rem; color: #666;">⏰ {current_question['timestamp']}</span>
                    </div>
                    <p style="margin: 0; font-size: 1rem; line-height: 1.5; color: #333;">
                        {current_question['content']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.info("⏳ Waiting for StudyMate's response...")

        # Summary section
        if qa_pairs:
            st.markdown("---")
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: #6366f1; margin: 0;">📊 Conversation Summary</h4>
                <p style="margin: 0.5rem 0; color: #6b7280;">
                    Total Questions Asked: <strong>{len(qa_pairs)}</strong> |
                    Last Activity: <strong>{qa_pairs[-1][1]['timestamp'] if qa_pairs else 'N/A'}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)




    # Chat input
    user_question = st.chat_input("What would you like to know about your study materials?")

    if user_question:
        # Add user message with timestamp
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user",
            "content": user_question,
            "timestamp": timestamp
        })

        if st.session_state.vector_store:
            # Process the question and add response
            with st.spinner("🤔 StudyMate is thinking..."):
                response = process_question(user_question, st.session_state.vector_store)

            # Add assistant response with timestamp
            response_timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": response_timestamp
            })
        else:
            # For testing, provide a simple response even without documents
            if "test" in user_question.lower() or "hello" in user_question.lower():
                response = f"Hello! I received your message: '{user_question}'. Please upload and process your study materials to get answers about your documents."
            else:
                response = "⚠️ Please upload and process your study materials first before asking questions. I need documents to provide accurate answers about your study content."

            response_timestamp = datetime.now().strftime("%H:%M")
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": response_timestamp
            })

        # Force a rerun to show the new messages
        st.rerun()

    # Floating action button for clearing chat (using HTML/CSS)
    if st.session_state.messages:
        st.markdown("""
        <div class="floating-btn" onclick="clearChat()" title="Clear Chat History">
            🗑️
        </div>
        <script>
        function clearChat() {
            // This would need to be implemented with Streamlit's session state
            alert('Use the Clear Chat History button in the sidebar to clear messages');
        }
        </script>
        """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()