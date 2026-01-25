import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os
import base64

# ================= PAGE CONFIG (FOR WIDER COLUMNS) =================
st.set_page_config(layout="wide")

# ================= THEME STATE =================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "show_saved" not in st.session_state:
    st.session_state.show_saved = False


def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"


def set_winter():
    st.session_state.theme = "winter"


# ================= WINTER VIDEO BACKGROUND =================
def get_base64_video(video_path):
    with open(video_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ================= NEON BUTTON STYLING =================
# This CSS adds a neon glow to all buttons and ensures text is sharp
st.markdown("""
    <style>
    div.stButton > button {
        border: 2px solid #00f2ff !important;
        border-radius: 10px !important;
        color: white !important;
        background-color: rgba(0, 0, 0, 0.4) !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff !important;
        box-shadow: 0 0 10px #00f2ff, inset 0 0 5px #00f2ff !important;
        transition: 0.3s all ease-in-out !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 20px #00f2ff, inset 0 0 10px #00f2ff !important;
        transform: scale(1.02) !important;
    }
    /* Specific styling for the 'Generate' button to make it even more visible */
    div.stButton > button:active {
        background-color: #00f2ff !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# ================= CSS THEMES (FIXED VISIBILITY) =================
if st.session_state.theme == "winter":
    if os.path.exists("gif.mp4"):
        video_base64 = get_base64_video("gif.mp4")
        st.markdown(f"""
            <style>
            #bg-video {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                object-fit: cover;
                z-index: -100;
            }}
            .stApp {{
                background: transparent;
            }}
            label, .stMarkdown p, .stSubheader, .stTitle {{
                color: white !important;
                text-shadow: 2px 2px 10px black;
            }}
            </style>

            <video autoplay loop muted playsinline id="bg-video">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        """, unsafe_allow_html=True)
    else:
        st.warning("gif.mp4 not found in project folder")

elif st.session_state.theme == "dark":
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: white; }
        label, .stMarkdown p, .stSubheader, .stTitle {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: white; color: black; }
        </style>
    """, unsafe_allow_html=True)

# ================= THEME BUTTONS =================
c1, c2, c3 = st.columns(3)
c1.button("🌙 Dark / ☀️ Light", on_click=toggle_theme)
c3.button("❄️ Winter Theme", on_click=set_winter)

# ================= PASSWORD DATA =================
letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
numbers = list("0123456789")
symbols = ['!', '@', '#', '$', '%', '^', '&', '*', ',', '+']

# ================= UI =================
st.title("Welcome to my Project Number 5 🔐")

name = st.text_input("Please enter your name")

app_name = st.text_input(
    "App or Website where you are going to use this password"
)

in_letter = st.number_input("Enter number of letters:", min_value=0, step=1)
in_number = st.number_input("How many numbers?", min_value=0, step=1)
in_symbol = st.number_input("How many symbols?", min_value=0, step=1)

# ================= GENERATE PASSWORD =================
if st.button("Generate Password 🔑"):
    password = ""
    for _ in range(in_letter):
        password += random.choice(letters)
    for _ in range(in_number):
        password += random.choice(numbers)
    for _ in range(in_symbol):
        password += random.choice(symbols)

    st.session_state.generated_password = password
    st.success(f"Your password is: **{password}**")

    user_name = name if name.strip() else "User"
    st.info(f"THANK YOU {user_name.upper()} FOR USING OUR PASSWORD GENERATOR")

# ================= SAVE PASSWORD =================
file_name = "saved_passwords.xlsx"

HEADERS = ["Name", "Password", "Date & Time", "App / Website Name"]

if "generated_password" in st.session_state:
    if st.button("💾 Save Password"):
        if not name:
            st.warning("Please enter your name before saving.")
        else:
            safe_app_name = app_name if app_name.strip() else "Not Provided"

            new_row = pd.DataFrame([{
                "Name": name,
                "Password": st.session_state.generated_password,
                "Date & Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "App / Website Name": safe_app_name
            }])

            if os.path.exists(file_name):
                old_df = pd.read_excel(file_name, engine='openpyxl')
                df = pd.concat([old_df, new_row], ignore_index=True)
            else:
                df = pd.DataFrame(columns=HEADERS)
                df = pd.concat([df, new_row], ignore_index=True)

            df.to_excel(file_name, index=False, engine='openpyxl')

            st.session_state.show_saved = True
            st.success("Password saved successfully! ✅")
            st.balloons()
            st.info(f"THANK YOU {name.upper()} FOR USING OUR PASSWORD GENERATOR")

# ================= VIEW & DELETE PASSWORDS =================
if st.session_state.show_saved and os.path.exists(file_name):
    st.subheader("📄 Saved Passwords")

    excel_data = pd.read_excel(file_name, engine='openpyxl')

    if not excel_data.empty:
        st.dataframe(excel_data, use_container_width=True, hide_index=True)

        with st.expander("🗑 Delete Passwords"):
            for index, row in excel_data.iterrows():
                del_c1, del_c2 = st.columns([4, 1])
                del_c1.write(f"**{row['App / Website Name']}** ({row['Name']})")
                if del_c2.button("🗑", key=f"delete_{index}"):
                    excel_data.drop(index, inplace=True)
                    excel_data.reset_index(drop=True, inplace=True)
                    excel_data.to_excel(file_name, index=False, engine='openpyxl')
                    st.rerun()
    else:
        st.info("No saved passwords found.")

# ================= FOOTER =================
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: gray;'>©️Made by Ansh Raj</h4>", unsafe_allow_html=True)
