import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. הגדרות מערכת קבועות ---
st.set_page_config(page_title="VibeLab Pro", page_icon="🎸", layout="wide")

# שמירה על זיכרון המערכת כדי למנוע קריסות
if 'history' not in st.session_state: st.session_state.history = []
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. עיצוב 4K קבוע (לא משתנה בלחיצה) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
        url('https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=3840');
        background-size: cover;
        background-attachment: fixed;
    }
    
    .main-header {
        font-family: 'Arial Black', sans-serif;
        font-size: 80px;
        color: #1DB954;
        text-align: center;
        text-shadow: 0 0 20px rgba(29, 185, 84, 0.5);
        margin-bottom: 0px;
    }

    /* תיבת הקלט - שחור אטום לקריאות מושלמת */
    .input-panel {
        background: rgba(0, 0, 0, 0.9);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #1DB954;
        margin: 20px 0;
    }

    label { color: #1DB954 !important; font-weight: bold !important; font-size: 1.1rem !important; }

    /* עיצוב שדות הקלט - לבן נקי */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: white !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }

    .song-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 15px;
        border-right: 5px solid #1DB954;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. חיבור חסין לספוטיפיי ---
@st.cache_resource(show_spinner=False)
def get_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except:
        return None

sp = get_spotify()

# --- 4. ממשק המשתמש ---
st.markdown('<h1 class="main-header">VIBELAB</h1>', unsafe_allow_html=True)

# כפתור היסטוריה בולט
col_empty, col_hist = st.columns([4, 1])
with col_hist:
    if st.button("📜 היסטוריית פלייליסטים"):
        st.toast("ההיסטוריה נפתחה בצד שמאל!")
        # כאן ה-Sidebar יפתח אוטומטית ב-Streamlit Cloud

st.markdown('<div class="input-panel">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    u_name = st.text_input("Name", placeholder="הכנס שם...") # שדה נקי ללא Guest
with c2:
    # סגנון רוק מופיע כאן ראשון וקבוע
    u_genre = st.selectbox("Genre", ["Rock", "Techno", "Hip Hop", "Pop", "Israeli", "Jazz"])
with c3:
    u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Chill"])

if st.button("CREATE MY EXPERIENCE ⚡"):
    if not sp:
        st.error("שגיאת חיבור. בדוק את המפתחות ב-Secrets.")
    elif not u_name:
        st.warning("חובה להזין שם.")
    else:
        with st.spinner('מחפש שירים...'):
            try:
                # הוספת המתנה קצרה למניעת חסימת API
                time.sleep(1) 
                res = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=10, type='track')
                if res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': res['tracks']['items']})
                    st.balloons()
            except Exception as e:
                st.error("ספוטיפיי עמוסה כרגע. המתן 20 שניות ונסה שוב.")

st.markdown('</div>', unsafe_allow_html=True)

# --- 5. הצגת התוצאות ---
if st.session_state.tracks:
    st.markdown(f"### ✨ Curated for {u_name}:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div class="song-card">
            <div style="display:flex; align-items:center; gap:15px; text-align:right; direction:rtl;">
                <img src="{t['album']['images'][0]['url']}" width="70" style="border-radius:10px;">
                <div style="flex-grow:1;">
                    <div style="color:#1DB954; font-size:0.8rem;">{t['artists'][0]['name']}</div>
                    <div style="font-size:1.2rem; font-weight:bold; color:white;">{t['name']}</div>
                    <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none;">האזן בספוטיפיי ←</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if t.get('preview_url'):
            st.audio(t['preview_url'])

# --- 6. היסטוריה ב-Sidebar ---
with st.sidebar:
    st.title("היסטוריה")
    if not st.session_state.history:
        st.write("אין פלייליסטים קודמים.")
    for i, item in enumerate(reversed(st.session_state.history)):
        if st.button(f"{item['name']} - {item['genre']}", key=f"btn_{i}"):
            st.session_state.tracks = item['tracks']
