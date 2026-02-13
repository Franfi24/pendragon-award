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

# --- 2. THEME & MOBILE STYLING (Original Red) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #8B0000 0%, #D32F2F 100%);
        color: #ffffff;
    }
    /* Logo and Title Alignment */
    [data-testid="column"]:nth-child(2) { margin-left: -25px !important; }
    [data-testid="stHorizontalBlock"] { align-items: center; }
    
    label, p, [data-testid="stWidgetLabel"] { color: white !important; font-weight: 600; }

    /* Button Styling */
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
    
    /* Input/Selectbox Styling */
    .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #000000 !important;
        border-radius: 10px;
    }

    h1 { font-size: 1.8rem !important; white-space: nowrap; color: white !important; }
    h3 { color: white !important; }
    hr { border-top: 1px solid rgba(255, 255, 255, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA (Roster & Awards) ---
roster = {
    "Ladies 1": ["Maria", "Sarah", "Elena", "Coach Jo"],
    "Ladies 2": ["Maria", "Sarah", "Elena", "Coach Jo"],
    "Men's 1": ["Tom", "Jake", "Ryan", "Pete"],
    "Men's 2": ["Alex", "Jordan", "Chris", "Big Steve"],
}

awards_list = [
    "🏆 Most Valuable Player (MVP)",
    "📈 Most Improved Player",
    "🛡️ Best Defensive Player",
    "🔥 Pendragon Spirit Award"
]

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 4. LOGIN INTERFACE ---
if not st.session_state.authenticated:
    col1, col2 = st.columns([1, 5])
    with col1:
        logo_path = os.path.join("images", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
        else:
            st.write("🏀")
    with col2:
        st.markdown("# Pendragon Awards")

    st.write("Official voting app for Pendragon Basketball")
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

# --- 5. VOTING INTERFACE ---
else:
    col1, col2 = st.columns([1, 5])
    with col1:
        logo_path = os.path.join("images", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=60)
    with col2:
        st.markdown(f"### WELCOME, {st.session_state.user_name.upper()}!")

    st.write(f"Voting for: **{st.session_state.user_team}**")
    st.divider()

    st.subheader("Cast Your Votes 🗳️")
    
    with st.form("voting_form"):
        user_votes = {}
        
        for award in awards_list:
            user_votes[award] = st.selectbox(
                f"Vote for: {award}",
                options=[""] + roster[st.session_state.user_team],
                key=f"vote_{award}"
            )
        
        st.write(" ")
        submit_button = st.form_submit_button("SUBMIT ALL VOTES")

        if submit_button:
            # Check if all categories were filled
            if all(val != "" for val in user_votes.values()):
                try:
                    for award_name, selection in user_votes.items():
                        supabase.table(TABLE_NAME).insert({
                            "Name": st.session_state.user_name,
                            "Team": st.session_state.user_team,
                            "Award": award_name,
                            "Selection": selection
                        }).execute()
                    
                    st.success("SUCCESS! Your votes have been counted. 🏀")
                    st.balloons()
                except Exception as e:
                    st.error(f"Sync Error: {e}")
            else:
                st.warning("Please pick a player for every category!")

    st.divider()
    if st.button("LOG OUT"):
        st.session_state.clear()
        st.rerun()
