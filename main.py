import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. הגדרות דף ---
st.set_page_config(page_title="VibeLab Infinity", page_icon="🎵", layout="wide")

# אתחול זיכרון
if 'tracks' not in st.session_state: st.session_state.tracks = []
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. עיצוב PRO מוזיקלי (4K) ---
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
        font-size: 80px;
        font-weight: 900;
        color: #1DB954;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 0 30px rgba(29, 185, 84, 0.5);
    }
    .control-panel {
        background: rgba(0, 0, 0, 0.85);
        padding: 35px;
        border-radius: 25px;
        border: 2px solid #1DB954;
        margin-top: 20px;
    }
    label { color: #1DB954 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: white !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    .song-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        border-right: 5px solid #1DB954;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .song-card:hover { background: rgba(255, 255, 255, 0.1); transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

# --- 3. חיבור חכם לספוטיפיי ---
@st.cache_resource(show_spinner=False)
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_sp()

# --- 4. ממשק המשתמש ---
st.markdown('<h1 class="main-title">VIBELAB</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>ARCHIVE</h2>", unsafe_allow_html=True)
    if st.session_state.history:
        for i, h in enumerate(reversed(st.session_state.history)):
            if st.button(f"{h['name']} - {h['genre']}", key=f"h_{i}"):
                st.session_state.tracks = h['tracks']
    else:
        st.write("No history yet.")

st.markdown('<div class="control-panel">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    u_name = st.text_input("Name", placeholder="What's your name?")
with c2:
    u_genre = st.selectbox("Genre", ["Rock", "Techno", "Hip Hop", "Pop", "Israeli", "Jazz"])
with c3:
    u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Deep Focus"])

if st.button("GET THE VIBE ⚡", use_container_width=True):
    if not u_name:
        st.error("Please enter your name.")
    elif not sp:
        st.error("Spotify Connection Failed.")
    else:
        with st.spinner('Searching for hits...'):
            try:
                # אסטרטגיית חיפוש ב-3 שלבים כדי להבטיח תוצאות
                query = f"genre:{u_genre} {u_vibe}"
                res = sp.search(q=query, limit=12, type='track')
                
                # אם לא מצא תוצאות מדויקות, נסה חיפוש רחב יותר
                if not res['tracks']['items']:
                    res = sp.search(q=f"{u_genre} {u_vibe}", limit=12, type='track')
                
                # אם עדיין לא מצא, נסה רק לפי ז'אנר
                if not res['tracks']['items']:
                    res = sp.search(q=f"genre:{u_genre}", limit=12, type='track')

                if res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': res['tracks']['items']})
                    st.balloons()
                else:
                    st.warning("Could not find songs. Try a different Vibe.")
            except:
                st.error("Spotify is busy. Wait 10 seconds and try again.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. הצגת התוצאות ---
if st.session_state.tracks:
    st.markdown(f"<h2 style='color:white; text-align:center; margin-top:30px;'>Top Tracks for {u_name}</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, t in enumerate(st.session_state.tracks):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="song-card">
                <div style="display:flex; align-items:center; gap:20px;">
                    <img src="{t['album']['images'][0]['url']}" width="90" style="border-radius:12px;">
                    <div>
                        <div style="color:#1DB954; font-weight:bold; font-size:0.9rem;">{t['artists'][0]['name']}</div>
                        <div style="color:white; font-size:1.4rem; font-weight:bold;">{t['name']}</div>
                        <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; font-weight:bold; text-decoration:none;">PLAY →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
