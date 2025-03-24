import streamlit as st
import ollama
import time
from datetime import datetime
import json
import re
from PIL import Image
import io
import base64

st.set_page_config(page_title="LLAVA Chatbot", layout="wide")

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
    with open("chat_history.json", "w") as f:
        json.dump(st.session_state.chat_history, f)

def load_chat_history():
    try:
        with open("chat_history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

if "llava_chat_history" not in st.session_state:
    st.session_state.llava_chat_history = load_chat_history()

if "llava_current_chat_id" not in st.session_state:
    st.session_state.llava_current_chat_id = None

if "llava_messages" not in st.session_state:
    user_name = st.session_state.get("user_name", "")
    welcome_message = f"Hi {user_name}! I'm LLaVA, your visual AI assistant! How can I help you today? You can send me both text and images!" if user_name else "Hi I'm LLaVA, your visual AI assistant! How can I help you today? You can send me both text and images!"
    st.session_state.llava_messages = [{"role": "assistant", "content": welcome_message}]

if "llava_search_term" not in st.session_state:
    st.session_state.llava_search_term = ""

if "llava_uploaded_image" not in st.session_state:
    st.session_state.llava_uploaded_image = None

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
    </style>
    """,
    unsafe_allow_html=True
)

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

loader_placeholder = st.empty()

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

time.sleep(1)  # Simulating 1/4 of elements loaded

loader_placeholder.empty()

MODEL_NAME = "llava"
MODEL_CONFIG = {
    "model": MODEL_NAME,
    "temperature": 0.7,
    "system": """You are LLaVA, a helpful visual AI assistant that excels at understanding and analyzing both images and text. 
    You can:
    - Analyze images in detail
    - Answer questions about images
    - Compare multiple images
    - Provide descriptions and explanations
    - Help with visual tasks and identification
    Please be specific and detailed in your image analysis."""
}

with st.sidebar:
    st.markdown('<div class="sidebar-image">', unsafe_allow_html=True)
    st.image("static/images/llava.jpg", width=150, use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>💬 Chat History</h3>", unsafe_allow_html=True)
    
    st.session_state.llava_search_term = st.text_input("🔍 Search chats", value=st.session_state.llava_search_term)
    
    if st.button("➕ New Chat"):
        if st.session_state.llava_messages:
            first_user_message = next((msg["content"] for msg in st.session_state.llava_messages if msg["role"] == "user"), None)
            chat_title = first_user_message[:50] + "..." if first_user_message and len(first_user_message) > 50 else first_user_message or "New Chat"
            
            chat_data = {
                "id": len(st.session_state.llava_chat_history),
                "title": chat_title,
                "messages": st.session_state.llava_messages.copy(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.llava_chat_history.append(chat_data)
            save_chat_history()
        
        st.session_state.llava_messages = [{"role": "assistant", "content": "Hi I'm LLaVA, your visual AI assistant! How can I help you today? You can send me both text and images!"}]
        st.session_state.llava_current_chat_id = None
        st.rerun()

    if st.session_state.llava_chat_history:
        for chat in st.session_state.llava_chat_history:
            chat_content = " ".join([msg["content"] for msg in chat["messages"]])
            if st.session_state.llava_search_term.lower() in chat_content.lower():
                col1, col2 = st.columns([8, 1])
                with col1:
                    if st.button(f"📝 {chat['title']} ({chat['timestamp']})", key=f"chat_{chat['id']}"):
                        st.session_state.llava_messages = chat['messages'].copy()
                        st.session_state.llava_current_chat_id = chat['id']
                        st.rerun()
                
                with col2:
                    if st.button("🗑️", key=f"delete_{chat['id']}"):
                        st.session_state.llava_chat_history.remove(chat)
                        save_chat_history()
                        if st.session_state.llava_current_chat_id == chat['id']:
                            st.session_state.llava_current_chat_id = None
                            st.session_state.llava_messages = [{"role": "assistant", "content": "Hi I'm LLaVA, your visual AI assistant! How can I help you today? You can send me both text and images!"}]
                        st.rerun()

    if st.session_state.llava_messages and len(st.session_state.llava_messages) > 1:
        st.subheader("💾 Export Chat")
        if st.button("Export as Text"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_export_{timestamp}.txt"
            export_as_text(st.session_state.llava_messages, filename)
            st.success(f"Chat exported as {filename}")

    st.subheader("⚙️ Settings")
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", st.session_state.get("dark_mode", False))
    st.session_state.font_size = st.slider("🔠 Font Size", 12, 24, st.session_state.get("font_size", 16))

st.markdown("<h1 style='text-align: center;'>💬 LLaVA Visual Assistant</h1>", unsafe_allow_html=True)

for idx, msg in enumerate(st.session_state.llava_messages):
    message_class = "user-message" if msg["role"] == "user" else "assistant-message"
    role_prefix = "👤 You: " if msg["role"] == "user" else "🤖 LLaVA: "
    
    formatted_content = format_message(msg["content"])

    image_html = ""
    if "image" in msg:
        image_html = f'<img src="data:image/jpeg;base64,{msg["image"]}" style="max-width: 300px; border-radius: 10px; margin: 10px 0;">'

    st.markdown(f"""
        <div class="chat-message {message_class}">
            {role_prefix} {formatted_content}
            {image_html}
        </div>
    """, unsafe_allow_html=True)

def process_image(uploaded_file, max_width=800, quality=85):
    try:
        image = Image.open(uploaded_file)
        
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        if image.width > max_width:
            ratio = max_width / image.width
            new_size = (max_width, int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
        img_byte_arr = img_byte_arr.getvalue()
        
        return base64.b64encode(img_byte_arr).decode()
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        prompt = st.chat_input("Ask me about any image or type your message...")
    
    with col2:
        uploaded_file = st.file_uploader(
            "📷 Upload Image", 
            type=['png', 'jpg', 'jpeg'], 
            key="image_uploader",
            help="Upload an image to analyze"
        )

if prompt or uploaded_file:
    message_content = prompt if prompt else "Please analyze this image."
    message_image = process_image(uploaded_file) if uploaded_file else None
    
    user_message = {"role": "user", "content": message_content}
    if message_image:
        user_message["image"] = message_image
    st.session_state.llava_messages.append(user_message)
    
    image_html = f'<img src="data:image/jpeg;base64,{message_image}" style="max-width: 300px; border-radius: 10px; margin: 10px 0;">' if message_image else ""
    st.markdown(f"""
        <div class="chat-message user-message">
            👤 You: {message_content}
            {image_html}
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("🤖 LLaVA is thinking..."):
        try:
            messages_for_model = []
            for msg in st.session_state.llava_messages:
                model_msg = {"role": msg["role"], "content": msg["content"]}
                if "image" in msg:
                    model_msg["images"] = [msg["image"]]
                messages_for_model.append(model_msg)
            
            response = ollama.chat(
                model=MODEL_NAME,
                messages=messages_for_model,
                options=MODEL_CONFIG
            )
            full_message = response['message']['content']
            st.session_state.llava_messages.append({"role": "assistant", "content": full_message})
        except Exception as e:
            error_message = f"Error communicating with the model: {str(e)}"
            st.error(error_message)
            st.session_state.llava_messages.append({"role": "assistant", "content": "I apologize, but I encountered an error processing your request. If you shared an image, please make sure it's in a supported format (JPG, PNG) and try again."})
            full_message = "Error: " + error_message

    st.markdown(f"""
        <div class="chat-message assistant-message">
            🤖 LLaVA: {full_message}
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.llava_current_chat_id is not None:
        for chat in st.session_state.llava_chat_history:
            if chat['id'] == st.session_state.llava_current_chat_id:
                chat['messages'] = st.session_state.llava_messages.copy()
                chat['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                break

apply_styles()
