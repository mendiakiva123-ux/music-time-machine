import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import random

# --- 1. הגדרות דף ואפליקציה ---
st.set_page_config(page_title="VibeLab Pro", page_icon="🎵", layout="wide")

# אתחול זיכרון למניעת שגיאות
if 'history' not in st.session_state: st.session_state.history = []
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. עיצוב PRO (רקע אולפן, ללא מלבנים מיותרים) ---
st.markdown("""
<style>
    /* רקע אולפן מקצועי */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=3840');
        background-size: cover;
        background-attachment: fixed;
    }

    /* כותרת ניאון נקייה */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 70px;
        font-weight: 900;
        color: #1DB954;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: -2px;
    }

    /* פאנל שליטה שקוף (Glassmorphism) */
    .control-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }

    /* עיצוב שדות קלט */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background: white !important;
        color: black !important;
        border-radius: 12px !important;
        height: 45px !important;
        font-weight: bold !important;
    }

    label { color: white !important; font-size: 1rem !important; margin-bottom: 10px !important; }

    /* כרטיסי שירים בעיצוב מודרני */
    .song-box {
        background: rgba(0,0,0,0.6);
        border: 1px solid #1DB954;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .song-box:hover { transform: translateY(-5px); background: rgba(0,0,0,0.8); }
</style>
""", unsafe_allow_html=True)

# --- 3. חיבור חסין לספוטיפיי ---
@st.cache_resource(show_spinner=False)
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except:
        return None

sp = get_sp()

# --- 4. ממשק המשתמש ---
st.markdown('<h1 class="main-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#aaa; margin-top:-20px;">AI-POWERED MUSIC CURATION</p>', unsafe_allow_html=True)

# כפתור היסטוריה אלגנטי
col_left, col_right = st.columns([5,1])
with col_right:
    if st.button("📜 ARCHIVE"):
        st.toast("הארכיון פתוח משמאל")

st.markdown('<div class="control-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    u_name = st.text_input("NAME", placeholder="Enter your name...")
with c2:
    u_genre = st.selectbox("GENRE", ["Rock", "Techno", "Pop", "Hip Hop", "Israeli", "Jazz"])
with c3:
    u_vibe = st.selectbox("VIBE", ["Party Mode", "Gym Flow", "Late Night", "Deep Focus"])

if st.button("CREATE SOUNDSCAPE ⚡", use_container_width=True):
    if not u_name:
        st.error("Please enter your name first.")
    else:
        with st.spinner('Building your vibe...'):
            try:
                # מנגנון הגנה: המתנה קלה למניעת חסימה
                time.sleep(0.5)
                res = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=12, type='track')
                if res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': res['tracks']['items']})
                    st.balloons()
            except:
                # אם יש שגיאה - האפליקציה לא קורסת! היא מראה הודעה נעימה
                st.warning("Spotify is warming up. Please wait 10 seconds and click again.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. הצגת התוצאות ---
if st.session_state.tracks:
    st.markdown(f"<h2 style='color:white; text-align:center; margin-top:40px;'>Curated for {u_name}</h2>", unsafe_allow_html=True)
    
    # הצגה ב-3 עמודות למראה מקצועי
    cols = st.columns(3)
    for i, track in enumerate(st.session_state.tracks):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="song-box">
                <img src="{track['album']['images'][0]['url']}" style="width:100%; border-radius:15px; margin-bottom:15px;">
                <div style="color:#1DB954; font-weight:bold; font-size:0.9rem;">{track['artists'][0]['name']}</div>
                <div style="color:white; font-size:1.2rem; font-weight:bold; margin-bottom:10px;">{track['name']}</div>
                <a href="{track['external_urls']['spotify']}" target="_blank" style="color:white; text-decoration:none; background:#1DB954; padding:8px 15px; border-radius:10px; font-size:0.8rem; display:inline-block;">LISTEN</a>
            </div>
            """, unsafe_allow_html=True)

# --- 6. היסטוריה נשלפת ---
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>HISTORY</h2>", unsafe_allow_html=True)
    if not st.session_state.history:
        st.write("No vibes saved yet.")
    for i, h in enumerate(reversed(st.session_state.history)):
        if st.button(f"{h['name']} - {h['genre']}", key=f"h_{i}"):
            st.session_state.tracks = h['tracks']
