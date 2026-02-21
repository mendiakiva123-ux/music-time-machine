import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time
from datetime import datetime

# --- 1. CORE ENGINE & STABILITY ---
st.set_page_config(page_title="VibeLab Ultra | AI Soundtrack", page_icon="💎", layout="wide")

# Persistent memory to block Spotify "Rate Limit" errors
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []
if 'bg_index' not in st.session_state:
    st.session_state.bg_index = random.randint(0, 3)

# Professional background assets
BGS = [
    "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=1920",
    "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920",
    "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920",
    "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1920"
]

# --- 2. LUXURY UI FRAMEWORK (The "Clarity" Fix) ---
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
    /* Prevent text being swallowed by background */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url('{BGS[st.session_state.bg_index]}');
        background-size: cover;
        background-attachment: fixed;
    }}

    /* The "Glass Capsule" - Fixes visibility */
    .glass-container {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 20px 0;
    }}

    .hero-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(50px, 10vw, 110px);
        text-align: center;
        background: linear-gradient(to right, #1DB954, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -6px;
        margin-bottom: 0;
    }}

    .hero-subtitle {{
        text-align: center;
        font-size: 1rem;
        letter-spacing: 7px;
        opacity: 0.6;
        text-transform: uppercase;
        margin-bottom: 30px;
    }}

    /* High-Contrast Inputs */
    label {{
        color: #1DB954 !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.9rem !important;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: white !important;
        color: black !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 55px !important;
    }}

    /* Result Cards */
    .track-card {{
        background: rgba(255, 255, 255, 0.07);
        padding: 25px;
        border-radius: 20px;
        border-left: 5px solid #1DB954;
        margin-bottom: 15px;
        transition: 0.3s;
    }}
    .track-card:hover {{
        background: rgba(255, 255, 255, 0.12);
        transform: translateX(10px);
    }}

    /* High-Performance Button */
    .stButton>button {{
        background: #1DB954 !important;
        color: black !important;
        font-weight: 900 !important;
        border-radius: 50px !important;
        padding: 20px !important;
        font-size: 1.3rem !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(29, 185, 84, 0.3);
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. THE "ANTI-BUG" SPOTIFY ENGINE ---
@st.cache_resource(show_spinner=False)
def connect_to_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = connect_to_spotify()

# --- 4. APP LAYOUT ---
st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Premium AI Soundtrack Experience</div>', unsafe_allow_html=True)

# Sidebar with better contrast
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>HISTORY</h2>", unsafe_allow_html=True)
    for i, item in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"⚡ {item['genre']} | {item['vibe']}", key=f"hist_{i}"):
            st.session_state.current_tracks = item['tracks']

# Interactive Controls
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    name = st.text_input("YOUR NAME", placeholder="Guest")
with c2:
    genre = st.selectbox("GENRE", ["Techno", "Pop", "Rock", "Israeli", "Hip Hop", "Jazz", "Metal"])
with c3:
    vibe = st.selectbox("VIBE", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Focus"])

if st.button("INITIATE EXPERIENCE ⚡"):
    if not sp:
        st.error("Connection Error: Please check your Spotify Secrets.")
    elif not name:
        st.warning("Identification required: Please enter your name.")
    else:
        with st.spinner('Syncing with Spotify Global Hub...'):
            try:
                # Optimized search for 2025/2026 freshness
                current_year = datetime.now().year
                results = sp.search(q=f"genre:{genre} {vibe} year:{current_year-1}-{current_year}", limit=10, type='track')
                
                # Fallback for niche genres
                if not results['tracks']['items']:
                    results = sp.search(q=f"genre:{genre} {vibe}", limit=10, type='track')
                
                st.session_state.current_tracks = results['tracks']['items']
                st.session_state.playlist_history.append({'genre': genre, 'vibe': vibe, 'tracks': results['tracks']['items']})
                st.balloons()
            except:
                st.error("Rate Limit Hit. Please wait 15 seconds for cooling.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ELITE RESULTS DISPLAY ---
if st.session_state.current_tracks:
    st.markdown(f"### ✨ Curated for {name.upper()}:")
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:25px;">
                <img src="{track['album']['images'][0]['url']}" width="90" style="border-radius:12px;">
                <div style="flex-grow:1;">
                    <div style="color:#1DB954; font-weight:800; font-size:0.8rem; letter-spacing:1px;">{track['artists'][0]['name'].upper()}</div>
                    <div style="font-size:1.5rem; font-weight:900;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; font-weight:bold; text-decoration:none;">LISTEN ON SPOTIFY →</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if track.get('preview_url'):
            st.audio(track['preview_url'])
