import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. הגדרות דף וחזותיות ---
st.set_page_config(page_title="VibeLab Elite | Global Music Engine", page_icon="🎵", layout="wide")

# CSS מתקדם - עיצוב בינלאומי
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }

    /* כרטיסיות שירים בסגנון Glassmorphism */
    .song-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .song-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
        border-color: #1DB954;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .main-title {
        background: linear-gradient(90deg, #1DB954, #19e68c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 70px;
        font-weight: 900;
        text-align: center;
        letter-spacing: -2px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5rem;
        background: linear-gradient(90deg, #1DB954, #1ed760) !important;
        color: black !important;
        font-weight: bold;
        text-transform: uppercase;
        border: none;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(29, 185, 84, 0.4);
    }
    
    /* עיצוב היסטוריה */
    .history-item {
        font-size: 0.9rem;
        padding: 5px 10px;
        background: rgba(255,255,255,0.1);
        border-radius: 5px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. ניהול מצב (Session State) ---
if 'history' not in st.session_state: st.session_state.history = []
if 'platform' not in st.session_state: st.session_state.platform = "Spotify"

# --- 3. לוגיקת חיבור חסינה ---
def get_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"], 
            client_secret=st.secrets["CLIENT_SECRET"]
        ))
    except Exception:
        return None

# --- 4. ממשק משתמש עליון ---
st.markdown('<h1 class="main-title">VIBELAB <span style="font-size:20px; color:white; vertical-align:middle;">ELITE</span></h1>', unsafe_allow_html=True)

# בחירת פלטפורמה (עיצוב מודרני)
col_p1, col_p2 = st.columns(2)
with col_p1:
    if st.button("🟢 Spotify", key="sp_btn"): st.session_state.platform = "Spotify"
with col_p2:
    if st.button("🔴 Apple Music (Coming Soon)", key="ap_btn"): st.session_state.platform = "Apple"

st.divider()

# טופס קלט חכם
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        u_name = st.text_input("What's your name?", placeholder="Enter name to personalize...")
    with col2:
        u_genre = st.selectbox("Genre", ["Israeli Pop", "Mizrachi", "Techno", "Hip Hop", "Lofi"])
    with col3:
        u_vibe = st.selectbox("Vibe", ["Workout", "Chill Night", "Party Mode", "Focus"])

# --- 5. מנוע יצירה ---
if st.button("Generate My Experience ⚡"):
    if not u_name:
        st.error("Wait! We need your name to build the vibe.")
    else:
        sp = get_spotify()
        if not sp:
            st.warning("Connection issue. Please check API keys.")
        else:
            with st.status("Analyzing your vibe...", expanded=True) as status:
                st.write("Searching global charts...")
                time.sleep(1) # אפקט פסיכולוגי של "עבודה"
                try:
                    query = f"{u_genre} {u_vibe}"
                    results = sp.search(q=query, limit=12)
                    tracks = results['tracks']['items']
                    
                    if tracks:
                        st.session_state.current_mix = tracks
                        st.session_state.history.append(f"{u_name}: {u_genre} ({u_vibe})")
                        status.update(label="Vibe Sync Complete!", state="complete")
                        st.balloons()
                    else:
                        st.error("No tracks found. Try a different vibe!")
                except Exception as e:
                    st.error("Global servers are busy. Try again.")

# --- 6. תצוגת תוצאות פרימיום ---
if 'current_mix' in st.session_state:
    st.markdown(f"### ✨ {u_name}'s {u_vibe} Mix")
    
    # תצוגת גריד (Grid)
    cols = st.columns(2)
    for idx, t in enumerate(st.session_state.current_mix):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="song-card">
                <img src="{t['album']['images'][0]['url']}" width="80" style="border-radius:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                <div style="flex-grow:1;">
                    <div style="font-size:1.1rem; font-weight:700; margin-bottom:4px;">{t['name']}</div>
                    <div style="color:#1DB954; font-weight:500;">{t['artists'][0]['name']}</div>
                </div>
                <a href="{t['external_urls']['spotify']}" target="_blank">
                    <div style="background:#1DB954; color:black; padding:8px 15px; border-radius:30px; font-weight:bold; font-size:12px;">LISTEN</div>
                </a>
            </div>
            """, unsafe_allow_html=True)

# --- 7. Sidebar היסטוריה ומידע ---
with st.sidebar:
    st.markdown("### 📜 Session History")
    for h in st.session_state.history[::-1]:
        st.markdown(f'<div class="history-item">{h}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 🚀 Pro Tip")
    st.info("Try mixing 'Israeli' with 'Techno' for a unique party vibe!")
