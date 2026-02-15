import streamlit as st
from supabase import create_client, Client
import os
import time

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

# --- UNIVERSAL AUTO-SCROLL SCRIPT ---
# This executes at the start of every rerun to snap the view to the top
st.components.v1.html(
    """
    <script>
        var mainContent = window.parent.document.querySelector('section.main');
        if (mainContent) {
            mainContent.scrollTo({top: 0, behavior: 'auto'});
        }
    </script>
    """,
    height=0,
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
    "Ladies 2": ["Agnese", "Emma", "Eva", "Ipek", "Jessica", "Jimena", "Marit", "Rita", "Stella", "Suzanne", "Weronika", "Ying"],
    "Men's 1": ["Chris", "Don", "Elia", "Elmer", "Harlod", "Melle", "Menno", "Noah"],
    "Men's 2": ["Akin", "Charlie", "Diego", "Jerko", "Kayvaughn", "Mattijs", "Miguel", "Vlad"],
    "Men's 3": ["Albert", "Dani", "Demir", "Eugen", "Francesco", "Gundars", "Hugo", "Jesper", "Quinn", "Rayan", "Terence", "Tuna"],
    "Men's 4": ["AK", "Alp", "Arda", "Atakan", "Eduard-George", "Kymaru", "Milos", "Olaf", "Paul", "Raphael", "Rron", "Stefan"],
    "Coach only": ["Niels", "Jerswin", "KJ"],
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
    
    # 1. Define the options correctly including the Admin Panel
    team_options = [""] + list(roster.keys()) + ["ADMIN PANEL"]
    
    st.write("Official 2026 Voting Portal")
    st.write("Welcome to the Pendragon Ballot!")
    st.divider()

    # 2. Use 'team_options' variable here so "ADMIN PANEL" actually appears
    team = st.selectbox("WHICH TEAM ARE YOU IN?", options=team_options)

    if team == "ADMIN PANEL":
        admin_pass = st.text_input("ENTER ADMIN PASSWORD", type="password")
        if st.button("LOGIN AS ADMIN"):
            if admin_pass == "Pendragon2026": 
                st.session_state.user_name = "ADMIN"
                st.session_state.user_team = "MANAGEMENT"
                st.session_state.is_admin = True # Enables the skip feature
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect Password")
                
    elif team:
        st.cache_data.clear()
        try:
            result = supabase.table(TABLE_NAME).select("name").execute()
            voted_names = [row['name'] for row in result.data]
        except:
            voted_names = []
        
        available_names = [n for n in roster[team] if n not in voted_names]
        if not available_names:
            st.warning("All players on this team have already voted! 🎉")
        else:
            name = st.selectbox("SELECT YOUR NAME", options=[""] + available_names)
            if name and st.button("VERIFY & ENTER"):
                st.session_state.user_name = name
                st.session_state.user_team = team
                st.session_state.is_admin = False # Explicitly not an admin
                st.session_state.authenticated = True
                st.rerun()
# --- POST-LOGIN VOTING FLOW ---
else:
    all_players = [player for team_list in roster.values() for player in team_list]
    universal_nominees = sorted([p for p in all_players if p != st.session_state.user_name])
    # STAGE 1: INSTRUCTIONS
    if st.session_state.voted_stage == "instructions":
        st.markdown(f"### WELCOME, {st.session_state.user_name.upper()}! 🏀")
        st.write("Click the categories below to see the voting rules.")
        
        # Dropdown 1
        with st.expander("THE VOTING PROCESS"):
            st.write("""
            * *Private Voting:* Your individual selections are private.
            * *Eligibility:* Vote for members of any team.
            * *No Self-Voting:* The system does not allow to vote for yourself.
            * *One-Time Access:* Your name disappears from this list once you submit.
                    """)

        # Dropdown 2
        with st.expander("BASKETBALL SEASON AWARDS"):
            st.write("Official categories with coach-selected nominees")
            st.write("A player can be nominated only for 1 Basketball Season Award")
            st.write(f"Players are not elgible for these awards if: ")
            st.write("""
            * Have been only part of Pendragon for a semester
            * Have missed 6 or more games because of injuries or other reasons
                    """)
            
        # Dropdown 3
        with st.expander("FUN SEASON AWARDS"):
            st.write("These are open categories. Any member can be voted!")
            st.write("""
            * A player can be nominated for multiple Fun Season Awards.
            * It does not matter if you have been part of Pendragon for only 1 semester or for a week. Anybody can be nominated for these awards!
                    """)
        st.divider()
        if st.button("START VOTING →"):
            st.session_state.voted_stage = "rookie_of_the_year"
            st.rerun()

    # STAGE 2: ROOKIE OF THE YEAR
    elif st.session_state.voted_stage == "rookie_of_the_year":
        st.markdown("## 👶 Rookie of the Year")
        st.write("*New players showing amazing improvement.*")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "rookie1.jpeg"))
        with col2: st.image(os.path.join("images", "rookie2.jpeg"))
        with col3: st.image(os.path.join("images", "rookie3.jpeg"))

        rookie_nominees = ["Jesper", "Stella", "AK"]
        filtered_rookie = [p for p in rookie_nominees if p != st.session_state.user_name]

        rookie_vote = st.selectbox("Your Pick:", options=[""] + filtered_rookie, key="rookie_sel")
        st.session_state.selections['rookie_of_the_year'] = rookie_vote

        st.write("") 
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "instructions"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('rookie_of_the_year') or st.session_state.get('is_admin'):
                    st.session_state.voted_stage = "most_improved_player"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")

    # STAGE 3: MOST IMPROVED PLAYER
    elif st.session_state.voted_stage == "most_improved_player":
        st.markdown("## 📈 Most Improved Player")
        st.write("*Players that have improved the most from last season.*")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "MIP1.jpeg"))
        with col2: st.image(os.path.join("images", "MIP2.jpeg"))
        with col3: st.image(os.path.join("images", "MIP3.jpeg"))

        mip_nominees = ["Rayan", "Lise", "Elmer"]
        filtered_mip = [p for p in mip_nominees if p != st.session_state.user_name]
        
        mip_vote = st.selectbox("Your Pick:", options=[""] + filtered_mip, key="mip_sel")
        st.session_state.selections['most_improved_player'] = mip_vote

        st.write("") 
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "rookie_of_the_year"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('most_improved_player') or st.session_state.get('is_admin'):
                    st.session_state.voted_stage = "defensive_player"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")
                    
    # STAGE 4: DEFENSIVE PLAYER OF THE YEAR
    elif st.session_state.voted_stage == "defensive_player":
        st.markdown("## 🛡️ Defensive Player of the Year")
        st.write("*The anchors of our defense.*")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "DPY1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "DPY2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "DPY3.jpeg"), use_container_width=True)
        
        dpoy_nominees = ["Atakan", "Ida", "Miguel"]
        filtered_dpoy = [p for p in dpoy_nominees if p != st.session_state.user_name]

        dpoy_vote = st.selectbox("Your Pick:", options=[""] + filtered_dpoy, key="dpoy_sel")
        st.session_state.selections['defensive_player'] = dpoy_vote

        st.write("") 
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "most_improved_player"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('defensive_player') or st.session_state.get('is_admin'):
                    st.session_state.voted_stage = "best_driver"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")
                    
    # STAGE 5: BEST DRIVER
    elif st.session_state.voted_stage == "best_driver":
        st.markdown("## 🏎️ BEST DRIVER")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "BD1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "BD2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "BD3.jpeg"), use_container_width=True)

        bd_nominees = ["Chris", "Iris", "Eugen"]
        filtered_bd = [p for p in bd_nominees if p != st.session_state.user_name]

        best_driver_vote = st.selectbox("Your Pick:", options=[""] + filtered_bd, key="bd_sel")
        st.session_state.selections['best_driver'] = best_driver_vote

        st.write("") 
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "defensive_player"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('best_driver') or st.session_state.get('is_admin'):
                    st.session_state.voted_stage = "best_shooter"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")

    # STAGE 6: BEST SHOOTER
    elif st.session_state.voted_stage == "best_shooter":
        st.markdown("## 🎯 Best Shooter")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "BS1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "BS2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "BS3.jpeg"), use_container_width=True)

        bs_nominees = ["Dani", "Ilinca", "Charlie"]
        filtered_bs = [p for p in bs_nominees if p != st.session_state.user_name]

        best_shooter_vote = st.selectbox("Your Pick:", options=[""] + filtered_bs, key="bs_sel")
        st.session_state.selections['best_shooter'] = best_shooter_vote

        st.write("") 
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "best_driver"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('best_shooter') or st.session_state.get('is_admin'):
                    st.session_state.voted_stage = "best_rebounder"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")

    # STAGE 7: BEST REBOUNDER
    elif st.session_state.voted_stage == "best_rebounder":
        st.markdown("## 🪟 Best Rebounder")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "BR1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "BR2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "BR3.jpeg"), use_container_width=True)

        br_nominees = ["Harlod", "Rachne", "Akin"]
        filtered_br = [p for p in br_nominees if p != st.session_state.user_name]

        best_rebounder_vote = st.selectbox("Your Pick:", options=[""] + filtered_br, key="br_sel")
        st.session_state.selections['best_rebounder'] = best_rebounder_vote

        st.write("") 
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "best_shooter"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('best_rebounder') or st.session_state.get('is_admin'):
                    st.session_state.voted_stage = "best_coach"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")

    # STAGE 8: BEST COACH
    elif st.session_state.voted_stage == "best_coach":
        st.markdown("## 📋 Best Coach")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.image(os.path.join("images", "BC1.jpeg"), use_container_width=True)
        with col2: st.image(os.path.join("images", "BC2.jpeg"), use_container_width=True)
        with col3: st.image(os.path.join("images", "BC3.jpeg"), use_container_width=True)

        bc_nominees = ["Niels", "Ilinca", "KJ"]
        filtered_bc = [p for p in bc_nominees if p != st.session_state.user_name]
         
        best_coach_vote = st.selectbox("Your Pick:", options=[""] + filtered_bc, key="bc_sel")
        st.session_state.selections['best_coach'] = best_coach_vote

        st.write("") 
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("← BACK"):
                st.session_state.voted_stage = "best_rebounder"
                st.rerun()
        with b_col2:
            if st.button("NEXT →"):
                if st.session_state.selections.get('best_coach') or st.session_state.get('is_admin'):
                    st.session_state.voted_stage = "fun_awards"
                    st.rerun()
                else:
                    st.warning("Please pick a winner!")
    
    # STAGE 9: FUN AWARDS
    elif st.session_state.voted_stage == "fun_awards":
        st.markdown("## ✨ Fun Season Awards")
        st.divider()

        # All selectboxes here use the filtered 'universal_nominees' list
        s_supporter = st.selectbox("📣 Best Supporter", options=[""] + universal_nominees, key="fun_supporter")
        s_party = st.selectbox("🍻 Party Animal", options=[""] + universal_nominees, key="fun_party")
        s_energy = st.selectbox("⚡ Best Energy", options=[""] + universal_nominees, key="fun_energy")
        s_karen = st.selectbox("👑 The 'Karen'", options=[""] + universal_nominees, key="fun_karen")
        s_late = st.selectbox("⏰ Always Late", options=[""] + universal_nominees, key="fun_late")
        s_forget = st.selectbox("🎒 The Forgetful One", options=[""] + universal_nominees, key="fun_forget")

        st.divider()
        f_col1, f_col2 = st.columns(2)
        
        with f_col1:
            if st.button("← BACK", key="f_back"):
                st.session_state.voted_stage = "best_coach"
                st.rerun()
                
        with f_col2:
            if st.button("SUBMIT 🏀", key="final_submit_btn"):
                fun_votes = [s_supporter, s_party, s_energy, s_karen, s_late, s_forget]
                
                if all(val != "" for val in fun_votes):
                    data = {
                        "name": st.session_state.user_name,
                        "team": st.session_state.user_team,
                        "rookie_vote": st.session_state.selections.get('rookie_of_the_year') or st.session_state.get('is_admin'),
                        "mip_vote": st.session_state.selections.get('most_improved_player') or st.session_state.get('is_admin'),
                        "dpoy_vote": st.session_state.selections.get('defensive_player') or st.session_state.get('is_admin'),
                        "best_driver": st.session_state.selections.get('best_driver') or st.session_state.get('is_admin'),
                        "best_shooter": st.session_state.selections.get('best_shooter') or st.session_state.get('is_admin'),
                        "best_rebounder": st.session_state.selections.get('best_rebounder') or st.session_state.get('is_admin'),
                        "best_coach": st.session_state.selections.get('best_coach') or st.session_state.get('is_admin'),
                        "best_supporter": s_supporter or st.session_state.get('is_admin'),
                        "party_animal": s_party or st.session_state.get('is_admin'),
                        "energy": s_energy or st.session_state.get('is_admin'),
                        "karen": s_karen or st.session_state.get('is_admin'),
                        "always_late": s_late or st.session_state.get('is_admin'),
                        "always_forgets": s_forget or st.session_state.get('is_admin')
                    }
                    
                    try:
                        supabase.table(TABLE_NAME).insert(data).execute()
                        # Move to the new event details page
                        st.session_state.voted_stage = "event_details"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Database Error: {e}")
                else:
                    st.warning("Please make a selection for all categories!")

    # --- NEW STAGE: AWARD NIGHT DETAILS ---
    elif st.session_state.voted_stage == "event_details":
        # The Trophy Celebration script triggers as soon as they land here
        st.components.v1.html(
            """
            <script>
            const confetti = window.parent.document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.top = '0'; confetti.style.left = '0';
            confetti.style.width = '100vw'; confetti.style.height = '100vh';
            confetti.style.pointerEvents = 'none'; confetti.style.zIndex = '9999';
            window.parent.document.body.appendChild(confetti);

            for(let i=0; i<50; i++) {
                const trophy = window.parent.document.createElement('div');
                trophy.innerHTML = '🏆';
                trophy.style.position = 'absolute';
                trophy.style.left = Math.random() * 100 + 'vw';
                trophy.style.top = '100vh';
                trophy.style.fontSize = (Math.random() * 20 + 20) + 'px';
                trophy.style.transition = 'transform ' + (Math.random() * 2 + 2) + 's linear, opacity 2s';
                confetti.appendChild(trophy);

                setTimeout(() => {
                    trophy.style.transform = 'translateY(-120vh) rotate(' + (Math.random() * 360) + 'deg)';
                    trophy.style.opacity = '0';
                }, 100);
            }
            </script>
            """,
            height=0,
        )

        st.markdown("<h2 style='text-align: center;'>VOTES SUBMITTED! 🏀</h2>", unsafe_allow_html=True)
        
        # Award Night Details Box
        st.markdown("""
            <div style="background-color: rgba(0,0,0,0.3); padding: 25px; border-radius: 15px; border: 1px solid #ffffff; text-align: center;">
                <h3 style="color: #FFD700; margin-top: 0;">🏆 Pendragon Awards Night</h3>
                <p style="font-size: 1.2rem;"><b>DATE:</b> TBD, TBD, 2026</p>
                <p style="font-size: 1.2rem;"><b>TIME:</b> TBD - Late</p>
                <p style="font-size: 1.2rem;"><b>LOCATION:</b> Sportcetner Cafe </p>
                <hr style="border-color: rgba(255,255,255,0.2);">
                <p><i>Bring your best energy!</i></p>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("LOGOUT"):
            st.session_state.authenticated = False
            st.session_state.voted_stage = "instructions"
            st.session_state.selections = {}
            st.rerun()
