import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Page Configuration
st.set_page_config(page_title="VibeLab | AI Soundtrack", page_icon="🎧", layout="wide")

# Initialize Session State for stability
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []

# Dynamic Background Feature
bg_images = [
    "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1920",
    "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920",
    "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920",
    "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=1920",
    "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=1920"
]
selected_bg = random.choice(bg_images)

# Advanced CSS for a Professional, Clean UI
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
    body {{
        color: white;
    }}
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), url('{selected_bg}');
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* VIBELAB Hero Header */
    .hero-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 100px;
        text-align: center;
        background: linear-gradient(to right, #1DB954, #1ed760, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: -4px;
        line-height: 1;
    }}

    .hero-subtitle {{
        font-family: 'Inter', sans-serif;
        text-align: center;
        font-size: 1.2rem;
        letter-spacing: 4px;
        text-transform: uppercase;
        opacity: 0.7;
        margin-top: 10px;
        margin-bottom: 40px;
    }}

    /* High Contrast Labels */
    label {{
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #1DB954 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Input Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: white !important;
        color: black !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: 2px solid #1DB954 !important;
    }}

    /* Glassmorphism Track Cards */
    .track-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: 0.4s ease;
    }}
    .track-card:hover {{
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-5px);
        border-color: #1DB954;
    }}

    /* Action Button */
    .stButton>button {{
        background: #1DB954 !important;
        color: black !important;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 50px !important;
        padding: 20px !important;
        font-size: 1.2rem !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 20px;
    }}

    /* Sidebar History */
    [data-testid="stSidebar"] {{
        background-color: rgba(0, 0, 0, 0.5);
        border-right: 1px solid rgba(255,255,255,0.1);
    }}
</style>
""", unsafe_allow_html=True)

# Secure Spotify Connection
def get_spotify_session():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))
    except:
        return None

sp = get_spotify_session()

# --- Main Layout ---

st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Artificial Intelligence • Human Emotion</div>', unsafe_allow_html=True)

# Sidebar: History
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954; font-family:Montserrat;'>HISTORY</h2>", unsafe_allow_html=True)
    if not st.session_state.playlist_history:
        st.write("Your generated vibes will appear here.")
    for i, entry in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"🎵 {entry['genre']} | {entry['vibe']}", key=f"hist_{i}"):
            st.session_state.current_tracks = entry['tracks']

# Input Section
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("YOUR NAME", placeholder="Enter name...")
with col2:
    genre = st.selectbox("GENRE", ["Techno", "Rock", "Pop", "Hip Hop", "Israeli", "Jazz", "Metal", "Lo-Fi"])
with col3:
    vibe = st.selectbox("CURRENT VIBE", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Focus", "Morning Energy"])

if st.button("Generate My Experience ⚡"):
    if not sp:
        st.error("Connection failed. Please check credentials and Reboot.")
    elif not name:
        st.warning("Please enter your name to proceed.")
    else:
        with st.spinner('Curating your unique soundscape...'):
            try:
                # Optimized search query
                results = sp.search(q=f"genre:{genre} {vibe}", limit=12, type='track')
                if results['tracks']['items']:
                    tracks = results['tracks']['items']
                    st.session_state.current_tracks = tracks
                    st.session_state.playlist_history.append({'genre': genre, 'vibe': vibe, 'tracks': tracks})
                    st.balloons()
                else:
                    st.warning("No exact matches found. Try changing the genre.")
            except Exception:
                st.error("Spotify API limit reached. Please try again in 60 seconds.")

# Result Display
if st.session_state.current_tracks:
    st.markdown(f"### ✨ Curated for {name}:")
    
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:25px;">
                <img src="{track['album']['images'][0]['url']}" width="110" style="border-radius:12px; box-shadow: 0 10px 20px rgba(0,0,0,0.5);">
                <div style="flex-grow:1;">
                    <div style="color:#1DB954; font-weight:800; font-size:0.9rem; letter-spacing:1px;">{track['artists'][0]['name'].upper()}</div>
                    <div style="font-size:1.6rem; font-weight:900; margin-bottom:10px;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; font-weight:bold; text-decoration:none; font-size:0.9rem;">LISTEN ON SPOTIFY ➜</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio Player (with safety check)
        preview = track.get('preview_url')
        if preview:
            st.audio(preview)
