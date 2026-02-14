import streamlit as st
from supabase import create_client, Client
import os


# --- DATABASE CONNECTION (SUPABASE) ---
SUPABASE_URL = "https://gkrkdujyuzcdoneuoakr.supabase.co"
SUPABASE_KEY = "sb_publishable_R20QEdVZMJuy8AiPBETy0g_R62okepN"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "Pendragon Awards"

# --- GLOBAL APP & PAGE SETTINGS ---
st.set_page_config(
    page_title="Pendragon Awards",
    page_icon="🏀",
    layout="centered"
)

# --- THE ULTIMATE NO-GAP HORIZONTAL CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #8B0000 0%, #D32F2F 100%);
        color: #ffffff;
    }

    /* Target the container of the 3 columns */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 0px !important;
    }

    /* Target the columns themselves and force them to stay 33% */
    [data-testid="column"], .stColumn {
        width: 33.33% !important;
        flex: 1 1 33.33% !important;
        min-width: 0px !important; /* This stops them from stacking */
        padding: 0px !important;
        margin: 0px !important;
    }

    /* Force the image to fill that 33% width perfectly */
    [data-testid="stImage"] img {
        height: 140px !important;
        width: 100% !important;
        object-fit: cover !important;
        border: none !important;
    }

    /* SOLID BLACK BUTTONS */
    div.stButton > button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 8px !important;
        width: auto !important;
        min-width: 110px;
    }

    /* Dropdown text size */
    div[data-baseweb="select"] div { font-size: 0.8rem !important; }

    /* Pinning buttons to edges */
    div.stButton > button {
        width: auto !important;
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

# --- SECTION 1: LOGIN ---hey
if not st.session_state.authenticated:
    st.markdown("<h1>Pendragon Awards 🏀</h1>", unsafe_allow_html=True)
    st.write("Official 2026 Voting Portal")
    st.write("Welcome to the Pendragon Ballot!")
    st.write("""
    * *Private Voting:* Your individual selections are private.
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

    # STAGE 1: INSTRUCTIONS
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
        st.write("Our coaches have selected 3 top candidates for each category.")
        st.write("### Fun Season Awards")
        st.write("These are open categories. You can nominate any member.")
        st.divider()

        if st.button("START VOTING →"):
            st.session_state.voted_stage = "rookie_of_the_year"
            st.rerun()

    # STAGE 2: ROOKIE OF THE YEAR
    elif st.session_state.voted_stage == "rookie_of_the_year":
        st.markdown("## Rookie of the Year")
        st.write("*New players showing amazing improvement.*")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "rookie1.jpeg"))
        with col2: st.image(os.path.join("images", "rookie2.jpeg"))
        with col3: st.image(os.path.join("images", "rookie3.jpeg"))

        st.divider()
        
        rookie_vote = st.selectbox("Your Pick:", options=["", "Jesper", "Stella", "AK"], key="rookie_sel")
        st.session_state.selections['rookie_of_the_year'] = rookie_vote

        # Back & Next Buttons on the same line
        st.write("") # Spacer
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "instructions"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('rookie_of_the_year'):
                    st.session_state.voted_stage = "most_improved_player"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")

    # STAGE 3: MOST IMPROVED PLAYER
    elif st.session_state.voted_stage == "most_improved_player":
        st.markdown("## Most Improved Player")
        st.write("*Players that have improved the most from last season.*")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "MIP1.jpeg"))
        with col2: st.image(os.path.join("images", "MIP2.jpeg"))
        with col3: st.image(os.path.join("images", "MIP3.jpeg"))

        st.divider()
        
        mip_vote = st.selectbox("Your Pick:", options=["", "Rayan", "Lise", "Elmer"], key="mip_sel")
        st.session_state.selections['most_improved_player'] = mip_vote

         # Back & Next Buttons on the same line
        st.write("") # Spacer
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "rookie_of_the_year"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('most_improved_player'):
                    st.session_state.voted_stage = "defensive_player"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")
                    
    # STAGE 4: DEFENSIVE PLAYER OF THE YEAR
    elif st.session_state.voted_stage == "defensive_player":
        st.markdown("## Defensive Player of the Year")
        st.write("*The anchors of our defense. Hustle, intensity and proud of being a good defender*")
        
        # Image Strip (Matches Rookie/MIP style)
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "DPY1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "DPY2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "DPY3.jpeg"), use_container_width=True)

        st.divider()
        
        # Dropdown
        dpoy_vote = st.selectbox(
            "Your Pick:", 
            options=["", "Atakan", "Ida", "Miguel"], 
            key="dpoy_sel"
        )
        st.session_state.selections['defensive_player'] = dpoy_vote

        # --- Navigation Buttons ---
        st.write("") 
        b_col, n_col = st.columns(2)
        
         # Back & Next Buttons on the same line
        st.write("") # Spacer
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "most_improved_player"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('defensive_player'):
                    st.session_state.voted_stage = "best_shooter"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")
                    
      # STAGE 5: BEST DRIVER
    elif st.session_state.voted_stage == "best_driver":
        st.markdown("## BEST DRIVER")
        st.write("*Best drivers and finishers under the basket. These players have shown amazing finishes abilities this season*")
        
        # Image Strip (Matches Rookie/MIP style)
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "BD1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "BD2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "BD3.jpeg"), use_container_width=True)

        st.divider()
        
        # Dropdown
        best_driver_vote = st.selectbox(
            "Your Pick:", 
            options=["", "Chris", "Iris", "Eugen"], 
            key="bd_sel"
        )
        st.session_state.selections['best_driver'] = best_driver_vote

        # --- Navigation Buttons ---
        st.write("") 
        b_col, n_col = st.columns(2)
        
         # Back & Next Buttons on the same line
        st.write("") # Spacer
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "defensive_player"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('best_driver'):
                    st.session_state.voted_stage = "best_shooter"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")
    

     # STAGE 6: BEST SHOOTER
    elif st.session_state.voted_stage == "best_shooter":
        st.markdown("## Best Shooter")
        st.write("*Best all around shooters. These players have made any kind of shot throughout the season whether from the pass, dribble, midrange or 3 pointer*")
        
        # Image Strip (Matches Rookie/MIP style)
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "BS1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "BS2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "BS3.jpeg"), use_container_width=True)

        st.divider()
        
        # Dropdown
        best_shooter_vote = st.selectbox(
            "Your Pick:", 
            options=["", "Dani", "Ilinca", "Charlie"], 
            key="bs_sel"
        )
        st.session_state.selections['best_shooter'] = best_shooter_vote

        # --- Navigation Buttons ---
        st.write("") 
        b_col, n_col = st.columns(2)
        
         # Back & Next Buttons on the same line
        st.write("") # Spacer
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "best_driver"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('best_shooter'):
                    st.session_state.voted_stage = "best_coach"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")

    # STAGE 7: BEST COACH
    elif st.session_state.voted_stage == "best_coach":
        st.markdown("## Best Coach")
        st.write("*Recognizing the leader behind the bench who has best inspired their team and guided their growth this season.*")
        
        # Image Strip (Matches Rookie/MIP style)
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "BC1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "BC2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "BC3.jpeg"), use_container_width=True)

        st.divider()
        
        # Dropdown
        best_coach_vote = st.selectbox(
            "Your Pick:", 
            options=["", "Niels", "Ilinca", "KJ"], 
            key="bc_sel"
        )
        st.session_state.selections['best_coach'] = best_coach_vote

        # --- Navigation Buttons ---
        st.write("") 
        b_col, n_col = st.columns(2)
        
         # Back & Next Buttons on the same line
        st.write("") # Spacer
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "defensive_driver"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('best_shooter'):
                    st.session_state.voted_stage = "fun_awards"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")
    
    # STAGE 8: FUN AWARDS
    elif st.session_state.voted_stage == "fun_awards":
        st.markdown("## ✨ Fun Season Awards")
        st.write("*Anybody is eligible for these awards, it does not matter if you were injured or only at Pendragon for 1 semester.*")
        st.divider()

        # 1. Best Supporter
        st.markdown("### 📣 Best Supporter")
        s_supporter = st.selectbox("Who is the heartbeat of the stands?", options=[""] + nominees, key="fun_supporter")
        st.write("*Cheering even when their own team isn't playing.*")

        # 2. Party Animal
        st.markdown("### 🍻 Party Animal")
        s_party = st.selectbox("Who dominates the post game?", options=[""] + nominees, key="fun_party")
        st.write("*First one at the bar, last one to leave the after-party.*")

        # 3. Drama
        st.markdown("### 🎭 Most Dramatic")
        s_drama = st.selectbox("Who brings Hollywood to the hardwood?", options=[""] + nominees, key="fun_drama")
        st.write("*Every foul is a tragedy, every missed layup is a heartbreak.*")

        # 4. Karen
        st.markdown("### 👑 The 'Karen'")
        s_karen = st.selectbox("Who always wants to speak to the referee's manager?", options=[""] + nominees, key="fun_karen")
        st.write("*Ready to challenge every whistle and discuss the rules.*")

        # 5. Always Late
        st.markdown("### ⏰ Always Late")
        s_late = st.selectbox("Who operates on their own time zone?", options=[""] + nominees, key="fun_late")
        st.write("*Who has never seen a 7:30 PM practice start at 7:30 PM?*")

        # 6. Forgetful One
        st.markdown("### 🎒 The Forgetful One")
        s_forget = st.selectbox("Who leaves a trail of gear across every gym?", options=[""] + nominees, key="fun_forget")
        st.write("*Always forgetting water bottles, shoes, or their head if it wasn't attached.*")

        st.divider()
        
       # STAGE 8: FUN AWARDS
    elif st.session_state.voted_stage == "fun_awards":
        st.markdown("## ✨ Fun Season Awards")
        st.divider()

        # 1-6: Award Selectboxes
        s_supporter = st.selectbox("📣 Best Supporter", options=[""] + nominees, key="fun_supporter")
        s_party = st.selectbox("🍻 Party Animal", options=[""] + nominees, key="fun_party")
        s_drama = st.selectbox("🎭 Most Dramatic", options=[""] + nominees, key="fun_drama")
        s_karen = st.selectbox("👑 The 'Karen'", options=[""] + nominees, key="fun_karen")
        s_late = st.selectbox("⏰ Always Late", options=[""] + nominees, key="fun_late")
        s_forget = st.selectbox("🎒 The Forgetful One", options=[""] + nominees, key="fun_forget")

        st.divider()
        
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            if st.button("← BACK", key="f_back"):
                st.session_state.voted_stage = "best_coach"
                st.rerun()
                
        with f_col2:
            if st.button("SUBMIT 🏀", key="final_submit_btn"):
                
                # Check if all fields are filled
                fun_votes = [s_supporter, s_party, s_drama, s_karen, s_late, s_forget]
                
                if all(val != "" for val in fun_votes):
                    # LOWERCASE KEYS match standard Supabase behavior
                   data = {
                            "name": st.session_state.user_name,
                            "team": st.session_state.user_team,
                            "rookie_vote": st.session_state.selections.get('rookie_of_the_year'),
                            "mip_vote": st.session_state.selections.get('most_improved_player'),
                            "dpoy_vote": st.session_state.selections.get('defensive_player'),
                            "best_driver": st.session_state.selections.get('best_driver'),
                            "best_shooter": st.session_state.selections.get('best_shooter'),
                            "best_coach": st.session_state.selections.get('best_coach'),
                            "best_supporter": s_supporter,
                            "party_animal": s_party,
                            "drama": s_drama,
                            "karen": s_karen,
                            "always_late": s_late,
                            "always_forgets": s_forget 
                        }
                    
                    try:
                        supabase.table(TABLE_NAME).insert(data).execute()
                        st.success("Votes Submitted! 🏀")
                        st.balloons()
                        st.session_state.authenticated = False
                    except Exception as e:
                        # This will tell us EXACTLY which column is missing
                        st.error(f"Submit Error: {e}")
                else:
                    st.warning("Please make a selection for all categories!")
            st.markdown('</div>', unsafe_allow_html=True)
