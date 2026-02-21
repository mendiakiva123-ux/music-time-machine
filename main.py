import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# --- CONFIGURATION & STABILITY ---
st.set_page_config(page_title="VibeLab | Global AI Soundtrack", page_icon="🎧", layout="wide")

# Persistent Session State (Prevents API Overload)
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []
if 'last_bg_change' not in st.session_state:
    st.session_state.last_bg_change = time.time()
if 'current_bg' not in st.session_state:
    # High-quality professional music backgrounds
    bg_list = [
        "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=1920",
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920",
        "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920",
        "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1920"
    ]
    st.session_state.current_bg = random.choice(bg_list)

# Background Logic: Change only if 60 seconds passed
if time.time() - st.session_state.last_bg_change > 60:
    bg_list = [
        "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=1920",
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920",
        "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920",
        "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1920"
    ]
    st.session_state.current_bg = random.choice(bg_list)
    st.session_state.last_bg_change = time.time()

# --- PROFESSIONAL UI (CSS) ---
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), url('{st.session_state.current_bg}');
        background-size: cover;
        background-attachment: fixed;
        transition: background 1s ease-in-out;
    }}
    .hero-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(60px, 10vw, 120px);
        text-align: center;
        background: linear-gradient(to right, #1DB954, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -5px;
        margin-bottom: 0;
    }}
    .hero-subtitle {{
        text-align: center;
        font-size: 1.2rem;
        letter-spacing: 5px;
        opacity: 0.8;
        text-transform: uppercase;
        margin-bottom: 40px;
    }}
    label {{
        font-weight: 900 !important;
        color: #1DB954 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: white !important;
        color: black !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: 2px solid #1DB954 !important;
    }}
    .track-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
        transition: 0.3s ease;
    }}
    .track-card:hover {{
        transform: translateY(-5px);
        border-color: #1DB954;
        background: rgba(255, 255, 255, 0.1);
    }}
    .stButton>button {{
        background: #1DB954 !important;
        color: black !important;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 50px !important;
        padding: 20px !important;
        font-size: 1.4rem !important;
        border: none !important;
        text-transform: uppercase;
    }}
</style>
""", unsafe_allow_html=True)

# --- SPOTIFY CONNECTION (The "Anti-Bug" Method) ---
@st.cache_resource(show_spinner=False)
def get_spotify_instance():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=csec)
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        return None

sp = get_spotify_instance()

# --- MAIN INTERFACE ---
st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Elevating Human Emotion through AI</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>HISTORY</h2>", unsafe_allow_html=True)
    if not st.session_state.playlist_history:
        st.write("Your history is empty.")
    for i, entry in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"🎵 {entry['genre']} - {entry['vibe']}", key=f"hist_{i}"):
            st.session_state.current_tracks = entry['tracks']

# Inputs
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("YOUR NAME", placeholder="Type here...")
with col2:
    genre = st.selectbox("GENRE", ["Techno", "Rock", "Pop", "Israeli", "Hip Hop", "Jazz", "Metal", "Lo-fi"])
with col3:
    vibe = st.selectbox("YOUR CURRENT VIBE", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Focus", "Morning Vibes"])

if st.button("GENERATE MY EXPERIENCE ⚡"):
    if not sp:
        st.error("Spotify Connection Error. Check your Secrets.")
    elif not name:
        st.warning("Please enter your name first.")
    else:
        with st.spinner('Scanning Spotify database...'):
            try:
                # Add a tiny delay to avoid hitting the rate limit
                time.sleep(0.5)
                query = f"genre:{genre} {vibe}"
                results = sp.search(q=query, limit=10, type='track')
                
                if results and results['tracks']['items']:
                    st.session_state.current_tracks = results['tracks']['items']
                    st.session_state.playlist_history.append({'genre': genre, 'vibe': vibe, 'tracks': results['tracks']['items']})
                    st.balloons()
                else:
                    st.warning("No tracks found for this specific combo.")
            except Exception as e:
                st.error("API Limit reached. Please wait 30 seconds and try again.")

# Results
if st.session_state.current_tracks:
    st.markdown(f"### ✨ Curated for {name}:")
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:25px;">
                <img src="{track['album']['images'][0]['url']}" width="100" style="border-radius:12px;">
                <div style="flex-grow:1;">
                    <div style="color:#1DB954; font-weight:800; font-size:0.9rem;">{track['artists'][0]['name'].upper()}</div>
                    <div style="font-size:1.6rem; font-weight:900;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">OPEN IN SPOTIFY →</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if track.get('preview_url'):
            st.audio(track['preview_url'])
