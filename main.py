import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# הגדרות דף
st.set_page_config(page_title="VibeLab Ultra", page_icon="⚡", layout="wide")

# אתחול היסטוריה
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []

# עיצוב CSS ברמה של אתר פרימיום
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Assistant:wght@300;400;600&display=swap" rel="stylesheet">
<style>
    /* הגדרות גלובליות */
    * { font-family: 'Assistant', sans-serif; }
    
    .stApp {
        background: #050505;
        color: #ffffff;
    }

    /* Hero Section - תמונת כותרת מקצועית */
    .hero-container {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(5,5,5,1)), 
                    url('https://images.unsplash.com/photo-1514525253361-bee8718a74a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        padding: 100px 20px;
        text-align: center;
        border-radius: 0 0 50px 50px;
        margin: -60px -20px 40px -20px;
    }

    .hero-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 85px;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 0;
        background: linear-gradient(to right, #1DB954, #1ed760, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }

    .hero-subtitle {
        font-size: 24px;
        font-weight: 300;
        letter-spacing: 5px;
        text-transform: uppercase;
        opacity: 0.7;
        margin-top: 10px;
    }

    /* כרטיסיות הקלט */
    .input-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 25px;
        backdrop-filter: blur(20px);
    }

    /* עיצוב טקסט של כרטיסיות שירים */
    .track-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .artist-name {
        font-size: 1rem;
        color: #1DB954;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* כפתורים */
    .stButton>button {
        background: #1DB954 !important;
        color: black !important;
        border-radius: 12px !important;
        height: 3.5em !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        border: none !important;
        transition: 0.3s all !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(29, 185, 84, 0.3) !important;
    }

    /* תיקון היסטוריה בסידבר */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# פונקציית חיבור
@st.cache_resource
def get_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_spotify()

# --- ממשק משתמש ---

# Hero Section
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">VIBELAB</div>
        <div class="hero-subtitle">Personalized Soundscapes</div>
    </div>
""", unsafe_allow_html=True)

# סידבר היסטוריה
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>🕒 Session History</h2>", unsafe_allow_html=True)
    for i, entry in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"🎵 {entry['genre']} - {entry['vibe']}", key=f"h_{i}"):
            st.session_state.current_tracks = entry['tracks']

# אזור קלט מעוצב
st.markdown('<div class="input-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1, 1])
with c1:
    user_name = st.text_input("שם המשתמש", placeholder="הכנס שם...")
with c2:
    selected_genre = st.selectbox("ז'אנר", ["Techno", "Rock", "Hip Hop", "Israeli", "Indie", "Jazz", "Metal"])
with c3:
    selected_vibe = st.selectbox("אווירה", ["Late Night", "Gym Flow", "Deep Chill", "Party Mode", "Focus"])

generate = st.button("Generate Playlist ⚡")
st.markdown('</div>', unsafe_allow_html=True)

# לוגיקה
if generate and user_name:
    if sp:
        with st.spinner('Curating your vibe...'):
            results = sp.search(q=f"genre:{selected_genre} {selected_vibe}", limit=12, type='track')
            if results['tracks']['items']:
                st.session_state.current_tracks = results['tracks']['items']
                st.session_state.playlist_history.append({
                    'genre': selected_genre,
                    'vibe': selected_vibe,
                    'tracks': results['tracks']['items']
                })
            else:
                st.error("No tracks found.")
    else:
        st.error("Connection Error.")

# תצוגת שירים
if st.session_state.current_tracks:
    st.markdown("<br><h2 style='letter-spacing:-1px;'>Current Selection</h2>", unsafe_allow_html=True)
    
    for track in st.session_state.current_tracks:
        st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:20px; margin-bottom:15px; border:1px solid rgba(255,255,255,0.05);">
                <div style="display:flex; align-items:center; gap:25px;">
                    <img src="{track['album']['images'][0]['url']}" width="120" style="border-radius:15px; box-shadow:0 10px 20px rgba(0,0,0,0.4);">
                    <div style="flex-grow:1;">
                        <div class="artist-name">{track['artists'][0]['name']}</div>
                        <div class="track-name">{track['name']}</div>
                        <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:700; font-size:14px;">LISTEN ON SPOTIFY →</a>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        preview = track.get('preview_url')
        if preview:
            st.audio(preview)
