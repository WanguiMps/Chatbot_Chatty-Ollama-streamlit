import streamlit as st
import ollama
import time
from datetime import datetime
import json
import re

st.set_page_config(page_title="LLAMA Chatbot", layout="wide")


if "user_name" not in st.session_state or not st.session_state.user_name:
    st.warning("Please log in to access this page.")
    st.stop()

def apply_styles():
    bg_color = "#1E1E1E" if st.session_state.dark_mode else "#F8F9FA"
    text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"

    dark_mode_css = """
    .stMarkdown, .stMarkdown p {
        color: #FFFFFF !important;
    }
    """ if st.session_state.dark_mode else ""

    st.markdown(f"""
        <style>
            body, .stApp {{
                background-color: {bg_color};
                color: {text_color};
                font-size: {st.session_state.font_size}px !important;
            }}
            
            .chat-message {{
                font-size: {st.session_state.font_size}px !important;
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            
            .user-message {{
                background: linear-gradient(135deg, #2E3192 0%, #1BFFFF 100%);
                color: white !important;
                margin-left: 2rem;
            }}
            
            .assistant-message {{
                background-color: {"#2A2A2A" if st.session_state.dark_mode else "#ffffff"};
                color: {"#FFFFFF" if st.session_state.dark_mode else "#000000"} !important;
                margin-right: 2rem;
                border: 1px solid {"#3A3A3A" if st.session_state.dark_mode else "#e0e0e0"};
            }}
            
            .css-1544g2n {{
                padding: 0 !important;
            }}

            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
                padding-top: 0 !important;
                margin-top: -5rem !important;
            }}

            [data-testid="stSidebar"] .element-container:first-child {{
                margin: 0 !important;
                padding: 0 !important;
            }}

            .st-emotion-cache-1q1n0ol {{display: none !important;}}
            
            .sidebar-image {{
                margin-top: -3rem !important;
                padding: 0 !important;
            }}

            .css-1d391kg {{
                padding-top: 0 !important;
            }}
        </style>
    """, unsafe_allow_html=True)

def save_chat_history():
    with open("chat_history_illama.json", "w") as f:
        json.dump(st.session_state.illama_chat_history, f)


def load_chat_history():
    try:
        with open("chat_history_illama.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


if "illama_chat_history" not in st.session_state:
    st.session_state.illama_chat_history = load_chat_history()

if "illama_current_chat_id" not in st.session_state:
    st.session_state.illama_current_chat_id = None

if "illama_messages" not in st.session_state:
    user_name = st.session_state.get("user_name", "")
    welcome_message = f"Hi {user_name}! I'm ILLAMA, your favorite AI assistant! How can I help you today?" if user_name else "Hi I'm ILLAMA, your favorite AI assistant! How can I help you today?"
    st.session_state.illama_messages = [{"role": "assistant", "content": welcome_message}]

if "illama_search_term" not in st.session_state:
    st.session_state.illama_search_term = ""


def format_message(content):
    code_block_pattern = r"```(.*?)```"
    formatted_content = content
    
    code_blocks = re.finditer(code_block_pattern, content, re.DOTALL)
    for block in code_blocks:
        code = block.group(1)
        styled_code = f"""
        <div style='background-color: #1E1E1E; color: #D4D4D4; padding: 1rem; border-radius: 5px; margin: 0.5rem 0; font-family: monospace; white-space: pre-wrap;'>
            {code}
        </div>
        """
        formatted_content = formatted_content.replace(block.group(0), styled_code)
    
    return formatted_content


st.markdown(
    """
    <style>
        /* Hide Streamlit default menu */
        #MainMenu {visibility: hidden;}
        
        /* Hide Streamlit header */
        header {visibility: hidden;}
        
        /* Hide footer */
        footer {visibility: hidden;}
        
        /* Hide pages navigation */
        [data-testid="stSidebarNav"] {display: none !important;}
        div[data-testid="collapsedControl"] {display: none !important;}
        
        /* Reduce top padding to bring content up */
        .block-container {
            padding-top: 0 !important;
        }

        /* Remove all padding and margin from sidebar */
        .css-1544g2n {
            padding: 0 !important;
        }

        /* Adjust all sidebar elements */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            padding-top: 0 !important;
            margin-top: -5rem !important;
        }

        /* Adjust first element container */
        [data-testid="stSidebar"] .element-container:first-child {
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Hide all navigation elements */
        .st-emotion-cache-1q1n0ol {display: none !important;}
        
        /* Custom sidebar image styling */
        .sidebar-image {
            margin-top: -3rem !important;
            padding: 0 !important;
        }

        /* Adjust sidebar content padding */
        .css-1d391kg {
            padding-top: 0 !important;
        }

        /* Navigation icons container */
        .nav-icons {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            display: flex;
            gap: 10px;
        }

        .nav-icon {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #2E3192;
            text-decoration: none;
        }

        .nav-icon:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.1);
        }

        /* Dark mode adjustments for nav icons */
        [data-theme="dark"] .nav-icon {
            background: rgba(0, 0, 0, 0.2);
            color: #1BFFFF;
        }

        [data-theme="dark"] .nav-icon:hover {
            background: rgba(0, 0, 0, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Add navigation icons
st.markdown("""
    <div class="nav-icons">
        <a href="?page=home" class="nav-icon" title="Go Back">←</a>
        <a href="?page=logout" class="nav-icon" title="Logout">×</a>
    </div>
""", unsafe_allow_html=True)

# Custom CSS for modern design
st.markdown("""
    <style>
    /* Modern Color Scheme */
    :root {
        --primary-color: #2E3192;
        --secondary-color: #1BFFFF;
        --accent-color: #FF6B6B;
        --background-color: #F8F9FA;
        --text-color: #2D3436;
    }

    /* Main Container Styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
        padding: 2rem;
    }

    /* Header Styling */
    h1 {
        color: var(--primary-color);
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* Card Styling */
    .stCard {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }

    .stCard:hover {
        transform: translateY(-5px);
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem;
    }

    /* Expander Styling */
    .stExpander {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Image Container */
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Custom Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    </style>
""", unsafe_allow_html=True)

# Placeholder for loader (Ensures it loads first)
loader_placeholder = st.empty()

# Custom CSS + HTML for Instant Animated Loader
loading_animation = """
<style>
    /* Hide Streamlit Sidebar Temporarily */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Full-screen Loader */
    #loading-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }

    /* Introductory Text */
    #loading-text {
        font-size: 22px;
        font-weight: bold;
        color: #333;
        margin-bottom: 15px;
        animation: fadeIn 0.5s ease-in-out;
    }

    /* Bouncing Balls Animation */
    .balls-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .ball {
        width: 15px;
        height: 15px;
        margin: 5px;
        background-color: #3498db;
        border-radius: 50%;
        animation: bounce 1s infinite ease-in-out;
    }

    .ball:nth-child(2) {
        animation-delay: 0.2s;
    }

    .ball:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-20px); }
    }

    /* Fade-out Effect */
    .fade-out {
        animation: fadeOut 0.5s ease-out forwards;
    }

    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; visibility: hidden; }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>

<!-- Loader HTML -->
<div id="loading-container">
    <div id="loading-text">🚀 Welcome! Initializing your experience...</div>
    <div class="balls-container">
        <div class="ball"></div>
        <div class="ball"></div>
        <div class="ball"></div>
    </div>
</div>

<script>
    // Hide the loader when 1/4 of the content is loaded & Show Sidebar
    setTimeout(() => {
        document.getElementById("loading-container").classList.add("fade-out");
        document.querySelector("[data-testid='stSidebar']").style.display = "block";
    }, 1500); // Adjust timing as needed
</script>
"""

loader_placeholder.markdown(loading_animation, unsafe_allow_html=True)

time.sleep(1) 

loader_placeholder.empty()

MODEL_NAME = "llama3.2"

with st.sidebar:
    st.markdown('<div class="sidebar-image">', unsafe_allow_html=True)
    st.image("static/images/Illama.jpeg", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>💬 Chat History</h3>", unsafe_allow_html=True)
    
    st.session_state.illama_search_term = st.text_input("🔍 Search chats", value=st.session_state.illama_search_term)
    
        
    if st.button("➕ New Chat"):
        if st.session_state.illama_messages:
            first_user_message = next((msg["content"] for msg in st.session_state.illama_messages if msg["role"] == "user"), None)
            chat_title = first_user_message[:50] + "..." if first_user_message and len(first_user_message) > 50 else first_user_message or "New Chat"
            
            chat_data = {
                "id": len(st.session_state.illama_chat_history),
                "title": chat_title,
                "messages": st.session_state.illama_messages.copy(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.illama_chat_history.append(chat_data)
            save_chat_history()
        
        st.session_state.illama_messages = [{"role": "assistant", "content": "Hi I'm ILLAMA, your favorite AI assistant! How can I help you today?"}]
        st.session_state.illama_current_chat_id = None
        st.rerun()

    if st.session_state.illama_chat_history:
        for chat in st.session_state.illama_chat_history:
            chat_content = " ".join([msg["content"] for msg in chat["messages"]])
            if st.session_state.illama_search_term.lower() in chat_content.lower():
                col1, col2 = st.columns([8, 1])
                with col1:
                    if st.button(f"📝 {chat['title']} ({chat['timestamp']})", key=f"chat_{chat['id']}"):
                        st.session_state.illama_messages = chat['messages'].copy()
                        st.session_state.illama_current_chat_id = chat['id']
                        st.rerun()
                
                with col2:
                    if st.button("🗑️", key=f"delete_{chat['id']}"):
                        st.session_state.illama_chat_history.remove(chat)
                        save_chat_history()
                        if st.session_state.illama_current_chat_id == chat['id']:
                            st.session_state.illama_current_chat_id = None
                            st.session_state.illama_messages = [{"role": "assistant", "content": "Hi I'm ILLAMA, your favorite AI assistant! How can I help you today?"}]
                        st.rerun()

    st.subheader("⚙️ Settings")
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", st.session_state.get("dark_mode", False))
    st.session_state.font_size = st.slider("🔠 Font Size", 12, 24, st.session_state.get("font_size", 16))

st.markdown("<h1 style='text-align: center;'>💬 ILLAMA Chatbot</h1>", unsafe_allow_html=True)

for idx, msg in enumerate(st.session_state.illama_messages):
    message_class = "user-message" if msg["role"] == "user" else "assistant-message"
    role_prefix = "👤 You: " if msg["role"] == "user" else "🤖 ILLAMA: "
    
    formatted_content = format_message(msg["content"])

    st.markdown(f"""
        <div class="chat-message {message_class}">
            {role_prefix} {formatted_content}
        </div>
    """, unsafe_allow_html=True)

if prompt := st.chat_input("Type your message..."):
    st.session_state.illama_messages.append({"role": "user", "content": prompt})
    st.markdown(f"""
        <div class="chat-message user-message">
            👤 You: {prompt}
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("🤖 ILLAMA is thinking..."):
        response = ollama.chat(model=MODEL_NAME, messages=st.session_state.illama_messages)
        full_message = response['message']['content']
        st.session_state.illama_messages.append({"role": "assistant", "content": full_message})

    st.markdown(f"""
        <div class="chat-message assistant-message">
            🤖 ILLAMA: {full_message}
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.illama_current_chat_id is not None:
        for chat in st.session_state.illama_chat_history:
            if chat['id'] == st.session_state.illama_current_chat_id:
                chat['messages'] = st.session_state.illama_messages.copy()
                chat['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                break

apply_styles()
