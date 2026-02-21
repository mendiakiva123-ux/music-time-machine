import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# --- 1. SETTINGS & PERFORMANCE ---
st.set_page_config(page_title="VibeLab Elite", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# Initialize Session States
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []
if 'last_bg_time' not in st.session_state:
    st.session_state.last_bg_time = time.time()
if 'bg_url' not in st.session_state:
    # Ultra-HD 4K Music & Party Backgrounds
    bgs = [
        "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=3840", # Concert 4K
        "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=3840", # Party 4K
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=3840", # DJ Gear 4K
        "https://images.unsplash.com/photo-1459749411177-042180ce673c?q=80&w=3840"  # Crowd 4K
    ]
    st.session_state.bg_url = random.choice(bgs)

# Dynamic Background Logic (Every 60 Seconds)
if time.time() - st.session_state.last_bg_time > 60:
    st.session_state.bg_url = random.choice([b for b in bgs if b != st.session_state.bg_url])
    st.session_state.last_bg_time = time.time()

# --- 2. THE ULTIMATE VISUAL INTERFACE (CSS) ---
st.markdown(f"""
<style>
    /* Full Page 4K Background with Overlay */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)), url('{st.session_state.bg_url}');
        background-size: cover;
        background-attachment: fixed;
        transition: background 2s ease-in-out;
    }}

    /* Title Styling - Impossible to miss */
    .mega-title {{
        font-family: 'Arial Black', sans-serif;
        font-size: 100px;
        text-align: center;
        background: linear-gradient(to bottom, #1DB954, #1ed760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 0px;
        letter-spacing: -5px;
    }}

    /* Text Shield - Fixes the "squashed/invisible" text bug */
    .glass-card {{
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(15px);
        padding: 35px;
        border-radius: 25px;
        border: 2px solid #1DB954;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        margin: 20px 0;
    }}

    /* Input Labels */
    label {{
        color: #1DB954 !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        margin-bottom: 10px !important;
    }}

    /* Song Result Cards */
    .song-box {{
        background: rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
        transition: 0.3s;
    }}
    .song-box:hover {{
        background: rgba(29, 185, 84, 0.15);
        transform: translateY(-5px);
        border-color: #1DB954;
    }}

    /* Hidden Sidebar Hint */
    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.95);
        border-right: 2px solid #1DB954;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. SPOTIFY ENGINE (Zero-Crash) ---
@st.cache_resource
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_sp()

# --- 4. SIDEBAR (HIDDEN BY DEFAULT) ---
with st.sidebar:
    st.markdown("<h1 style='color:#1DB954;'>HISTORY</h1>", unsafe_allow_html=True)
    if not st.session_state.playlist_history:
        st.info("No playlists yet. Create one!")
    for i, h in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"Session {len(st.session_state.playlist_history)-i}: {h['genre']}", key=f"hist_{i}"):
            st.session_state.current_tracks = h['tracks']

# --- 5. MAIN CONTENT ---
st.markdown('<h1 class="mega-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; font-size:1.5rem; font-weight:bold;'>4K AI Music Experience</p>", unsafe_allow_html=True)

# Input Section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    name = st.text_input("Name", placeholder="Who are you?")
with c2:
    genre = st.selectbox("Genre", ["Techno", "Pop", "Rock", "Israeli Hits", "Hip Hop", "Deep House"])
with c3:
    vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Morning Vibes"])

if st.button("GENERATE MY VIBE 🚀"):
    if not sp:
        st.error("Spotify Connection Error. Check your secrets.")
    elif not name:
        st.warning("Please enter your name.")
    else:
        with st.spinner('Curating your 4K Soundtrack...'):
            try:
                results = sp.search(q=f"genre:{genre} {vibe}", limit=12, type='track')
                if results['tracks']['items']:
                    st.session_state.current_tracks = results['tracks']['items']
                    st.session_state.playlist_history.append({'genre': genre, 'tracks': results['tracks']['items']})
                    st.balloons()
            except:
                st.error("Spotify API Limit reached. Try again in 30s.")
st.markdown('</div>', unsafe_allow_html=True)

# Results Area
if st.session_state.current_tracks:
    st.markdown(f"<h2 style='color:white;'>✨ Curated for {name}:</h2>", unsafe_allow_html=True)
    
    # Display in a nice grid
    cols = st.columns(2)
    for idx, track in enumerate(st.session_state.current_tracks):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="song-box">
                <div style="display:flex; align-items:center; gap:20px;">
                    <img src="{track['album']['images'][0]['url']}" width="90" style="border-radius:15px; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                    <div style="flex-grow:1;">
                        <div style="color:#1DB954; font-weight:bold; font-size:0.9rem;">{track['artists'][0]['name'].upper()}</div>
                        <div style="font-size:1.5rem; font-weight:bold; color:white; line-height:1.2;">{track['name']}</div>
                        <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">OPEN IN SPOTIFY →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if track.get('preview_url'):
                st.audio(track['preview_url'])
