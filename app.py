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

# --- MOBILE-FIRST HORIZONTAL LAYOUT ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #8B0000 0%, #D32F2F 100%);
        color: #ffffff;
    }

    /* THE PICTURE FIX: Small, Horizontal, and Identical */
    [data-testid="stImage"] img {
        height: 120px !important;    /* Small enough for phone width */
        width: 100px !important;     /* Uniform width */
        object-fit: cover !important; /* Crops landscape photos to fit */
        object-position: center 20%; 
        border-radius: 12px;
        border: 2px solid rgba(255,255,255,0.4);
    }

    /* Force columns to stay side-by-side on mobile */
    [data-testid="column"] {
        width: 30% !important;
        flex: 1 1 30% !important;
        min-width: 30% !important;
        text-align: center;
    }

    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        gap: 5px !important;
    }

    /* Button Spacing for Mobile */
    .stSelectbox { margin-bottom: 30px !important; }
    
    div.stButton > button {
        background-color: #000000 !important; 
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 8px;
        font-size: 0.8rem !important;
        min-width: 100px !important;
        padding: 5px !important;
    }

    /* Navigation button alignment */
    [data-testid="column"]:nth-of-type(1) div.stButton { justify-content: flex-start; }
    [data-testid="column"]:nth-of-type(2) div.stButton { justify-content: flex-end; }
    
    p { font-size: 0.8rem !important; margin-top: -10px; }
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

    # AWARD 1 - ROOKIE OF THE YEAR
    st.markdown("## 1. Rookie of the Year")
    
    # Force 3 small columns for the mobile row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(os.path.join("images", "rookie1.jpeg"))
        st.markdown("Jesper")
    with col2:
        st.image(os.path.join("images", "rookie2.jpeg"))
        st.markdown("Stella")
    with col3:
        st.image(os.path.join("images", "rookie3.jpeg"))
        st.markdown("Matei")

    st.divider()
    
    rookie_vote = st.selectbox("Your Pick:", options=["", "Jesper", "Stella", "Matei"], key="rookie_select")
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
