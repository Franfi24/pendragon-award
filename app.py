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

# --- MOBILE-FIRST CSS ---
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(180deg, #8B0000 0%, #D32F2F 100%);
        color: #ffffff;
    }

    /* THE HORIZONTAL STRIP: No Gaps, No Vertical Stacking */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important; /* Prevents stacking on phone */
        gap: 0px !important;           /* Removes gaps between images */
        width: 100% !important;
    }

    [data-testid="column"] {
        flex: 1 !important;
        width: 33.33% !important;      /* Forces exact thirds */
        min-width: 0px !important;
        padding: 0px !important;       /* Removes internal column spacing */
    }

    [data-testid="stImage"] img {
        height: 140px !important;      /* Uniform height */
        width: 100% !important;
        object-fit: cover !important;  /* Crops landscape to match portrait */
        object-position: center 20%;
        border: 0.5px solid rgba(255,255,255,0.2);
        box-sizing: border-box !important;
    }

    /* SELECTBOX: Smaller text and slimmer profile */
    div[data-baseweb="select"] div {
        font-size: 0.8rem !important;
        color: #000000 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        min-height: 35px !important;
    }

    /* NAVIGATION BUTTONS: Far Left / Far Right Styling */
    div.stButton > button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 8px;
        font-size: 0.75rem !important;
        min-width: 90px;
    }
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
    st.write("Welcome to the Pendragon Ballot!")
    st.write("""
    * *Anonymous Voting:* Your individual selections are private.
    * *Eligibility:* Vote for members of any team.
    * *No Self-Voting:* The system does not allow to vote for yourself.
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
        * **Basketball Season Awards:** Official categories with coach-selected nominees.
        * **Fun Awards:** Community-focused categories where anyone is eligible.
        """)
        
        st.divider()
        st.write("### Basketball Season Awards")
        st.write("Our coaches have selected 3 top candidates for each category. *Your job is to crown the winner!*")
        st.write("### Fun Season Awards")
        st.write("These are open categories. You can nominate any member. *(Note: You cannot nominate yourself!)*")
        st.divider()

        if st.button("START VOTING →"):
            st.session_state.voted_stage = "rookie_awards"
            st.rerun()

    # --- ROOKIE OF THE YEAR STAGE ---
# --- SECTION 2: ROOKIE OF THE YEAR STAGE ---
    if st.session_state.voted_stage == "rookie_awards":
        st.markdown("## 1. Rookie of the Year")
        st.write("*Players that are new to Pendragon and have shown amazing improvement.*")
        
    # Nominee Row (Forced Horizontal by Section 1)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(os.path.join("images", "rookie1.jpeg"))
        st.markdown("<p style='text-align:center; font-size:10px; margin-top:-5px;'>Jesper</p>", unsafe_allow_html=True)
    with col2:
        st.image(os.path.join("images", "rookie2.jpeg"))
        st.markdown("<p style='text-align:center; font-size:10px; margin-top:-5px;'>Stella</p>", unsafe_allow_html=True)
    with col3:
        st.image(os.path.join("images", "rookie3.jpeg"))
        st.markdown("<p style='text-align:center; font-size:10px; margin-top:-5px;'>Matei</p>", unsafe_allow_html=True)

    st.divider()
    
    # Voting Dropdown
    rookie_vote = st.selectbox("Your Pick:", options=["", "Jesper", "Stella", "Matei"], key="rookie_select")
    st.session_state.selections['rookie_of_the_year'] = rookie_vote

    # Navigation: Far Left and Far Right
    nav_left, nav_right = st.columns(2)
    with nav_left:
        # Pinned far left
        if st.button("← BACK"):
            st.session_state.voted_stage = "instructions"
            st.rerun()
            
    with nav_right:
        # Wrapper to push the 'Next' button to the far right
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.button("NEXT →"):
            if st.session_state.selections.get('rookie_of_the_year'):
                st.session_state.voted_stage = "fun_awards" # Update to your next stage
                st.rerun()
            else:
                st.warning("Please select a winner!")
        st.markdown("</div>", unsafe_allow_html=True)
    # Voting Dropdown
    rookie_vote = st.selectbox("Your Pick:", options=["", "Jesper", "Stella", "Matei"], key="rookie_select")
    st.session_state.selections['rookie_of_the_year'] = rookie_vote

    # Navigation: Far Left and Far Right
    nav_left, nav_right = st.columns(2)
    with nav_left:
        # Pinned far left
        if st.button("← BACK"):
            st.session_state.voted_stage = "instructions"
            st.rerun()
            
    with nav_right:
        # Wrapper to push the 'Next' button to the far right
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.button("NEXT →"):
            if st.session_state.selections.get('rookie_of_the_year'):
                st.session_state.voted_stage = "fun_awards" # Update to your next stage
                st.rerun()
            else:
                st.warning("Please select a winner!")
        st.markdown("</div>", unsafe_allow_html=True)

    
    # STAGE: FUN AWARDS & SUBMISSION
    elif st.session_state.voted_stage == "fun_awards":
        st.markdown("## ✨ Fun Season Awards")
        st.write("*Choose anyone from the club for these community titles.*")
        
        best_dressed = st.selectbox("Best Dressed", options=[""] + nominees)
        st.session_state.selections['best_dressed'] = best_dressed

        st.divider()
        
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
