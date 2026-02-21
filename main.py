import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# --- 1. הגדרות מערכת חסינות ---
st.set_page_config(
    page_title="VibeLab Infinity",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# זיכרון פנימי למניעת כפילויות ושגיאות API
if 'history' not in st.session_state: st.session_state.history = []
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. עיצוב ELITE צבעוני וחסין שגיאות (CSS) ---
st.markdown("""
<style>
    /* רקע 4K עוצמתי וקבוע - לא משתנה בלחיצה */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&w=3840&q=100');
        background-size: cover;
        background-attachment: fixed;
    }

    /* כותרת ניאון צבעונית */
    .hero-title {
        font-family: 'Arial Black', sans-serif;
        font-size: clamp(40px, 10vw, 90px);
        text-align: center;
        color: #1DB954;
        text-shadow: 0 0 20px rgba(29, 185, 84, 0.6);
        margin-top: -50px;
    }

    /* פאנל שליטה אטום - למניעת דריסת טקסט */
    .control-panel {
        background: rgba(0, 0, 0, 0.95);
        padding: 30px;
        border-radius: 25px;
        border: 2px solid #1DB954;
        margin-bottom: 30px;
        box-shadow: 0 10px 50px rgba(0,0,0,0.5);
    }

    /* עיצוב שדות קלט קריאים במיוחד */
    label { color: #1DB954 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    
    .stTextInput>div>div>input {
        background-color: white !important;
        color: black !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* כפתור היסטוריה צף וברור */
    .stSidebar [data-testid="stVerticalBlock"] {
        padding-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. חיבור חכם לספוטיפיי (Multi-User Safe) ---
@st.cache_resource(show_spinner=False)
def connect_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except:
        return None

sp = connect_spotify()

# --- 4. ממשק האפליקציה ---
st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)

# כפתור היסטוריה גדול בראש העמוד (ליד הכותרת)
col_title, col_hist = st.columns([3, 1])
with col_hist:
    if st.button("📜 HISTORY ARCHIVE"):
        st.info("פתח את התפריט בצד שמאל ←")

st.markdown('<div class="control-panel">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    # שדה Name נקי לגמרי
    u_name = st.text_input("Name", placeholder="Enter your name...")
with c2:
    # רוק מופיע וקבוע
    u_genre = st.selectbox("Genre", ["Rock", "Techno", "Hip Hop", "Pop", "Israeli", "Jazz", "Lounge"])
with c3:
    u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Focus"])

if st.button("CREATE THE EXPERIENCE ⚡"):
    if not sp:
        st.error("Connection Error. Check Secrets.")
    elif not u_name:
        st.warning("Please enter your Name.")
    else:
        with st.spinner('Syncing Soundwaves...'):
            try:
                # המתנה קלה למניעת חסימת API
                time.sleep(0.5)
                res = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=12, type='track')
                if res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': res['tracks']['items']})
                    st.balloons()
            except:
                st.error("Spotify is a bit busy. Try one more time in 10 seconds.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. הצגת פלייליסט ---
if st.session_state.tracks:
    st.markdown(f"<h2 style='color:white; text-align:center;'>CURATED FOR {u_name.upper()}</h2>", unsafe_allow_html=True)
    grid = st.columns(2)
    for idx, t in enumerate(st.session_state.tracks):
        with grid[idx % 2]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.08); padding:20px; border-radius:20px; border-right:5px solid #1DB954; margin-bottom:15px; display:flex; align-items:center; gap:15px;">
                <img src="{t['album']['images'][0]['url']}" width="80" style="border-radius:10px;">
                <div>
                    <div style="color:#1DB954; font-weight:bold; font-size:0.8rem;">{t['artists'][0]['name']}</div>
                    <div style="font-size:1.3rem; font-weight:900; color:white;">{t['name']}</div>
                    <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">PLAY →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if t.get('preview_url'):
                st.audio(t['preview_url'])

# --- 6. היסטוריה נשלפת ב-Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>PAST VIBES</h2>", unsafe_allow_html=True)
    for i, item in enumerate(reversed(st.session_state.history)):
        if st.button(f"Session {len(st.session_state.history)-i}: {item['genre']}", key=f"hist_{i}"):
            st.session_state.tracks = item['tracks']
