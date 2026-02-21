import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# --- 1. PRO CONFIGURATION ---
st.set_page_config(page_title="VibeLab | Neo-Experience", page_icon="🔥", layout="wide")

# Persistent memory to prevent crashes
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []
if 'bg_seed' not in st.session_state:
    st.session_state.bg_seed = random.randint(1, 100)

# Professional Neon Backgrounds
BGS = [
    "https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=1920", # Neon Abstract
    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=1920", # Cyberpunk Tech
    "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=1920", # Music Studio
    "https://images.unsplash.com/photo-1459749411177-042180ce673c?q=80&w=1920"  # Concert Crowd
]
current_bg = BGS[st.session_state.bg_seed % len(BGS)]

# --- 2. HIGH-END VISUALS (CSS) ---
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap" rel="stylesheet">
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.85)), url('{current_bg}');
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Neon Title */
    .hero-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(40px, 10vw, 120px);
        text-align: center;
        color: #fff;
        text-shadow: 0 0 10px #1DB954, 0 0 20px #1DB954, 0 0 40px #1DB954;
        margin-bottom: 0;
        letter-spacing: 10px;
    }}

    .hero-subtitle {{
        font-family: 'Inter', sans-serif;
        text-align: center;
        font-size: 1rem;
        letter-spacing: 5px;
        color: #1DB954;
        text-transform: uppercase;
        margin-bottom: 50px;
    }}

    /* Glass Container */
    .glass-box {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}

    /* Modern Inputs */
    label {{
        color: #fff !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }}
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: rgba(0,0,0,0.5) !important;
        color: #1DB954 !important;
        border: 1px solid #1DB954 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }}

    /* Track Cards - Neon Style */
    .track-card {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(29, 185, 84, 0.2);
        transition: 0.3s;
    }}
    .track-card:hover {{
        border-color: #1DB954;
        box-shadow: 0 0 20px rgba(29, 185, 84, 0.3);
        transform: scale(1.01);
    }}

    /* Ultimate Button */
    .stButton>button {{
        background: linear-gradient(90deg, #1DB954, #19e68c) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 50px !important;
        padding: 20px !important;
        font-size: 1.4rem !important;
        text-transform: uppercase;
        border: none !important;
        box-shadow: 0 10px 30px rgba(29, 185, 84, 0.4) !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. FAIL-SAFE SPOTIFY ENGINE ---
@st.cache_resource(show_spinner=False)
def get_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_spotify()

# --- 4. THE INTERFACE ---
st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">The Future of Sound</div>', unsafe_allow_html=True)

# Main Glass Box
st.markdown('<div class="glass-box">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    u_name = st.text_input("NAME", placeholder="Identify yourself...")
with c2:
    u_genre = st.selectbox("GENRE", ["Techno", "Hip Hop", "Indie", "Israeli Hits", "Rock", "Pop", "Deep House"])
with c3:
    u_vibe = st.selectbox("VIBE", ["Late Night", "Gym Flow", "Deep Chill", "Party Mode", "Work Focus"])

if st.button("LAUNCH EXPERIENCE ⚡"):
    if not sp:
        st.error("SYSTEM ERROR: Spotify Bridge Offline.")
    elif not u_name:
        st.warning("PROTOCOL ERROR: Identity Required.")
    else:
        with st.spinner('Syncing with Global Audio Hub...'):
            try:
                # Anti-Bug: Small delay to respect Spotify API
                time.sleep(0.3)
                results = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=12, type='track')
                
                if results and results['tracks']['items']:
                    st.session_state.current_tracks = results['tracks']['items']
                    st.session_state.playlist_history.append({'genre': u_genre, 'vibe': u_vibe, 'tracks': results['tracks']['items']})
                    st.session_state.bg_seed += 1 # Change BG on success
                    st.balloons()
            except:
                st.error("CONNECTION BUSY: Retrying in 5 seconds...")

st.markdown('</div>', unsafe_allow_html=True)

# --- 5. NEON RESULTS ---
if st.session_state.current_tracks:
    st.markdown(f"<br><h2 style='color:#1DB954; font-family:Orbitron;'>CURATED FOR {u_name.upper()}</h2>", unsafe_allow_html=True)
    
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:30px;">
                <img src="{track['album']['images'][0]['url']}" width="110" style="border-radius:15px; box-shadow: 0 0 15px rgba(29,185,84,0.4);">
                <div style="flex-grow:1;">
                    <div style="color:#1DB954; font-weight:800; font-size:0.8rem; letter-spacing:2px;">{track['artists'][0]['name'].upper()}</div>
                    <div style="font-size:1.8rem; font-weight:900; color:#fff;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="background:#1DB954; color:#000; padding:10px 25px; border-radius:50px; text-decoration:none; font-weight:900; font-size:12px; display:inline-block; margin-top:10px;">PLAY ON SPOTIFY</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if track.get('preview_url'):
            st.audio(track['preview_url'])

# Sidebar History
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954; font-family:Orbitron;'>HISTORY</h2>", unsafe_allow_html=True)
    for i, entry in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"● {entry['genre']} | {entry['vibe']}", key=f"hist_{i}"):
            st.session_state.current_tracks = entry['tracks']
