import streamlit as st
from supabase import create_client, Client
import os

# --- 0. SUPABASE CONFIG ---
SUPABASE_URL = "https://gkrkdujyuzcdoneuoakr.supabase.co"
SUPABASE_KEY = "sb_publishable_R20QEdVZMJuy8AiPBETy0g_R62okepN"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "Pendragon Awards 2026"

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Pendragon Awards",
    page_icon="🏀",
    layout="centered"
)

# --- 2. THEME & MOBILE TWEAKS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #8B0000 0%, #D32F2F 100%);
        color: #ffffff;
    }

    /* Pulls the second column (title) closer to the first column (logo) */
    [data-testid="column"]:nth-child(2) {
        margin-left: -25px !important;
    }

    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }

    label, p, [data-testid="stWidgetLabel"] {
        color: white !important;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background-color: #000000; 
        color: #ffffff;
        border: 2px solid #ffffff;
        font-weight: 700;
        text-transform: uppercase;
        height: 3.5rem;
    }

    .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        border-radius: 10px;
    }

    h1 {
        font-size: 1.8rem !important;
        white-space: nowrap; /* Prevents title from jumping to next line */
    }

    hr { border-top: 1px solid rgba(255, 255, 255, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ---
roster = {
    "Ladies 1": ["Maria", "Sarah", "Elena", "Coach Jo"],
    "Ladies 2": ["Maria", "Sarah", "Elena", "Coach Jo"],
    "Men's 1": ["Tom", "Jake", "Ryan", "Pete"],
    "Men's 2": ["Alex", "Jordan", "Chris", "Big Steve"],
}

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 4. LOGIN ---
if not st.session_state.authenticated:
    # Header Row
    t_col1, t_col2 = st.columns([1, 5])
    with t_col1:
        logo_path = os.path.join("images", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)  # Made the logo bigger
    with t_col2:
        st.markdown("# Pendragon Awards 🏀")

    st.write("Official voting app")
    st.divider()

    team = st.selectbox("WHICH TEAM ARE YOU IN?", options=[""] + list(roster.keys()))

    if team:
        name = st.selectbox("SELECT YOUR NAME", options=[""] + roster[team])

        if st.button("VERIFY & ENTER"):
            if name:
                st.session_state.user_name = name
                st.session_state.user_team = team
                st.session_state.authenticated = True
                st.rerun()

# --- 5. THE SYNC & SUCCESS ---
else:
    # Header Row for Welcome Page
    t_col1, t_col2 = st.columns([1, 5])
    with t_col1:
        logo_path = os.path.join("images", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=60)
    with t_col2:
        st.markdown(f"### WELCOME, {st.session_state.user_name.upper()}!")

    if 'logged_entry' not in st.session_state:
        try:
            entry_data = {
                "Name": st.session_state.user_name,
                "Team": st.session_state.user_team,
                "Selection": "Login Success",
                "Award": "Design Polish"
            }
            supabase.table(TABLE_NAME).insert(entry_data).execute()
            st.session_state.logged_entry = True
            st.toast("Logged in!✅ ")
        except Exception as e:
            st.error(f"Sync Error: {e}")

    st.write(f"Logged in as: **{st.session_state.user_team}**")
    st.divider()

    if st.button("LOG OUT"):
        st.session_state.clear()
        st.rerun()
