import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. הגדרות דף ---
st.set_page_config(page_title="VibeLab Elite", page_icon="🎵", layout="wide")

# אתחול זיכרון
if 'tracks' not in st.session_state: st.session_state.tracks = []
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. עיצוב 4K נקי (ללא מלבנים מיותרים) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=3840');
        background-size: cover;
        background-attachment: fixed;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 70px;
        font-weight: 900;
        color: #1DB954;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 0 30px rgba(29, 185, 84, 0.5);
    }
    /* פאנל שליטה נקי */
    .control-panel {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    label { color: #1DB954 !important; font-weight: bold !important; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: white !important;
        color: black !important;
        font-weight: bold !important;
    }
    /* כפתור יוקרתי רחב */
    .stButton>button {
        width: 100% !important;
        background-color: #1DB954 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        height: 50px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. חיבור לספוטיפיי ---
@st.cache_resource
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_sp()

# --- 4. ממשק האפליקציה ---
st.markdown('<h1 class="main-title">VIBELAB</h1>', unsafe_allow_html=True)

# כפתור היסטוריה בראש העמוד
col_e, col_h = st.columns([5, 1])
with col_h:
    if st.button("📜 MY HISTORY"):
        st.session_state.show_history = not st.session_state.get('show_history', False)

if st.session_state.get('show_history', False):
    st.info("Sessions saved: " + str(len(st.session_state.history)))
    for h in st.session_state.history:
        if st.button(f"Load: {h['name']} ({h['genre']})"):
            st.session_state.tracks = h['tracks']

st.markdown('<div class="control-panel">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    u_name = st.text_input("Name", placeholder="Your Name...")
with c2:
    u_genre = st.selectbox("Genre", ["Rock", "Techno", "Pop", "Hip Hop", "Israeli"])
with c3:
    u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Deep Focus"])

if st.button("INITIATE SOUNDSCAPE ⚡"):
    if not u_name:
        st.warning("Please enter your name.")
    else:
        with st.spinner('Syncing...'):
            try:
                # ניסיון חיפוש בספוטיפיי
                res = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=10, type='track')
                if not res['tracks']['items']:
                    res = sp.search(q=f"{u_genre}", limit=10, type='track')
                
                st.session_state.tracks = res['tracks']['items']
                st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': res['tracks']['items']})
                st.balloons()
            except:
                # מנגנון הגיבוי - אם ספוטיפיי חוסמת, האתר עדיין עובד!
                st.info("Spotify API limit reached. Using VibeLab local archive...")
                # כאן אפשר להוסיף רשימה קבועה לגיבוי
                st.session_state.tracks = [] 
                st.error("Please try again in 10 seconds.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. הצגת התוצאות (כרטיסים נקיים) ---
if st.session_state.tracks:
    st.markdown(f"<h3 style='color:white; text-align:center;'>Curated for {u_name}</h3>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, t in enumerate(st.session_state.tracks):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; border-left:5px solid #1DB954; margin-bottom:10px; display:flex; align-items:center; gap:15px;">
                <img src="{t['album']['images'][0]['url']}" width="70" style="border-radius:8px;">
                <div>
                    <div style="color:#1DB954; font-size:0.8rem;">{t['artists'][0]['name']}</div>
                    <div style="color:white; font-size:1.1rem; font-weight:bold;">{t['name']}</div>
                    <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none;">PLAY →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
