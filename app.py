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
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] * {
        color: #000000 !important;
    }
    h1 {
        text-align: left !important;
        font-size: 2.2rem !important;
    }
    label, p, [data-testid="stWidgetLabel"] {
        color: white !important;
        font-weight: 700 !important;
    }
    div.stButton > button {
        background-color: #000000 !important; 
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 12px;
        text-transform: uppercase;
        font-weight: 700;
    }
    hr { border-top: 1px solid rgba(255, 255, 255, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ---
roster = {
    "Ladies 1": ["Ida", "Ilinca", "Imke", "Iris", "Janne", "Lise", "Margherita", "Rachne", "Susanna", "Zey", "Zeynep", "Zoë"],
    "Men's 3": ["Albert", "Dani", "Demir", "Eugen", "Francesco", "Gundars", "Hugo", "Jesper", "Quinn", "Rayan", "Terence", "Tuna"],
}

# Fetch names that already exist in Supabase
def get_voters():
    try:
        result = supabase.table(TABLE_NAME).select("Name").execute()
        return [row['Name'] for row in result.data]
    except Exception:
        return []

voted_names = get_voters()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 4. LOGIN (THE INVISIBLE WAY) ---
if not st.session_state.authenticated:
    st.markdown("""
        <div style='display: flex; align-items: center; white-space: nowrap;'>
            <h1 style='margin: 0;'>Pendragon Awards</h1>
            <span style='font-size: 1.5rem; margin-left: 10px;'>🏀</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("Official 2026 Voting Portal")
    st.divider()
    
    st.write("Welcome to the Pendragon Ballot!")
    st.write("""
    * *Anonymous Voting:* Your individual selections are private.
    * *Eligibility:* Vote for members of any team.
    * *No Self-Voting:* The system hides your name from the ballot.
    * *One-Time Access:* Your name disappears from this list once you submit.
    """)
    
    st.divider()

    team = st.selectbox("WHICH TEAM ARE YOU IN?", options=[""] + list(roster.keys()))
    
    if team:
        # THE INVISIBLE LOGIC: Only show names NOT in voted_names
        available_names = [n for n in roster[team] if n not in voted_names]
        
        if not available_names:
            st.warning("All players on this team have already voted! 🎉")
        else:
            name = st.selectbox("SELECT YOUR NAME", options=[""] + available_names)

            if name:
                btn_col, _ = st.columns([1, 2])
                with btn_col:
                    if st.button("VERIFY & ENTER"):
                        st.session_state.user_name = name
                        st.session_state.user_team = team
                        st.session_state.authenticated = True
                        st.rerun()
# --- 5. TITLES & LABELS: LEFT ALIGNED & WHITE ---
    h1 {
        text-align: left !important;
        font-size: 2.2rem !important;
    }

    /* Change font-weight to 400 here to stop forcing everything to be bold */
    label, p, [data-testid="stWidgetLabel"] {
        color: white !important;
        font-weight: 400 !important; /* This was 700, making it bold */
        font-size: 1.1rem !important;
        text-align: left !important;
    }

# --- 6. THE SYNC & SUCCESS ---
else:
    # Header Row for Welcome Page
    t_col1, t_col2 = st.columns([1, 5])
    with t_col1:
        logo_path = os.path.join("images", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=60)
    with t_col2:
        st.markdown(f"### WELCOME, {st.session_state.user_name.upper()}!")

    st.write(f"***Here is some information about the voting process***")
    
    st.divider()

    # --- NO SELF-VOTING LOGIC ---
    all_players = [player for team_list in roster.values() for player in team_list]
    nominees = [p for p in all_players if p != st.session_state.user_name]
    
    st.write(f"**The 2026 Ballot is split into two halves:**")
    st.write("""
    * **Basketball Season Awards:** Official performance categories with pre-selected nominees.
    * **Fun Awards:** Community-focused categories where any Pendragon member is eligible.
    """)
    
    st.divider()
    
    st.write(f"***Basketball Season Awards***")
    st.write(f"""
    Our coaches have selected 3 top candidates for each of the 5 player categories and the Coach of the Year award
    """)
    st.write(f"*Your job is to crown the winner!*")
    
    st.divider()
    
    st.write(f"***Fun Season Awards***")
    st.write(f"These are open categories. You can nominate any Pendragon member you feel fits the title.")
    st.write(f"*(Note: You cannot nominate yourself!)*")
        
    st.divider()

    if st.button("LOG OUT"):
        st.session_state.clear()
        st.rerun()
