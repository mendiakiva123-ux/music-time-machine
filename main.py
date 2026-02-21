import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# הגדרות דף Pro
st.set_page_config(page_title="VibeLab Experience", page_icon="🎧", layout="wide")

# אתחול היסטוריה ושמירת מצב
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []

# עיצוב CSS - חוויית משתמש ייחודית ונוחה
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700;800&family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
    /* רקע מוזיקלי חי ואפלולי */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1459749411177-042180ce673c?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }

    /* כותרת ראשית עוצמתית */
    .hero-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 100px;
        text-align: center;
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: -5px;
    }

    /* שיפור נראות הטקסט בשדות הקלט */
    label {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: #1DB954 !important;
        text-shadow: 1px 1px 2px black;
        margin-bottom: 10px !important;
    }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        border: 2px solid #1DB954 !important;
    }

    /* כרטיסיות שירים מקצועיות */
    .track-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    .track-card:hover {
        transform: scale(1.02);
        background: rgba(255, 255, 255, 0.1);
    }

    /* כפתור יצירה */
    .stButton>button {
        background: #1DB954 !important;
        color: black !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        padding: 15px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# חיבור לספוטיפיי (עם המפתחות שלך מה-Secrets)
@st.cache_resource
def get_sp():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=st.secrets["CLIENT_ID"].strip(),
        client_secret=st.secrets["CLIENT_SECRET"].strip()
    ))

sp = get_sp()

# --- ממשק האתר ---

st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.5rem; opacity:0.8; margin-top:-20px;">Curating Your Moment</p>', unsafe_allow_html=True)

# סרגל צד להיסטוריה (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>🕒 Session History</h2>", unsafe_allow_html=True)
    for i, entry in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"🎵 {entry['genre']} | {entry['vibe']}", key=f"hist_{i}"):
            st.session_state.current_tracks = entry['tracks']

# אזור קלט - דגש על טקסט קריא
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    name = st.text_input("איך לקרוא לך?", placeholder="הכנס שם כאן...")
with col2:
    genre = st.selectbox("סגנון מוזיקלי מועדף", 
                        ["Rock", "Techno", "Pop", "Israeli", "Hip Hop", "Deep House", "Jazz", "Metal", "Indie"])
with col3:
    # השינוי שביקשת: "מה הוויב שלך כעת"
    vibe = st.selectbox("מה הוויב שלך כעת?", 
                       ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Focus", "Morning Energy"])

if st.button("Generate My Experience ⚡"):
    if sp and name:
        with st.spinner('יוצרים את הפסקול המושלם עבורך...'):
            q = f"genre:{genre} {vibe}"
            results = sp.search(q=q, limit=12, type='track')
            
            if results['tracks']['items']:
                st.session_state.current_tracks = results['tracks']['items']
                # שמירה להיסטוריה
                st.session_state.playlist_history.append({
                    'genre': genre, 'vibe': vibe, 'tracks': results['tracks']['items']
                })
                st.balloons()

# הצגת הפלייליסט
if st.session_state.current_tracks:
    st.markdown(f"### ✨ הפלייליסט שנבנה עבורך:")
    
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:25px;">
                <img src="{track['album']['images'][0]['url']}" width="110" style="border-radius:12px;">
                <div>
                    <div style="color:#1DB954; font-weight:800; font-size:0.9rem; text-transform:uppercase;">{track['artists'][0]['name']}</div>
                    <div style="font-size:1.6rem; font-weight:900; margin-bottom:10px;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="background:#1DB954; color:black; padding:8px 20px; border-radius:50px; text-decoration:none; font-weight:800; font-size:14px;">PLAY ON SPOTIFY ➜</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if track.get('preview_url'):
            st.audio(track['preview_url'])
