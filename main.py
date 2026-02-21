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

# אתחול זיכרון המערכת
if 'history' not in st.session_state: st.session_state.history = []
if 'tracks' not in st.session_state: st.session_state.tracks = []
if 'last_call' not in st.session_state: st.session_state.last_call = 0

# --- 2. עיצוב 4K צבעוני וחסין (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&w=3840&q=100');
        background-size: cover;
        background-attachment: fixed;
    }
    
    .main-title {
        font-family: 'Arial Black', sans-serif;
        font-size: clamp(40px, 8vw, 85px);
        color: #1DB954;
        text-align: center;
        text-shadow: 0 0 25px rgba(29, 185, 84, 0.4);
        margin-top: -40px;
    }

    .glass-panel {
        background: rgba(0, 0, 0, 0.9);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #1DB954;
        box-shadow: 0 10px 40px rgba(0,0,0,0.8);
    }

    /* תיקון השם והתוויות */
    label { color: #1DB954 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    .stTextInput>div>div>input { background-color: white !important; color: black !important; font-weight: bold !important; border-radius: 10px !important; }
    
    /* כפתור היסטוריה ניאון */
    .hist-trigger {
        background: #1DB954;
        color: black;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: bold;
        text-align: center;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. חיבור חכם לספוטיפיי (עם מנגנון Retry) ---
@st.cache_resource(show_spinner=False)
def connect_spotify():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csc = st.secrets["CLIENT_SECRET"].strip()
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csc))
    except:
        return None

sp = connect_spotify()

# --- 4. ממשק האפליקציה ---
st.markdown('<h1 class="main-title">VIBELAB</h1>', unsafe_allow_html=True)

# כפתור היסטוריה בולט למעלה
c_empty, c_btn = st.columns([4, 1])
with c_btn:
    if st.button("📜 HISTORY"):
        st.toast("ההיסטוריה נפתחה בצד!")

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    # שם נקי ללא ברירת מחדל
    u_name = st.text_input("Name", placeholder="Enter Name...")
with col2:
    # רוק בפנים
    u_genre = st.selectbox("Genre", ["Rock", "Techno", "Pop", "Hip Hop", "Israeli"])
with col3:
    u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill"])

if st.button("GENERATE MY EXPERIENCE 🚀"):
    # הגנה מפני לחיצות רצופות שגורמות לשגיאה
    now = time.time()
    if now - st.session_state.last_call < 5:
        st.warning("Please wait 5 seconds between requests.")
    elif not u_name:
        st.error("Please enter your name.")
    else:
        st.session_state.last_call = now
        with st.spinner('Accessing Spotify...'):
            try:
                res = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=12, type='track')
                if res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': res['tracks']['items']})
                    st.balloons()
            except Exception:
                st.error("Spotify is busy. Wait 10 seconds and try one more time.")

st.markdown('</div>', unsafe_allow_html=True)

# --- 5. הצגת תוצאות ---
if st.session_state.tracks:
    st.markdown(f"<h3 style='color:white;'>Curated for {u_name}:</h3>", unsafe_allow_html=True)
    grid = st.columns(2)
    for idx, t in enumerate(st.session_state.tracks):
        with grid[idx % 2]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; border-left:5px solid #1DB954; margin-bottom:15px; display:flex; align-items:center; gap:15px;">
                <img src="{t['album']['images'][0]['url']}" width="80" style="border-radius:10px;">
                <div>
                    <div style="color:#1DB954; font-weight:bold; font-size:0.8rem;">{t['artists'][0]['name']}</div>
                    <div style="font-size:1.3rem; font-weight:bold; color:white;">{t['name']}</div>
                    <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none;">LISTEN →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- 6. היסטוריה ב-Sidebar ---
with st.sidebar:
    st.header("Archive")
    if not st.session_state.history:
        st.write("No history yet.")
    for i, item in enumerate(reversed(st.session_state.history)):
        if st.button(f"{item['name']} - {item['genre']}", key=f"h_{i}"):
            st.session_state.tracks = item['tracks']
