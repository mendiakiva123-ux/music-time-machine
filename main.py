import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time
from datetime import datetime

# --- ELITE CONFIGURATION ---
st.set_page_config(page_title="VibeLab Elite | AI Audio Experience", page_icon="💎", layout="wide")

# Persistent State Management
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []
if 'last_bg_change' not in st.session_state:
    st.session_state.last_bg_change = time.time()
if 'current_bg' not in st.session_state:
    st.session_state.current_bg = "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920"

# Background Rotation (Every 60 Seconds)
if time.time() - st.session_state.last_bg_change > 60:
    bgs = [
        "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=1920",
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920",
        "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1920",
        "https://images.unsplash.com/photo-1516280440614-37939bbacd81?q=80&w=1920"
    ]
    st.session_state.current_bg = random.choice(bgs)
    st.session_state.last_bg_change = time.time()

# --- DYNAMIC THEME LOGIC ---
vibe_colors = {
    "Party Mode": "#FF007A",
    "Gym Flow": "#FF4B2B",
    "Late Night": "#8A2BE2",
    "Deep Chill": "#00D2FF",
    "Focus": "#1DB954",
    "Morning Energy": "#FFD700"
}

# --- ADVANCED ELITE UI (CSS) ---
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.92)), url('{st.session_state.current_bg}');
        background-size: cover;
        background-attachment: fixed;
        transition: all 1s ease-in-out;
    }}
    
    .hero-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(50px, 12vw, 140px);
        text-align: center;
        background: linear-gradient(to right, #ffffff, #1DB954, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -8px;
        line-height: 0.8;
        margin-bottom: 10px;
    }}

    .hero-subtitle {{
        font-family: 'Inter', sans-serif;
        text-align: center;
        font-size: 1rem;
        letter-spacing: 8px;
        text-transform: uppercase;
        opacity: 0.6;
        margin-bottom: 50px;
    }}

    /* ELITE INPUT FIELDS */
    label {{
        color: white !important;
        font-size: 0.9rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px !important;
        opacity: 0.9;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 15px !important;
        height: 60px !important;
        font-size: 1.1rem !important;
        backdrop-filter: blur(10px);
    }}

    /* DYNAMIC CARDS */
    .track-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        padding: 25px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .track-card:hover {{
        transform: scale(1.02);
        background: rgba(255, 255, 255, 0.07);
        border-color: #1DB954;
    }}

    /* PRO BUTTON */
    .stButton>button {{
        background: white !important;
        color: black !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        padding: 25px !important;
        font-size: 1.2rem !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        width: 100%;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: #1DB954 !important;
        box-shadow: 0 0 40px rgba(29, 185, 84, 0.5);
    }}

    /* SIDEBAR CUSTOMIZATION */
    [data-testid="stSidebar"] {{
        background-color: rgba(0, 0, 0, 0.8);
        border-right: 1px solid rgba(255,255,255,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# --- SECURE API BRIDGE ---
@st.cache_resource(show_spinner=False)
def init_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = init_spotify()

# --- MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Premium AI Audio Curator</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='letter-spacing:2px;'>ARCHIVE</h2>", unsafe_allow_html=True)
    for i, entry in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"● {entry['genre']} - {entry['vibe']}", key=f"h_{i}"):
            st.session_state.current_tracks = entry['tracks']

# ELITE INPUT AREA
col1, col2, col3 = st.columns(3)
with col1:
    u_name = st.text_input("IDENTIFIER", placeholder="Guest Name")
with col2:
    u_genre = st.selectbox("GENRE SELECTION", ["Techno", "Pop", "Rock", "Israeli Hits", "Hip Hop", "Deep House", "Jazz", "Metal"])
with col3:
    u_vibe = st.selectbox("CURRENT VIBE", list(vibe_colors.keys()))

if st.button("INITIATE CURATION ⚡"):
    if sp and u_name:
        with st.spinner('Accessing Global Databases...'):
            try:
                # Up-to-date music logic (Current Year Search)
                current_year = datetime.now().year
                query = f"genre:{u_genre} {u_vibe} year:{current_year-1}-{current_year}"
                results = sp.search(q=query, limit=12, type='track')
                
                if results and results['tracks']['items']:
                    st.session_state.current_tracks = results['tracks']['items']
                    st.session_state.playlist_history.append({'genre': u_genre, 'vibe': u_vibe, 'tracks': results['tracks']['items']})
                    st.balloons()
                else:
                    st.warning("No fresh hits found. Expanding search to all-time classics...")
                    results = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=12, type='track')
                    st.session_state.current_tracks = results['tracks']['items']
            except:
                st.error("Protocol Error. API Limit reached.")

# RESULTS DISPLAY
if st.session_state.current_tracks:
    v_color = vibe_colors.get(u_vibe, "#1DB954")
    st.markdown(f"<h3 style='color:{v_color};'>Selected for {u_name}:</h3>", unsafe_allow_html=True)
    
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:30px;">
                <img src="{track['album']['images'][0]['url']}" width="120" style="border-radius:20px; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));">
                <div style="flex-grow:1;">
                    <div style="color:{v_color}; font-weight:800; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">{track['artists'][0]['name']}</div>
                    <div style="font-size:1.8rem; font-weight:900; margin-bottom:15px; letter-spacing:-1px;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="background:{v_color}; color:white; padding:12px 30px; border-radius:50px; text-decoration:none; font-weight:900; font-size:13px;">STREAM NOW</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if track.get('preview_url'):
            st.audio(track['preview_url'])
