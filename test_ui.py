#!/usr/bin/env python3
"""
Simple test to verify the UI functionality
"""

import streamlit as st
from datetime import datetime

def test_basic_ui():
    st.title("UI Test")
    
    # Test session state
    if "test_messages" not in st.session_state:
        st.session_state.test_messages = []
    
    # Test chat input
    user_input = st.chat_input("Test input")
    
    if user_input:
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.test_messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })
        
        # Echo response
        st.session_state.test_messages.append({
            "role": "assistant",
            "content": f"You said: {user_input}",
            "timestamp": timestamp
        })
    
    # Display messages
    for message in st.session_state.test_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            st.caption(f"⏰ {message['timestamp']}")

if __name__ == "__main__":
    test_basic_ui()
