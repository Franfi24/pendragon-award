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


def trigger_basketball_gif(gif_type):
    # This dictionary must be indented 4 spaces to be "inside" the function
    gifs = {
        # 1. THE ERROR (Technical Foul)
        "error": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l41lXkx9x8OTM1rwY/giphy.gif",
        
        # 2. ROOKIE OF THE YEAR (Gym Training)
        "rookie": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnV6Z3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0HlPtb37mC0n5LJS/giphy.gif",
        
        # 3. MOST IMPROVED (Gym Training / Practice)
        "improved": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnV6Z3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxf837vXis8/giphy.gif",
        
        # 4. BEST SHOOTER (Swish)
        "shooter": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnV6Z3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3oAt20560Snc7KzHj2/giphy.gif",
        
        # 5. BEST DEFENDER (Defense/Block)
        "defender": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnV6Z3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0HlTfbH522K9I1W0/giphy.gif",
        
        # 6. BEST COACH (Leadership/Clapping)
        "coach": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnV6Z3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l2SpXzEYXUIg83EAg/giphy.gif",
        
        # 7. EVERYTHING ELSE (The Slam Dunk)
        "dunk": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxZ3RreHpxJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKP9Xh7h1P9iXis/giphy.gif"
    }

    # The rest of the function must also stay indented!
    selected_gif = gifs.get(gif_type, gifs["dunk"])
    unique_id = f"gif_{int(time.time() * 1000)}"
    
    st.components.v1.html(
        f"""
        <script>
        const gifContainer = window.parent.document.createElement('div');
        gifContainer.id = '{unique_id}';
        gifContainer.style.position = 'fixed';
        gifContainer.style.top = '50%';
        gifContainer.style.left = '50%';
        gifContainer.style.transform = 'translate(-50%, -50%)';
        gifContainer.style.zIndex = '10000';
        gifContainer.style.pointerEvents = 'none';
        
        gifContainer.innerHTML = `<img src="{selected_gif}" style="width: 320px; border-radius: 12px; box-shadow: 0 15px 50px rgba(0,0,0,0.9);">`;
        
        window.parent.document.body.appendChild(gifContainer);

        setTimeout(() => {{
            gifContainer.style.opacity = '0';
            gifContainer.style.transition = 'opacity 0.4s ease';
            setTimeout(() => {{ gifContainer.remove(); }}, 400);
        }}, 2200); 
        </script>
        """,
        height=0
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
    "COACH ONLY": ["Niels", "Jerswin", "KJ"],
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
    team_options = [""] + list(roster.keys()) + ["ADMIN"]
    
    st.write("Official 2026 Voting Portal")
    st.write("Welcome to the Pendragon Ballot!")
    st.divider()

    # 2. Use 'team_options' variable here so "ADMIN PANEL" actually appears
    team = st.selectbox("WHICH TEAM ARE YOU IN?", options=team_options)

    if team == "ADMIN":
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
        st.write("Have a look at the voting rules before proceeding.")
        
        # Dropdown 1
        with st.expander("GENERAL INFORMATION"):
            st.markdown("""
            * **Private Voting:** All individual selections are strictly confidential.
            * **Eligibility:** You may vote for members from any team.
            * **Self-Voting Guard:** The system automatically prevents self-voting.
            * **Single Entry:** Once you submit your ballot, your name is removed from the login list.
            """)

        # Dropdown 2
        with st.expander("BASKETBALL SEASON AWARDS"):
            st.write("**Official categories featuring coach-selected nominees.**")
            st.write("Note: A player can only be nominated in one Basketball Season Award.")
            st.write("Players are **not eligible** for these specific awards if they:")
            st.markdown("""
            * Have only been a member of Pendragon for a single semester.
            * Have missed more  than 6 games due to injury or other absences.
            """)
            
        # Dropdown 3
        with st.expander("FUN SEASON AWARDS"):
            st.write("**Open categories where every member is a potential nominee!**")
            st.markdown("""
            * **Unlimited Nominations:** Players can be nominated for multiple Fun Season Awards.
            * **No Restrictions:** Time with the club doesn't matter. Whether you joined last year or last week, everyone is eligible!
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
            if st.button("NEXT →", key="btn_rookie"):
    if st.session_state.selections.get('rookie_of_the_year'):
        trigger_basketball_gif("rookie")  # Gym training GIF
        time.sleep(1.5) 
        st.session_state.voted_stage = "most_improved_player"
        st.rerun()
    else:
        trigger_blue_warning()
        trigger_basketball_gif("error")   # Technical Foul GIF

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
            if st.button("NEXT →", key="btn_improved"):
    if st.session_state.selections.get('most_improved'):
        trigger_basketball_gif("improved") # Practice GIF
        time.sleep(1.5)
        st.session_state.voted_stage = "best_shooter"
        st.rerun()
    else:
        trigger_blue_warning()
        trigger_basketball_gif("error")
                    
    # STAGE 4: DEFENSIVE PLAYER OF THE YEAR
    elif st.session_state.voted_stage == "defensive_player":
        st.markdown("## 🛡️ Defensive Player of the Year")
        st.write("*The anchors of our defense. Hustle, intensity and proud of being a good defender*")
        
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
            if st.button("NEXT →", key="btn_defender"):
    if st.session_state.selections.get('best_defender'):
        trigger_basketball_gif("defender") # Block/Defense GIF
        time.sleep(1.5)
        st.session_state.voted_stage = "fun_awards" # Transition to the rest
        st.rerun()
    else:
        trigger_blue_warning()
        trigger_basketball_gif("error")
                    
    # STAGE 5: BEST DRIVER
    elif st.session_state.voted_stage == "best_driver":
        st.markdown("## 🏎️ BEST DRIVER")
        st.write("*Best drivers and finishers under the basket. These players have shown amazing finishes abilities this season*")
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
            if st.button("NEXT →", key="btn_generic"):
    if st.session_state.selections.get('current_category_key'):
        trigger_basketball_gif("dunk") # Slam Dunk GIF
        time.sleep(1.5)
        st.session_state.voted_stage = "next_category_name"
        st.rerun()
    else:
        trigger_blue_warning()
        trigger_basketball_gif("error")

    # STAGE 6: BEST SHOOTER
    elif st.session_state.voted_stage == "best_shooter":
        st.markdown("## 🎯 Best Shooter")
        st.write("*Best all around shooters. These players have made any kind of shot throughout the season whether from the pass, dribble, midrange or 3 pointer*")
        
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
          if st.button("NEXT →", key="btn_shooter"):
    if st.session_state.selections.get('best_shooter'):
        trigger_basketball_gif("shooter")  # Swish GIF
        time.sleep(1.5)
        st.session_state.voted_stage = "best_defender"
        st.rerun()
    else:
        trigger_blue_warning()
        trigger_basketball_gif("error")

    # STAGE 7: BEST REBOUNDER
    elif st.session_state.voted_stage == "best_rebounder":
        st.markdown("## 🪟 Best Rebounder")
        st.write("*The glass cleaners. Box out with grit, and ensure the team gets every second-chance opportunity.*")
        
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
            if st.button("NEXT →", key="btn_generic"):
    if st.session_state.selections.get('current_category_key'):
        trigger_basketball_gif("dunk") # Slam Dunk GIF
        time.sleep(1.5)
        st.session_state.voted_stage = "next_category_name"
        st.rerun()
    else:
        trigger_blue_warning()
        trigger_basketball_gif("error")

    # STAGE 8: BEST COACH
    elif st.session_state.voted_stage == "best_coach":
        st.markdown("## 📋 Best Coach")
        st.write("*Recognizing the leader behind the bench who has best inspired their team and guided their growth this season.*")
        
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
           if st.button("NEXT →", key="btn_coach"):
    if st.session_state.selections.get('best_coach'):
        trigger_basketball_gif("coach") # Coach celebration GIF
        time.sleep(1.5)
        # Change 'final_review' to whatever your next stage is
        st.session_state.voted_stage = "final_review" 
        st.rerun()
    else:
        trigger_blue_warning()
        trigger_basketball_gif("error") # Technical Foul
    
    # STAGE 9: FUN AWARDS
    elif st.session_state.voted_stage == "fun_awards":
        st.markdown("## ✨ Fun Season Awards")

        # All selectboxes here use the filtered 'universal_nominees' list
        s_supporter = st.selectbox("📣 Best Supporter", options=[""] + universal_nominees, key="fun_supporter")
        s_party = st.selectbox("🍻 Party Animal", options=[""] + universal_nominees, key="fun_party")
        s_energy = st.selectbox("⚡ Best Energy", options=[""] + universal_nominees, key="fun_energy")
        s_karen = st.selectbox("👑 The 'Karen'", options=[""] + universal_nominees, key="fun_karen")
        s_late = st.selectbox("⏰ Always Late", options=[""] + universal_nominees, key="fun_late")
        s_forget = st.selectbox("🎒 The Forgetful One", options=[""] + universal_nominees, key="fun_forget")

        f_col1, f_col2 = st.columns(2)
        
        with f_col1:
            if st.button("← BACK", key="f_back"):
                st.session_state.voted_stage = "best_coach"
                st.rerun()
                
        with f_col2:
            if st.button("SUBMIT 🏀", key="final_submit_btn"):
                fun_votes = [s_supporter, s_party, s_energy, s_karen, s_late, s_forget]
                
                if all(val != "" for val in fun_votes) or st.session_state.get('is_admin'):
                    data = {
                        "name": st.session_state.user_name,
                        "team": st.session_state.user_team,
                        "rookie_vote": st.session_state.selections.get('rookie_of_the_year'),
                        "mip_vote": st.session_state.selections.get('most_improved_player'),
                        "dpoy_vote": st.session_state.selections.get('defensive_player'),
                        "best_driver": st.session_state.selections.get('best_driver'),
                        "best_shooter": st.session_state.selections.get('best_shooter'),
                        "best_rebounder": st.session_state.selections.get('best_rebounder'),
                        "best_coach": st.session_state.selections.get('best_coach'),
                        "best_supporter": s_supporter,
                        "party_animal": s_party,
                        "energy": s_energy,
                        "karen": s_karen,
                        "always_late": s_late,
                        "always_forgets": s_forget
                    }
                    
                    try:
                        supabase.table(TABLE_NAME).insert(data).execute()
                        # Move to the new event details page
                        st.session_state.voted_stage = "event_details"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Database Error: {e}")
                else:
                    trigger_blue_warning()

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
