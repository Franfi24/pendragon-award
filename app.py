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
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(180deg, #8B0000 0%, #D32F2F 100%);
        color: #ffffff;
    }

    /* 1. MAKE DROPDOWNS WHITE WITH BLACK TEXT */
    /* This targets the main box */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 10px !important;
        border: none !important;
    }

    /* This targets the text inside the dropdown when selected */
    div[data-baseweb="select"] * {
        color: #000000 !important;
    }
    
    /* This ensures the placeholder text (like "Select your name") is also visible */
    div[role="listbox"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* 2. PROGRESS BAR COLOR */
    /* This makes the progress bar a bright white/silver or gold so it pops */
    .stProgress > div > div > div > div {
        background-color: #FFFFFF !important;
    }

    /* Label text (the questions above dropdowns) */
    label, p, [data-testid="stWidgetLabel"] {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* 3. BUTTON STYLING */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        background-color: #000000 !important; 
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        font-weight: 700;
        text-transform: uppercase;
        height: 3.5rem;
        margin-top: 10px;
    }

    div.stButton > button {
        height: 2.5rem !important; /* Shorter height */
        font-size: 0.8rem !important; /* Smaller text */
        padding: 0px 10px !important;
    }
    
    div.stButton > button:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

   h1 {
        text-align: left !important;
        margin-left: 0 !important;
        margin-right: auto !important;
        width: 100% !important;
        display: block !important;
    }

    hr { border-top: 1px solid rgba(255, 255, 255, 0.3); }
    </style>
    """, unsafe_allow_html=True)

   /* This makes the info box background invisible */
    div.stAlert {
        background-color: transparent !important;
        border: none !important;
        padding-left: 0 !important; /* Aligns text perfectly to the left */
        margin-bottom: -20px !important; /* Pulls the divider closer */
    }

    /* This forces the text to be white and clean */
    div.stAlert p {
        color: #FFFFFF !important;
        font-weight: 400 !important;
        font-size: 1.05rem !important;
        line-height: 1.5 !important;
    }
# --- 3. DATA ---
roster = {
    "Ladies 1": ["Maria", "Sarah", "Elena", "Coach Jo"],
    "Ladies 2": ["Maria", "Sarah", "Elena", "Coach Jo"],
    "Men's 1": ["Tom", "Jake", "Ryan", "Pete"],
    "Men's 2": ["Alex", "Jordan", "Chris", "Big Steve"],
}

# --- ADDED: Function to see who already voted ---
def get_voters():
    try:
        # Fetches only the 'Name' column from your Supabase table
        result = supabase.table(TABLE_NAME).select("Name").execute()
        return [row['Name'] for row in result.data]
    except Exception:
        return []

# Get the list of names that already exist in the database
voted_names = get_voters()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 4. LOGIN ---
if not st.session_state.authenticated:
    st.markdown("# Pendragon Awards 🏀") # No columns, just straight text
    st.write("Official 2026 Voting Portal")
    st.divider()
    st.divider()

    st.info("""
    Welcome to the Pendragon Ballot! 
    Please Select your Team and find your name in the dropdown menu.
    Each Pendragon Member can only vote once. 
    """)

    team = st.selectbox("WHICH TEAM ARE YOU IN?", options=[""] + list(roster.keys()))
    
    if team:
        available_names = [n for n in roster[team] if n not in voted_names]
        
        if not available_names:
            st.warning("All players on this team have voted! 🎉")
        else:
            name = st.selectbox("SELECT YOUR NAME", options=[""] + available_names)

            if name != "":
                # Keep the button small and on the left
                btn_col, _ = st.columns([1, 2])
                with btn_col:
                    if st.button("VERIFY & ENTER"):
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
