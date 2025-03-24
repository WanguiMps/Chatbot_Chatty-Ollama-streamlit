import streamlit as st

st.title("Settings ⚙️")

if "theme_color" not in st.session_state:
    st.session_state.theme_color = "#030312"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "font_size" not in st.session_state:
    st.session_state.font_size = 16
if "notif_sound" not in st.session_state:
    st.session_state.notif_sound = True

selected_color = st.color_picker("Choose your theme color:", st.session_state.theme_color)
if selected_color != st.session_state.theme_color:
    st.session_state.theme_color = selected_color
    st.rerun()

dark_mode = st.checkbox("Enable Dark Mode", st.session_state.dark_mode)
if dark_mode != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_mode
    st.rerun()

font_size = st.slider("Adjust Font Size:", min_value=12, max_value=30, value=st.session_state.font_size)
if font_size != st.session_state.font_size:
    st.session_state.font_size = font_size
    st.rerun()

notif_sound = st.checkbox("Enable Notification Sound", st.session_state.notif_sound)
st.session_state.notif_sound = notif_sound

if st.button("Reset to Default ⚠️"):
    st.session_state.theme_color = "#C0C0CE"
    st.session_state.dark_mode = False
    st.session_state.font_size = 16
    st.session_state.notif_sound = True
    st.rerun()

background_color = "#1E1E1E" if st.session_state.dark_mode else st.session_state.theme_color
text_color = "white" if st.session_state.dark_mode else "black"

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {background_color};
            color: {text_color};
            font-size: {st.session_state.font_size}px;
        }}
        .stButton > button {{
            font-size: {st.session_state.font_size}px;
        }}
        .stTextInput > div > input {{
            font-size: {st.session_state.font_size}px;
        }}
        .stSelectbox > div > div > div {{
            font-size: {st.session_state.font_size}px;
        }}
        .stSlider > div > div > div {{
            font-size: {st.session_state.font_size}px;
        }}
        .stCheckbox > div > div > div {{
            font-size: {st.session_state.font_size}px;
        }}
        .stRadio > div > div > div {{
            font-size: {st.session_state.font_size}px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.success(f"Settings updated! Theme color: {st.session_state.theme_color}, Dark mode: {'On' if st.session_state.dark_mode else 'Off'}, Font size: {st.session_state.font_size}px.")

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
