import streamlit as st
from pearl_response import get_response
from translate_input import trans_text
from language_codes import LANGUAGES

def main():
    st.set_page_config(page_title="Dr Pearl", page_icon="❤️", layout="centered")
    st.title("Dr Pearl")
    st.write("Welcome! Type 'exit' to end the conversation.")

    # --- SESSION STATE ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_user_input" not in st.session_state:
        st.session_state.last_user_input = ""

    # --- SIDEBAR FOR LANGUAGE SELECTION ---
    lang = st.sidebar.selectbox(
        "Choose your preferred language:",
        LANGUAGES.keys(),
        index=0
    )

    if not lang:
        st.warning("Please select a valid language code (e.g., 'en', 'fr', 'es').")
        return

    st.markdown(
        f"**{trans_text('I am Dr. Pearl. Please describe how you feel as detailed as you can. Remember, health is wealth.', lang)}**"
    )

    # --- CUSTOM STYLES ---
    st.markdown("""
        <style>
        .chat-box {
            background-color: #0e1117;
            padding: 15px;
            border-radius: 12px;
            height: 480px;
            overflow-y: auto;
            border: 1px solid #333;
            display: flex;
            flex-direction: column;  /* changed from column-reverse */
            scroll-behavior: smooth;
        }
        .user-msg {
            background-color: #1f77b4;
            color: white;
            padding: 8px 12px;
            border-radius: 10px;
            margin: 6px 0;
            text-align: right;
        }
        .bot-msg {
            background-color: #333;
            color: #eee;
            padding: 8px 12px;
            border-radius: 10px;
            margin: 6px 0;
            text-align: left;
        }
        .bottom-input {
            position: sticky;
            bottom: 0;
            background-color: #0e1117;
            padding-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- CHAT CONTAINER ---
    chat_container = st.container()
    with chat_container:
        st.markdown("### 💬 Conversation")
        st.markdown('<div class="chat-box" id="chat-box">', unsafe_allow_html=True)
        
        # Display messages in normal chronological order (oldest to newest)
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"<div class='user-msg'>🧑‍⚕️ {chat['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-msg'>🤖 {chat['text']}</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # --- AUTO SCROLL SCRIPT ---
        st.markdown("""
            <script>
                var chatBox = window.parent.document.querySelector("#chat-box");
                if (chatBox) {
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            </script>
        """, unsafe_allow_html=True)

    # --- INPUT BOX (STICKY AT BOTTOM) ---
    st.markdown('<div class="bottom-input">', unsafe_allow_html=True)
    user_input = st.text_input(trans_text("💬 Type your message:", lang), key="user_input")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- HANDLE INPUT ---
    if user_input and user_input != st.session_state.last_user_input:
        st.session_state.last_user_input = user_input  # Prevent double-send

        if user_input.lower() == 'exit':
            st.success(trans_text("Goodbye! Stay healthy!", lang))
            st.session_state.chat_history = []
            st.session_state.last_user_input = ""
            st.stop()
        else:
            # Append user message
            st.session_state.chat_history.append({"role": "user", "text": user_input})

            # Get bot response
            bot_response = get_response(user_input, lang)

            # Append bot response
            st.session_state.chat_history.append({"role": "bot", "text": bot_response})

            # Force rerun to refresh chat immediately
            st.rerun()

if __name__ == "__main__":
    main()
