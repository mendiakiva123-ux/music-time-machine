import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# הגדרות דף
st.set_page_config(page_title="VibeLab | Dynamic Experience", page_icon="⚡", layout="wide")

# אתחול Session State
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []

# רשימת מילות מפתח לתמונות רקע מתחלפות (מוזיקה בלבד)
bg_themes = ["concert", "recording-studio", "vinyl-records", "dj-mixer", "electric-guitar", "synthesizer"]
random_theme = random.choice(bg_themes)
bg_url = f"https://source.unsplash.com/featured/1920x1080?{random_theme}"

# עיצוב CSS - יוקרתי, קריא ודינמי
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
    /* רקע מתחלף בכל כניסה */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.9)), 
                    url('{bg_url}');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }}

    /* כותרת ענק מקצועית */
    .hero-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(50px, 8vw, 110px);
        text-align: center;
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -4px;
    }}

    /* עיצוב טקסט קריא ובולט לשדות קלט */
    label {{
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        color: #1ed760 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        padding-bottom: 10px;
    }}
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: white !important;
        color: black !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: 3px solid #1DB954 !important;
        font-size: 1.1rem !important;
    }}

    /* כרטיסיות שירים (Glassmorphism) */
    .track-card {{
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.3s ease;
    }}
    .track-card:hover {{
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.12);
        border-color: #1DB954;
    }}

    /* כפתור יצירה עוצמתי */
    .stButton>button {{
        background: linear-gradient(90deg, #1DB954, #1ed760) !important;
        color: black !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        padding: 18px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(29, 185, 84, 0.4) !important;
        width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# חיבור חזק לספוטיפיי (עם טיפול בשגיאות)
@st.cache_resource
def connect_to_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except Exception as e:
        st.error(f"שגיאת התחברות לספוטיפיי: {e}")
        return None

sp = connect_to_spotify()

# --- ממשק האתר ---

st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.4rem; opacity:0.9; font-weight:300;">Elevating Your Daily Soundtrack</p>', unsafe_allow_html=True)

# סרגל צד להיסטוריה
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>🕒 Session History</h2>", unsafe_allow_html=True)
    if not st.session_state.playlist_history:
        st.info("כאן יופיעו הפלייליסטים הקודמים שלך")
    for i, entry in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"🎼 {entry['genre']} | {entry['vibe']}", key=f"hist_{i}"):
            st.session_state.current_tracks = entry['tracks']

# אזור קלט
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    name = st.text_input("איך לקרוא לך?", placeholder="הכנס שם...")
with col2:
    genre = st.selectbox("סגנון מוזיקלי מועדף", ["Rock", "Techno", "Pop", "Israeli", "Hip Hop", "Indie", "Jazz", "Metal"])
with col3:
    vibe = st.selectbox("מה הוויב שלך כעת?", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Focus", "Morning Energy"])

if st.button("Generate My Experience ⚡"):
    if not sp:
        st.error("לא ניתן להתחבר לספוטיפיי. בדוק את ה-Secrets.")
    elif not name:
        st.warning("אנא הכנס שם כדי להמשיך.")
    else:
        with st.spinner('מנתחים את הוויב שלך...'):
            try:
                q = f"genre:{genre} {vibe}"
                results = sp.search(q=q, limit=12, type='track')
                
                if results['tracks']['items']:
                    st.session_state.current_tracks = results['tracks']['items']
                    st.session_state.playlist_history.append({
                        'genre': genre, 'vibe': vibe, 'tracks': results['tracks']['items']
                    })
                    st.balloons()
                else:
                    st.warning("לא נמצאו שירים מתאימים, נסה לשנות את הסגנון.")
            except Exception as e:
                st.error("הייתה תקלה קטנה מול ספוטיפיי. נסה לעשות Reboot לאפליקציה.")

# הצגת הפלייליסט
if st.session_state.current_tracks:
    st.markdown(f"<br><h3>✨ הפלייליסט המדויק עבורך, {name}:</h3>", unsafe_allow_html=True)
    
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:30px;">
                <img src="{track['album']['images'][0]['url']}" width="120" style="border-radius:15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="flex-grow:1;">
                    <div style="color:#1DB954; font-weight:800; font-size:1rem; text-transform:uppercase; letter-spacing:1px;">{track['artists'][0]['name']}</div>
                    <div style="font-size:1.8rem; font-weight:900; margin-bottom:12px; line-height:1.2;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="background:#1DB954; color:black; padding:10px 25px; border-radius:50px; text-decoration:none; font-weight:800; font-size:14px; display:inline-block;">LISTEN ON SPOTIFY ➜</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        preview = track.get('preview_url')
        if preview:
            st.audio(preview)
