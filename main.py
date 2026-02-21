import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. הגדרות מערכת ואפליקציה ---
st.set_page_config(
    page_title="VibeLab Infinity",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# אתחול זיכרון למניעת קריסות
if 'history' not in st.session_state: st.session_state.history = []
if 'tracks' not in st.session_state: st.session_state.tracks = []
if 'last_action_time' not in st.session_state: st.session_state.last_action_time = 0

# --- 2. עיצוב 4K צבעוני וקבוע (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&w=3840&q=100');
        background-size: cover;
        background-attachment: fixed;
    }
    
    .hero-text {
        font-family: 'Arial Black', sans-serif;
        font-size: clamp(40px, 8vw, 80px);
        color: #1DB954;
        text-align: center;
        text-shadow: 0 0 20px rgba(29, 185, 84, 0.5);
        margin-top: -30px;
    }

    .main-container {
        background: rgba(0, 0, 0, 0.9);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #1DB954;
        box-shadow: 0 10px 50px rgba(0,0,0,0.7);
    }

    /* תוויות ושדות קלט */
    label { color: #1DB954 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    .stTextInput>div>div>input { background-color: white !important; color: black !important; font-weight: bold !important; border-radius: 8px !important; }
    
    /* כרטיסי שירים */
    .song-card {
        background: rgba(255, 255, 255, 0.07);
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #1DB954;
        margin-bottom: 12px;
        transition: 0.3s;
    }
    .song-card:hover { background: rgba(255, 255, 255, 0.15); }
</style>
""", unsafe_allow_html=True)

# --- 3. חיבור חכם לספוטיפיי (עם Cache למניעת שגיאות) ---
@st.cache_resource(show_spinner=False)
def get_spotify_instance():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except:
        return None

sp = get_spotify_instance()

# --- 4. ממשק האפליקציה ---
st.markdown('<h1 class="hero-text">VIBELAB</h1>', unsafe_allow_html=True)

# כפתור היסטוריה מהיר
col_space, col_history = st.columns([4, 1])
with col_history:
    if st.button("📜 HISTORY ARCHIVE"):
        st.info("ההיסטוריה נפתחה בתפריט הצד!")

st.markdown('<div class="main-container">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    # שם נקי ללא טקסט קבוע
    u_name = st.text_input("Name", placeholder="Enter your name...")
with c2:
    # סגנון Rock תמיד ראשון וקיים
    u_genre = st.selectbox("Genre", ["Rock", "Techno", "Hip Hop", "Pop", "Israeli", "Jazz"])
with c3:
    u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Deep Focus"])

if st.button("GENERATE EXPERIENCE ⚡"):
    now = time.time()
    # הגנה מפני לחיצות מהירות מדי (Cooldown של 5 שניות)
    if now - st.session_state.last_action_time < 5:
        st.warning("Please wait 5 seconds before generating again to avoid Spotify block.")
    elif not u_name:
        st.error("Please enter your name.")
    elif not sp:
        st.error("Connection Error. Please check your Spotify API keys.")
    else:
        st.session_state.last_action_time = now
        with st.spinner('Curating your soundscape...'):
            try:
                # חיפוש שירים
                results = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=12, type='track')
                if results and results['tracks']['items']:
                    st.session_state.tracks = results['tracks']['items']
                    st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': results['tracks']['items']})
                    st.balloons()
                else:
                    st.warning("No tracks found for this selection. Try another vibe!")
            except Exception:
                st.error("Spotify API is currently overloaded. Please wait 30 seconds.")

st.markdown('</div>', unsafe_allow_html=True)

# --- 5. תצוגת תוצאות מקצועית ---
if st.session_state.tracks:
    st.markdown(f"<h2 style='color:white; text-align:center;'>FOR {u_name.upper()}</h2>", unsafe_allow_html=True)
    res_cols = st.columns(2)
    for idx, track in enumerate(st.session_state.tracks):
        with res_cols[idx % 2]:
            st.markdown(f"""
            <div class="song-card">
                <div style="display:flex; align-items:center; gap:15px;">
                    <img src="{track['album']['images'][0]['url']}" width="75" style="border-radius:10px;">
                    <div>
                        <div style="color:#1DB954; font-weight:bold; font-size:0.8rem;">{track['artists'][0]['name']}</div>
                        <div style="font-size:1.2rem; font-weight:bold; color:white;">{track['name']}</div>
                        <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none;">PLAY ON SPOTIFY →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if track.get('preview_url'):
                st.audio(track['preview_url'])

# --- 6. היסטוריה ב-Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>PAST SESSIONS</h2>", unsafe_allow_html=True)
    if not st.session_state.history:
        st.write("Your history will appear here.")
    for i, session in enumerate(reversed(st.session_state.history)):
        if st.button(f"{session['name']} - {session['genre']}", key=f"hist_{i}"):
            st.session_state.tracks = session['tracks']
