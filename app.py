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

# --- VISUAL THEME & CSS STYLING (ORIGINAL RED) ---
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
        font-weight: 400 !important; 
        font-size: 1.1rem !important;
        text-align: left !important;
    }

    div.stButton > button {
        background-color: #000000 !important; 
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 12px;
        text-transform: uppercase;
        font-weight: 700;
        width: auto !important;
    }
    hr { border-top: 1px solid rgba(255, 255, 255, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- PLAYER ROSTER & CLUB DATA ---
roster = {
    "Ladies 1": ["Ida", "Ilinca", "Imke", "Iris", "Janne", "Lise", "Margherita", "Rachne", "Susanna", "Zey", "Zeynep", "Zoë"],
    "Men's 3": ["Albert", "Dani", "Demir", "Eugen", "Francesco", "Gundars", "Hugo", "Jesper", "Quinn", "Rayan", "Terence", "Tuna"],
}

# --- DATABASE HELPER: FETCH SUBMITTED BALLOTS ---
def get_voters():
    try:
        result = supabase.table(TABLE_NAME).select("Name").execute()
        return [row['Name'] for row in result.data]
    except Exception:
        return []

voted_names = get_voters()

# --- SESSION STATE INITIALIZATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'voted_stage' not in st.session_state:
    st.session_state.voted_stage = "instructions"
if 'selections' not in st.session_state:
    st.session_state.selections = {}

# --- SECTION 1: LOGIN & AUTHENTICATION ---
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

# --- POST-LOGIN VOTING FLOW ---
else:
    all_players = [player for team_list in roster.values() for player in team_list]
    nominees = [p for p in all_players if p != st.session_state.user_name]

    # --- SECTION 2: VOTING INSTRUCTIONS ---
    if st.session_state.voted_stage == "instructions":
        t_col1, t_col2 = st.columns([1, 5])
        with t_col1:
            logo_path = os.path.join("images", "logo.png")
            if os.path.exists(logo_path):
                st.image(logo_path, width=60)
        with t_col2:
            st.markdown(f"### WELCOME, {st.session_state.user_name.upper()}!")

        st.write("***Information about the voting process***")
        st.divider()
        st.write("**The 2026 Ballot is split into two halves:**")
        st.write("""
        * Basketball Season Awards: Official categories with coach-selected nominees.
        * Fun Awards: Community categories where any member is eligible.
        """)
        st.divider()
        
        if st.button("START VOTING →"):
            st.session_state.voted_stage = "basketball_awards"
            st.rerun()

    # --- SECTION 3: BASKETBALL AWARDS & ELIGIBILITY RULES ---
    elif st.session_state.voted_stage == "basketball_awards":
        st.markdown("## 🏀 Basketball Season Awards")
        
        st.write("***Basketball Award Eligibility:***")
        st.write("Every member is encouraged to vote! However, per coaching staff regulations, players were not eligible for nomination if:")
        st.write("""
        * They have been a member for only one semester.
        * They missed 6 or more games due to injury or other reasons.
        """)
        st.divider()

        st.write("### Cast Your Votes")

        # --- AWARD: ROOKIE OF THE YEAR ---
        st.write("**1. Rookie of the Year**")
        st.write("*Players who are new to Pendragon and have shown amazing improvement, commitment, and growth this season.*")
        
        # Replace these placeholders with your actual 3 nominees
        rookie_nominees = ["", "Nominee A", "Nominee B", "Nominee C"]
        rookie_vote = st.selectbox("Select your Rookie of the Year:", options=rookie_nominees, key="rookie_select")
        st.session_state.selections['rookie_of_the_year'] = rookie_vote

        st.divider()
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← BACK TO INFO"):
                st.session_state.voted_stage = "instructions"
                st.rerun()
        with col2:
            if st.button("NEXT: FUN AWARDS →"):
                if st.session_state.selections.get('rookie_of_the_year'):
                    st.session_state.voted_stage = "fun_awards"
                    st.rerun()
                else:
                    st.warning("Please make a selection for Rookie of the Year!")

    # --- SECTION 4: FUN AWARDS & SUBMISSION ---
    elif st.session_state.voted_stage == "fun_awards":
        st.markdown("## ✨ Fun Season Awards")
        st.write("These awards are open to any member of Pendragon except yourself.")
        st.divider()
        
        # Example Fun Award
        best_dressed = st.selectbox("Best Dressed", options=[""] + nominees)
        st.session_state.selections['best_dressed'] = best_dressed

        st.divider()
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "basketball_awards"
                st.rerun()
        with col2:
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
