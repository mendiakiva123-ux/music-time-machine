import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# --- 1. CONFIG & PERSISTENCE ---
st.set_page_config(page_title="VibeLab | Ultra Clarity", page_icon="🎵", layout="wide")

if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []
if 'bg_img' not in st.session_state:
    # High-end, dark professional backgrounds
    bgs = [
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920",
        "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=1920",
        "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920"
    ]
    st.session_state.bg_img = random.choice(bgs)

# --- 2. THE CLARITY DESIGN (CSS) ---
st.markdown(f"""
<style>
    /* Dark overlay to make everything pop */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('{st.session_state.bg_img}');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }}

    /* Title Styling */
    .main-title {{
        font-family: 'Arial Black', sans-serif;
        font-size: 80px;
        text-align: center;
        color: #1DB954;
        margin-bottom: 0px;
        text-transform: uppercase;
    }}

    /* MAKING TEXT CLEAR: High contrast inputs */
    label {{
        color: #1DB954 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 4px black;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: white !important;
        color: black !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        border: 3px solid #1DB954 !important;
        border-radius: 10px !important;
    }}

    /* Result Cards */
    .song-card {{
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #1DB954;
        margin-bottom: 15px;
    }}

    /* Big Green Button */
    .stButton>button {{
        background-color: #1DB954 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.5rem !important;
        width: 100%;
        border-radius: 10px !important;
        height: 70px !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. SPOTIFY ENGINE (Anti-Error) ---
@st.cache_resource
def connect_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except Exception as e:
        st.error(f"Spotify Key Error: {e}")
        return None

sp = connect_spotify()

# --- 4. UI LAYOUT ---
st.markdown('<h1 class="main-title">VIBELAB</h1>', unsafe_allow_html=True)
st.write("<p style='text-align:center; font-size:1.2rem;'>Premium AI Music Curation</p>", unsafe_allow_html=True)

# Inputs
col1, col2, col3 = st.columns(3)
with col1:
    name = st.text_input("Name", placeholder="Enter your name...")
with col2:
    genre = st.selectbox("Genre", ["Pop", "Rock", "Techno", "Hip Hop", "Israeli", "Jazz"])
with col3:
    vibe = st.selectbox("Current Vibe", ["Party", "Chill", "Focus", "Gym", "Late Night"])

if st.button("GET MY MUSIC ⚡"):
    if not sp:
        st.error("Connection failed. Check your Secrets.")
    elif not name:
        st.warning("Please enter your name.")
    else:
        with st.spinner('Loading hits...'):
            try:
                # Optimized search
                results = sp.search(q=f"genre:{genre} {vibe}", limit=10, type='track')
                if results['tracks']['items']:
                    st.session_state.current_tracks = results['tracks']['items']
                    st.session_state.playlist_history.append({'name': name, 'tracks': results['tracks']['items']})
                    st.balloons()
            except Exception as e:
                st.error("Spotify is busy. Try again in 10 seconds.")

# --- 5. RESULTS ---
if st.session_state.current_tracks:
    st.markdown(f"### ✨ Curated for {name}:")
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="song-card">
            <div style="display:flex; align-items:center; gap:20px;">
                <img src="{track['album']['images'][0]['url']}" width="80" style="border-radius:10px;">
                <div>
                    <div style="color:#1DB954; font-weight:bold;">{track['artists'][0]['name']}</div>
                    <div style="font-size:1.4rem; font-weight:bold;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="color:white;">▶ Listen on Spotify</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if track.get('preview_url'):
            st.audio(track['preview_url'])

# Sidebar History
with st.sidebar:
    st.title("History")
    for i, h in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"Session {i+1}", key=f"h_{i}"):
            st.session_state.current_tracks = h['tracks']
