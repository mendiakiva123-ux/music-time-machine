import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. הגדרות מערכת ---
st.set_page_config(page_title="VibeLab Israel Pro", page_icon="🎧", layout="centered")

if 'tracks' not in st.session_state: st.session_state.tracks = []
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. עיצוב מובייל יוקרתי (4K) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=1080&q=80');
        background-size: cover;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 55px;
        font-weight: 900;
        color: #1DB954;
        text-align: center;
        text-shadow: 0 0 20px rgba(29, 185, 84, 0.4);
    }
    .mobile-panel {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 10px;
    }
    label { color: #1DB954 !important; font-weight: bold !important; font-size: 1rem !important; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: white !important; color: black !important; font-weight: bold !important; border-radius: 12px !important;
    }
    .song-item {
        background: rgba(0, 0, 0, 0.7);
        padding: 15px;
        border-radius: 20px;
        border-right: 5px solid #1DB954;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
        direction: rtl;
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

# --- 4. הגדרת ז'אנרים וזמרים (מעודכן 2024-2025) ---
GENRE_MAP = {
    "מזרחית": ["עומר אדם", "אושר כהן", "אייל גולן", "עדן חסון", "פאר טסי", "נס וסטילה"],
    "ישראלי / פופ": ["חנן בן ארי", "נועה קירל", "אנה זק", "סטטיק", "רביב כנר", "יסמין מועלם"],
    "רוק ישראלי": ["שלמה ארצי", "ברי סחרוף", "טונה", "רביד פלוטניק", "היהודים"],
    "Techno / Electronic": ["Artbat", "Solomun", "Vintage Culture", "Innellea"],
    "Hip Hop": ["Drake", "Travis Scott", "Kendrick Lamar", "Eminem"]
}

# --- 5. ממשק המשתמש ---
st.markdown('<h1 class="main-title">VIBELAB</h1>', unsafe_allow_html=True)

# כפתור היסטוריה קטן
c_space, c_hist = st.columns([5, 1])
with c_hist:
    if st.button("📜"):
        st.toast("ההיסטוריה נשמרה בצד!")

st.markdown('<div class="mobile-panel">', unsafe_allow_html=True)

u_name = st.text_input("Name", placeholder="איך קוראים לך?")
u_genre = st.selectbox("בחר סגנון", list(GENRE_MAP.keys()))

# פילטור זמרים דינמי לפי הז'אנר שנבחר
u_artist = st.selectbox(f"זמרים מובילים ב-{u_genre}", GENRE_MAP[u_genre])

if st.button("צור לי פלייליסט מנצח ⚡", use_container_width=True):
    if not u_name:
        st.error("חובה להזין שם!")
    else:
        with st.spinner('מושך את הלהיטים הכי חמים...'):
            try:
                # חיפוש לפי השם של הזמר שנבחר - תמיד יביא את השירים הכי פופולריים שלו כיום
                results = sp.search(q=f"artist:{u_artist}", limit=15, type='track')
                if results and results['tracks']['items']:
                    st.session_state.tracks = results['tracks']['items']
                    st.session_state.history.append({'name': u_name, 'genre': u_genre, 'artist': u_artist, 'tracks': results['tracks']['items']})
                    st.balloons()
                else:
                    st.warning("לא מצאתי שירים כרגע, נסה שוב.")
            except:
                st.error("שגיאת חיבור לספוטיפיי. נסה שוב בעוד 10 שניות.")

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. הצגת השירים (עיצוב מובייל) ---
if st.session_state.tracks:
    st.markdown(f"<p style='color:white; text-align:center; font-size:1.2rem; margin-top:20px;'>הפלייליסט של {u_name}:</p>", unsafe_allow_html=True)
    
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div class="song-item">
            <img src="{t['album']['images'][0]['url']}" width="65" style="border-radius:12px;">
            <div style="flex-grow:1; text-align:right;">
                <div style="color:#1DB954; font-size:0.8rem; font-weight:bold;">{t['artists'][0]['name']}</div>
                <div style="color:white; font-size:1.1rem; font-weight:bold;">{t['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="background:#1DB954; color:white; padding:10px 18px; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:bold;">נגן</a>
        </div>
        """, unsafe_allow_html=True)

# היסטוריה בסידבר
with st.sidebar:
    st.header("היסטוריית האזנה")
    for h in reversed(st.session_state.history):
        if st.button(f"{h['name']} - {h['artist']}"):
            st.session_state.tracks = h['tracks']
