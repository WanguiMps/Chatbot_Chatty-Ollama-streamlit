import streamlit as st
import sqlite3
import hashlib
from PIL import Image
import time

st.set_page_config(page_title="Chatty Chatbot", layout="wide")




st.markdown(
    """
    <style>
        /* Hide Streamlit default menu */
        #MainMenu {visibility: hidden;}
        
        /* Hide Streamlit header */
        header {visibility: hidden;}
        
        /* Hide footer */
        footer {visibility: hidden;}
        
        /* Hide Sidebar - More specific selector to ensure it's always hidden */
        section[data-testid="stSidebar"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
        }
        
        /* Reduce top padding to bring content up */
        .block-container {
            padding-top: 1rem; /* Adjust this value as needed */
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

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
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

time.sleep(1)  

loader_placeholder.empty()
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    username TEXT UNIQUE,
                    dob TEXT,
                    password TEXT)''')
    conn.commit()
    conn.close()

def add_user(name, username, dob, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, username, dob, password) VALUES (?, ?, ?, ?)",
                  (name, username, dob, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user  


create_user_table()


st.markdown("""
    <div class="fade-in">
        <h1>Chatty Chatbot</h1>
        <p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
            Your Trusted AI Chatbot
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
        <h2 style="color: var(--primary-color); margin-bottom: 1rem;">Introduction</h2>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            Welcome to our AI-powered chatbot system! 🤖 This platform lets you interact with different AI models, 
            compare their responses, and explore their capabilities.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            <strong>Choose from:</strong> <span style="color: var(--secondary-color);">DeepSeek, Gemma, or Llama</span> 
            to experience diverse AI interactions.
        </p>
        <ul style="font-size: 1.1rem; line-height: 1.6; padding-left: 1.5rem;">
            <li>Select a chatbot to start a conversation.</li>
            <li>Each AI has unique strengths—explore and compare them!</li>
            <li>Type your question and receive real-time responses.</li>
        </ul>
        <p style="font-size: 1.1rem; line-height: 1.6;">
            Get started by selecting an AI model and enjoy the experience! 
        </p>
    """, unsafe_allow_html=True)


with col2:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Robot/3D/robot_3d.png", width=400)
    st.markdown('</div>', unsafe_allow_html=True)

get_started_col1, get_started_col2 = st.columns([1, 2])

with get_started_col1:
    st.image("static/images/landing.jpeg", width=250)

with get_started_col2:
    st.markdown("""
        <div style="padding: 2rem; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <h2 style="color: var(--primary-color); font-size: 2.5rem; margin-bottom: 1rem;">Ready to Get Started?</h2>
            <p style="color: #666; font-size: 1.2rem; margin-bottom: 2rem;">Get started with us in seconds</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    div.stButton > button {
        background: white !important;
        background-color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.8rem 2rem !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        width: auto !important;
        margin: 0 auto !important;
        display: block !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    
    div.stButton > button span {
        background: linear-gradient(90deg, #2E3192, #1BFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("LOGIN / SIGN UP", key="cta_login"):
    st.session_state.show_expander = not st.session_state.show_expander

st.markdown(
    """
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
    }
    body {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: #444;
    }
    .container {
        position: relative;
        width: 70vw;
        height: auto;
        background: #fff;
        border-radius: 15px;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3), 0 6px 20px 0 rgba(0, 0, 0, 0.3);
        padding: 20px;
        text-align: center;
    }
    .input-field {
        position: relative;
        width: 100%;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        background: #f0f0f0;
        border: 2px solid #15e4d0;
        border-radius: 50px;
        padding: 10px;
    }
    .input-field i {
        margin-right: 10px;
        color: #666;
        font-size: 18px;
    }
    .input-field input {
        flex: 1;
        border: none;
        outline: none;
        background: none;
        font-size: 16px;
        color: #444;
        padding: 8px;
    }
    .btn {
        width: 150px;
        height: 50px;
        border: none;
        border-radius: 50px;
        background: rgb(3, 13, 15);
        color: #fff;
        font-weight: 600;
        margin-top: 10px;
        text-transform: uppercase;
        cursor: pointer;
        transition: 0.3s;
    }
    .btn:hover {
        background: #40a2b1;
    }
    </style>
    """,
    unsafe_allow_html=True
)



if "show_expander" not in st.session_state:
    st.session_state.show_expander = False


st.markdown("""
    <style>
    /* Modern Glassmorphism Effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    /* Enhanced Input Fields */
    .input-field {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
    }

    .input-field:hover {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(46, 49, 146, 0.1);
    }

    .input-field i {
        font-size: 1.2rem;
        margin-right: 1rem;
        color: var(--primary-color);
    }

    .input-field input {
        border: none;
        background: none;
        width: 100%;
        font-size: 1rem;
        color: #333;
        outline: none;
    }

    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    /* Enhanced Card Styling */
    .stCard {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }

    .stCard:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }

    /* Enhanced Model Cards */
    .model-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .model-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }

    .model-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }

    .model-card img {
        border-radius: 15px;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }

    .model-card:hover img {
        transform: scale(1.05);
    }

    /* Enhanced Radio Buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }

    /* Success Message Styling */
    .stSuccess {
        background: rgba(76, 175, 80, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(76, 175, 80, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.show_expander:
    with st.expander("Login / Sign Up", expanded=True):
        st.title("Welcome to Chatty Chatbot")
        
        choice = st.radio("Select an option:", ["Login", "Sign Up"])

        if choice == "Sign Up":
            st.subheader("Create Your Account")
            
            name = st.text_input("Full Name")
            username = st.text_input("Username")
            dob = st.date_input("Date of Birth")
            password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.button("Create Account", key="signup"):
                if password == confirm_password:
                    if add_user(name, username, str(dob), password):
                        st.success("🎉 Account created successfully! You can now log in.")
                    else:
                        st.error("Username already exists. Please choose a different username.")
                else:
                    st.error("Passwords do not match. Please try again.")

        elif choice == "Login":
            st.subheader("Welcome Back")
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login", key="login"):
                user = check_user(username, password)
                if user:
                    st.session_state.user_name = user[1] 
                    st.success("🎉 Welcome back! You are now logged in.")
                    st.switch_page("pages/welcome.py")
                else:
                    st.error("Invalid username or password. Please try again.")


st.markdown("""
    <h2 style="text-align: center; color: var(--primary-color); margin: 4rem 0 2rem; font-size: 2.5rem;">
        Meet Illava
    </h2>
""", unsafe_allow_html=True)

illava_col1, illava_col2 = st.columns([1, 3])

with illava_col1:
    st.markdown("""
        <div style="max-width: 300px; margin: auto;">
    """, unsafe_allow_html=True)
    st.image("static/images/llava2.jpg", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with illava_col2:
    st.markdown("""
        <div class="glass-container" style="padding: 2rem;">
            <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; font-size: 2rem;">
                Multimodal AI Assistant
            </h3>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #444;">
                Illava is a powerful multimodal AI assistant that can understand and process both text and images, 
                making it versatile for various tasks and interactions.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <h2 style="text-align: center; color: var(--primary-color); margin: 4rem 0 2rem; font-size: 2.5rem;">
        Meet Illama
    </h2>
""", unsafe_allow_html=True)

illama_col1, illama_col2 = st.columns([1, 3])

with illama_col1:
    st.markdown("""
        <div style="max-width: 300px; margin: auto;">
    """, unsafe_allow_html=True)
    st.image("static/images/Illama.jpeg", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with illama_col2:
    st.markdown("""
        <div class="glass-container" style="padding: 2rem;">
            <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; font-size: 2rem;">
                Efficient Language Model
            </h3>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #444;">
                Illama is an efficient and powerful language model optimized for speed and resource usage, 
                making it perfect for real-time applications and edge computing.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <h2 style="text-align: center; color: var(--primary-color); margin: 4rem 0 2rem; font-size: 2.5rem;">
        Meet Deepseek
    </h2>
""", unsafe_allow_html=True)

deepseek_col1, deepseek_col2 = st.columns([1, 3])

with deepseek_col1:
    st.markdown("""
        <div style="max-width: 300px; margin: auto;">
    """, unsafe_allow_html=True)
    st.image("static/images/deepseek.jpg", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with deepseek_col2:
    st.markdown("""
        <div class="glass-container" style="padding: 2rem;">
            <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; font-size: 2rem;">
                Advanced Reasoning AI
            </h3>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #444;">
                Deepseek excels in complex problem-solving and reasoning tasks, with advanced capabilities 
                in code generation and research assistance.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <h2 style="text-align: center; color: var(--primary-color); margin: 4rem 0 2rem; font-size: 2.5rem;">
        Meet Gemma
    </h2>
""", unsafe_allow_html=True)

gemma_col1, gemma_col2 = st.columns([1, 3])

with gemma_col1:
    st.markdown("""
        <div style="max-width: 200px; margin: auto;">
    """, unsafe_allow_html=True)
    st.image("static/images/gemma.png", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with gemma_col2:
    st.markdown("""
        <div class="glass-container" style="padding: 2rem;">
            <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; font-size: 2rem;">
                Google's Multimodal Model
            </h3>
            <p style="font-size: 1.1rem; line-height: 1.8; color: #444;">
                Gemma is Google's advanced multimodal model that combines text and image understanding 
                with powerful reasoning capabilities for comprehensive AI interactions.
            </p>
        </div>
    """, unsafe_allow_html=True)

if "theme_color" not in st.session_state:
    st.session_state.theme_color = "#C0C0CE"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "font_size" not in st.session_state:
    st.session_state.font_size = 16

def apply_custom_styles():
    background_color = "#1E1E1E" if st.session_state.dark_mode else st.session_state.theme_color
    text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"

    st.markdown(f"""
        <style>
            .stApp {{
                background-color: {background_color};
                color: {text_color};
                font-size: {st.session_state.font_size}px;
            }}
            div.stButton > button {{
                background-color: {st.session_state.theme_color};
                color: {text_color};
                font-size: {st.session_state.font_size}px;
            }}
        </style>
        """, unsafe_allow_html=True)

apply_custom_styles()
