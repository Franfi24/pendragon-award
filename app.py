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

    /* DROPDOWNS: FORCE WHITE BOX, BLACK TEXT */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
    }
    
    /* Force text inside white boxes to be black */
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    h1 {
        text-align: left !important;
        margin-bottom: 0 !important;
        font-size: 2.2rem !important;
    }

    label, [data-testid="stWidgetLabel"] {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-align: left !important;
    }

    /* BUTTON: SMALL, BLACK, LEFT ALIGNED */
    div.stButton > button {
        width: auto !important;
        padding: 0px 20px !important;
        border-radius: 12px;
        background-color: #000000 !important; 
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        height: 2.5rem !important;
        font-size: 0.8rem !important;
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

def get_voters():
    try:
        result = supabase.table(TABLE_NAME).select("Name").execute()
        return [row['Name'] for row in result.data]
    except Exception:
        return []

voted_names = get_voters()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 4. LOGIN ---
if not st.session_state.authenticated:
    # Small ball fix and Title
    st.markdown("<h1>Pendragon Awards <span style='font-size: 1.5rem;'>🏀</span></h1>", unsafe_allow_html=True)
    st.write("Official 2026 Voting Portal")
    
    st.divider()
    
    # Three sentences stacked vertically
    st.write("Welcome to the Pendragon Ballot!")
    st.write("Please Select your Team and find your name in the dropdown menu.")
    st.write("Each Pendragon Member can only vote once!")
    
    st.divider()

    team = st.selectbox("WHICH TEAM ARE YOU IN?", options=[""] + list(roster.keys()))

    if team:
        available_names = [n for n in roster[team] if n not in voted_names]
        
        if not available_names:
            st.warning("All players on this team have voted! 🎉")
        else:
            name = st.selectbox("SELECT YOUR NAME", options=[""] + available_names)

            if name != "":
                btn_col, _ = st.columns([1, 2])
                with btn_col:
                    if st.button("VERIFY & ENTER"):
                        st
