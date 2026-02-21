import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time
from datetime import datetime

# --- SYSTEM & STABILITY ---
st.set_page_config(page_title="VibeLab | Premium AI Sound", page_icon="💎", layout="wide")

# Persistent State to prevent API flooding
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []
if 'current_bg' not in st.session_state:
    bgs = [
        "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=1920",
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920",
        "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920",
        "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1920"
    ]
    st.session_state.current_bg = random.choice(bgs)

# --- LUXURY UI DESIGN (CSS) ---
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
    /* Full Page Background */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url('{st.session_state.current_bg}');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }}

    /* Main Container for Clarity */
    .main-box {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }}

    /* Massive Professional Header */
    .hero-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(40px, 8vw, 100px);
        text-align: center;
        background: linear-gradient(135deg, #1DB954 0%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -5px;
        margin-bottom: 0px;
    }}

    .hero-subtitle {{
        font-family: 'Inter', sans-serif;
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        opacity: 0.5;
        margin-bottom: 40px;
    }}

    /* Input Fields Styling - High Contrast */
    label {{
        font-weight: 700 !important;
        color: #1DB954 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        height: 55px !important;
        font-size: 1.1rem !important;
    }}

    /* Elite Result Cards */
    .track-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
        transition: 0.3s ease;
    }}
    .track-card:hover {{
        background: rgba(255, 255, 255, 0.08);
        border-color: #1DB954;
        transform: translateY(-3px);
    }}

    /* Glowing Action Button */
    .stButton>button {{
        background: #1DB954 !important;
        color: black !important;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 15px !important;
        padding: 20px !important;
        font-size: 1.2rem !important;
        border: none !important;
        transition: 0.3s;
        box-shadow: 0 10px 30px rgba(29, 185, 84, 0.2);
    }}
    .stButton>button:hover {{
        box-shadow: 0 10px 40px rgba(29, 185, 84, 0.4);
        transform: scale(1.01);
    }}
</style>
""", unsafe_allow_html=True)

# --- SECURE SPOTIFY CONNECT ---
@st.cache_resource(show_spinner=False)
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_sp()

# --- INTERFACE LAYOUT ---
st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">World Class AI Soundtrack Curator</div>', unsafe_allow_html=True)

# History Sidebar
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954; letter-spacing:2px;'>ARCHIVE</h2>", unsafe_allow_html=True)
    if not st.session_state.playlist_history:
        st.write("No vibes stored yet.")
    for i, entry in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"🎵 {entry['genre']} - {entry['vibe']}", key=f"h_{i}"):
            st.session_state.current_tracks = entry['tracks']

# Input Section with Container
st.markdown('<div class="main-box">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    u_name = st.text_input("NAME", placeholder="Enter your name...")
with c2:
    u_genre = st.selectbox("GENRE", ["Techno", "Pop", "Rock", "Israeli", "Hip Hop", "Deep House", "Indie"])
with c3:
    u_vibe = st.selectbox("VIBE", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Morning Vibes"])

if st.button("CREATE MY EXPERIENCE ⚡"):
    if not sp:
        st.error("Protocol Error: Check Spotify Credentials.")
    elif not u_name:
        st.warning("Identity Required: Please enter a name.")
    else:
        with st.spinner('Accessing Global Servers...'):
            try:
                # Up-to-the-minute freshness
                year = datetime.now().year
                results = sp.search(q=f"genre:{u_genre} {u_vibe} year:{year-1}-{year}", limit=12, type='track')
                
                if not results['tracks']['items']: # Fallback
                    results = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=12, type='track')
                
                st.session_state.current_tracks = results['tracks']['items']
                st.session_state.playlist_history.append({'genre': u_genre, 'vibe': u_vibe, 'tracks': results['tracks']['items']})
                st.balloons()
            except Exception:
                st.error("Spotify is busy. Please wait 30 seconds and try again.")
st.markdown('</div>', unsafe_allow_html=True)

# Results Display
if st.session_state.current_tracks:
    st.markdown(f"<br><h3 style='letter-spacing:2px;'>CURATED FOR {u_name.upper()}:</h3>", unsafe_allow_html=True)
    
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:25px;">
                <img src="{track['album']['images'][0]['url']}" width="100" style="border-radius:15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="flex-grow:1;">
                    <div style="color:#1DB954; font-weight:800; font-size:0.8rem; letter-spacing:1px;">{track['artists'][0]['name'].upper()}</div>
                    <div style="font-size:1.6rem; font-weight:900; letter-spacing:-1px;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold; font-size:0.9rem;">OPEN ON SPOTIFY →</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if track.get('preview_url'):
            st.audio(track['preview_url'])
