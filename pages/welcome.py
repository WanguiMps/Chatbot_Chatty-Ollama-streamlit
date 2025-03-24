import streamlit as st
import time


st.title("Welcome to Chatty Chatbot")



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

# Inject into Streamlit immediately
loader_placeholder.markdown(loading_animation, unsafe_allow_html=True)

# Simulate Page Loading (Content starts appearing)
time.sleep(1)  # Simulating 1/4 of elements loaded

# Remove the loader once content has loaded
loader_placeholder.empty()

import streamlit as st

def logout():
    # Clear session state to end the session
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("landing_page.py")  # Redirect to the landing page

# Custom CSS for styling the logout button
st.markdown(
    """
    <style>
    .logout-button {
        position: absolute;
        top: 10px;
        right: 20px;
        background-color: #ff4b4b;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .logout-button:hover {
        background-color: #cc3a3a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Align button to the right and make it functional
col1, col2 = st.columns([8, 1])
with col2:
    if st.button("Logout", key="logout_btn"):
        logout()



st.markdown(
    """
    <style>
        /* Hide Streamlit default menu */
        #MainMenu {visibility: hidden;}
        
        /* Hide Streamlit header */
        header {visibility: hidden;}
        
        /* Hide footer */
        footer {visibility: hidden;}
         /* Reduce top padding to bring content up */
        .block-container {
            padding-top: 1rem; /* Adjust this value as needed */
        }
    </style>
    """,
    unsafe_allow_html=True
)


button_style = """
    <style>
    .container {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin-top: 20px;
    }
    .big-button {
        width: 220px;
        height: 220px;
        font-size: 18px;
        text-align: center;
        font-weight: bold;
        border: none;
        border-radius: 15px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: 0.3s;
    }
    .gemma { background-color: #007bff; color: white; } /* Blue */
    .llama { background-color: #28a745; color: white; } /* Green */
    .general { background-color: #ffc107; color: black; } /* Yellow */
    .llava { background-color: #8B4513; color: white; } /* Brown */
    .big-button:hover {
        opacity: 0.8;
        transform: scale(1.05);
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)


col1, col2, col3,col4 = st.columns(4)


with col1:
    st.markdown('<button class="big-button gemma">Gemma</button>', unsafe_allow_html=True)
    
    st.page_link("pages/bot2.py", label="Go to Gemma Bot", icon="🤖")

with col2:
    st.markdown('<button class="big-button llama">Llama</button>', unsafe_allow_html=True)
    
    st.page_link("pages/bot3.py", label="Go to Llama Bot", icon="🦙")

with col3:
    st.markdown('<button class="big-button general">Deepseek</button>', unsafe_allow_html=True)
    
    st.page_link("pages/bot1.py", label="Deepseek", icon="🌊")

with col4:
    st.markdown('<button class="big-button llava">Llava</button>', unsafe_allow_html=True)
    
    st.page_link("pages/bot4.py", label="Go to Llava Bot", icon="🖼️")



if "theme_color" not in st.session_state:
    st.session_state.theme_color = "#C0C0CE"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "font_size" not in st.session_state:
    st.session_state.font_size = 16


def apply_custom_styles():
    if st.session_state.dark_mode:
        background_color = "#1E1E1E"
        text_color = "#FFFFFF"
    else:
        background_color = st.session_state.theme_color
        text_color = "#000000"

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

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)