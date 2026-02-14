import streamlit as st
from supabase import create_client, Client
import os

# --- DATABASE CONNECTION (SUPABASE) ---
SUPABASE_URL = "https://gkrkdujyuzcdoneuoakr.supabase.co"
SUPABASE_KEY = "sb_publishable_R20QEdVZMJuy8AiPBETy0g_R62okepN"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "Pendragon Awards 2026"

# --- GLOBAL APP & PAGE SETTINGS ---
st.set_page_config(
    page_title="Pendragon Awards",
    page_icon="🏀",
    layout="centered"
)

# --- CONSOLIDATED MOBILE-FIRST CSS ---
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(180deg, #8B0000 0%, #D32F2F 100%);
        color: #ffffff;
    }

    /* UNIVERSAL IMAGE FORMATTER - MOBILE OPTIMIZED */
    [data-testid="stImage"] img {
        height: 350px !important; 
        width: 100% !important;      
        object-fit: cover !important; 
        object-position: center 20%; 
        border-radius: 15px;
        border: 2px solid rgba(255,255,255,0.3);
    }

    /* Pushes content up to avoid scrolling on small phones */
    .stSelectbox {
        margin-bottom: 40px !important; 
    }

    /* Selectbox Styling */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] * {
        color: #000000 !important;
    }

    /* BUTTONS: Same line, Small, and Pushed to edges */
    div.stButton > button {
        background-color: #000000 !important; 
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 10px;
        text-transform: uppercase;
        font-weight: 700;
        font-size: 0.85rem !important; 
        min-width: 130px !important; 
        padding: 8px 10px !important;
    }

    /* THE MOBILE LAYOUT FIX: Forces side-by-side columns */
    [data-testid="column"] {
        width: 48% !important;
        flex: 1 1 48% !important;
        min-width: 40% !important;
    }

    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
    }

    /* Individual Button Alignment */
    [data-testid="column"]:nth-of-type(1) div.stButton {
        display: flex;
        justify-content: flex-start;
    }
    [data-testid="column"]:nth-of-type(2) div.stButton {
        display: flex;
        justify-content: flex-end;
    }

    /* Header & Text Styling */
    h1 { text-align: left !important; font-size: 1.8rem !important; }
    label, p, [data-testid="stWidgetLabel"] {
        color: white !important;
        font-weight: 400 !important; 
        font-size: 1rem !important;
    }
    hr { border-top: 1px solid rgba(255, 255, 255, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- PLAYER ROSTER ---
roster = {
    "Ladies 1": ["Ida", "Ilinca", "Imke", "Iris", "Janne", "Lise", "Margherita", "Rachne", "Susanna", "Zey", "Zeynep", "Zoë"],
    "Men's 3": ["Albert", "Dani", "Demir", "Eugen", "Francesco", "Gundars", "Hugo", "Jesper", "Quinn", "Rayan", "Terence", "Tuna"],
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
if 'voted_stage' not in st.session_state:
    st.session_state.voted_stage = "instructions"
if 'selections' not in st.session_state:
    st.session_state.selections = {}

# --- SECTION 1: LOGIN ---
if not st.session_state.authenticated:
    st.markdown("<h1>Pendragon Awards 🏀</h1>", unsafe_allow_html=True)
    st.write("Official 2026 Voting Portal")
    st.divider()
    team = st.selectbox("WHICH TEAM ARE YOU IN?", options=[""] + list(roster.keys()))
    if team:
        available_names = [n for n in roster[team] if n not in voted_names]
        if not available_names:
            st.warning("All players on this team have already voted! 🎉")
        else:
            name = st.selectbox("SELECT YOUR NAME", options=[""] + available_names)
            if name and st.button("VERIFY & ENTER"):
                st.session_state.user_name = name
                st.session_state.user_team = team
                st.session_state.authenticated = True
                st.rerun()

# --- POST-LOGIN VOTING FLOW ---
else:
    all_players = [player for team_list in roster.values() for player in team_list]
    nominees = [p for p in all_players if p != st.session_state.user_name]

    # STAGE: INSTRUCTIONS
    if st.session_state.voted_stage == "instructions":
        st.markdown(f"### WELCOME, {st.session_state.user_name.upper()}!")
        st.write("***Information about the voting process***")
        st.divider()
        st.write("**The 2026 Ballot is split into two halves:**")
        st.write("""
        * **Basketball Season Awards:** Official categories.
        * **Fun Awards:** Community-focused categories.
        """)
        st.divider()
        if st.button("START VOTING →"):
            st.session_state.voted_stage = "rookie_awards"
            st.rerun()

    # STAGE: AWARD 1 - ROOKIE OF THE YEAR
    elif st.session_state.voted_stage == "rookie_awards":
        st.markdown("## 1. Rookie of the Year")
        st.write("*Players that are new and showing amazing improvement.*")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(os.path.join("images", "rookie1.jpeg"))
            st.markdown("<p style='text-align: center;'>Jesper</p>", unsafe_allow_html=True)
        with col2:
            st.image(os.path.join("images", "rookie2.jpeg"))
            st.markdown("<p style='text-align: center;'>Stella</p>", unsafe_allow_html=True)
        with col3:
            st.image(os.path.join("images", "rookie3.jpeg"))
            st.markdown("<p style='text-align: center;'>Matei</p>", unsafe_allow_html=True)

        st.divider()
        rookie_vote = st.selectbox("Your Pick:", options=["", "Jesper", "Stella", "Matei"])
        st.session_state.selections['rookie_of_the_year'] = rookie_vote

        # Navigation Buttons
        c1, c2 = st.columns(2) 
        with c1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "instructions"
                st.rerun()
        with c2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('rookie_of_the_year'):
                    st.session_state.voted_stage = "fun_awards"
                    st.rerun()
                else:
                    st.warning("Please select a winner!")

    # STAGE: FUN AWARDS & SUBMISSION
    elif st.session_state.voted_stage == "fun_awards":
        st.markdown("## ✨ Fun Season Awards")
        best_dressed = st.selectbox("Best Dressed", options=[""] + nominees)
        st.session_state.selections['best_dressed'] = best_dressed

        if st.button("🏀 SUBMIT FINAL BALLOT"):
            try:
                submission = {
                    "Name": st.session_state.user_name,
                    "Team": st.session_state.user_team,
                    "Selection": str(st.session_state.selections)
                }
                supabase.table(TABLE_NAME).insert(submission).execute()
                st.success("Ballot Submitted!")
                st.balloons()
                st.session_state.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
