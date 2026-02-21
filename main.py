import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# --- 1. PRO CONFIG & SILENT SIDEBAR ---
st.set_page_config(
    page_title="VibeLab Master 4K", 
    page_icon="👑", 
    layout="wide", 
    initial_sidebar_state="collapsed" # הסתרת ההיסטוריה כברירת מחדל
)

# Initialize Session Memory
if 'history' not in st.session_state: st.session_state.history = []
if 'tracks' not in st.session_state: st.session_state.tracks = []
if 'bg_url' not in st.session_state:
    # Ultra-HD 4K Vibrant Backgrounds
    bgs = [
        "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=3840",
        "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=3840",
        "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=3840",
        "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?q=80&w=3840"
    ]
    st.session_state.bg_url = random.choice(bgs)

# --- 2. MASTER UI DESIGN (CSS) ---
st.markdown(f"""
<style>
    /* Full Page 4K Background */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), url('{st.session_state.bg_url}');
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Neon Title with Shadow - No more "Squashed" text */
    .master-title {{
        font-family: 'Arial Black', sans-serif;
        font-size: clamp(50px, 8vw, 120px);
        text-align: center;
        color: #1DB954;
        text-shadow: 4px 4px 20px rgba(0,0,0,0.9), 0 0 30px #1DB954;
        margin-bottom: 10px;
        letter-spacing: -2px;
    }}

    /* Main Content Shield */
    .glass-container {{
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 30px;
        border: 2px solid #1DB954;
        margin-top: 20px;
    }}

    /* Clear Inputs */
    label {{
        color: #1DB954 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        text-shadow: 2px 2px 4px black;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: white !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        height: 55px !important;
    }}

    /* Professional Track Cards */
    .track-card {{
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        border-left: 8px solid #1DB954;
        transition: 0.3s;
    }}
    .track-card:hover {{
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.02);
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.9);
        border-right: 2px solid #1DB954;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. FAIL-SAFE ENGINE ---
@st.cache_resource
def get_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_spotify()

# --- 4. SIDEBAR (HIDDEN BY DEFAULT) ---
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>ARCHIVE</h2>", unsafe_allow_html=True)
    if not st.session_state.history:
        st.write("No sessions stored.")
    for i, session in enumerate(reversed(st.session_state.history)):
        if st.button(f"Session {len(st.session_state.history)-i}: {session['genre']}", key=f"s_{i}"):
            st.session_state.tracks = session['tracks']

# --- 5. MAIN PAGE ---
st.markdown('<h1 class="master-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; font-size:1.2rem;'>ULTRA 4K AI AUDIO EXPERIENCE</p>", unsafe_allow_html=True)

# Central Dashboard
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    u_name = st.text_input("Name", value="Guest")
with c2:
    u_genre = st.selectbox("Genre", ["Techno", "Hip Hop", "Pop", "Rock", "Israeli", "Deep House"])
with c3:
    u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Focus", "Deep Chill"])

if st.button("CREATE THE EXPERIENCE ⚡"):
    if not sp:
        st.error("Connection lost.")
    else:
        with st.spinner('Accessing Global Satellite Servers...'):
            try:
                # Anti-Limit Strategy: Search with retry
                time.sleep(0.5)
                results = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=12, type='track')
                
                if results['tracks']['items']:
                    st.session_state.tracks = results['tracks']['items']
                    st.session_state.history.append({'genre': u_genre, 'tracks': results['tracks']['items']})
                    st.balloons()
            except:
                st.warning("Spotify is slightly busy. Showing previous results or try again in 10s.")

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. DISPLAY ---
if st.session_state.tracks:
    st.markdown(f"<br><h3 style='color:white;'>SELECTED FOR {u_name.upper()}:</h3>", unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, track in enumerate(st.session_state.tracks):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="track-card">
                <div style="display:flex; align-items:center; gap:20px;">
                    <img src="{track['album']['images'][0]['url']}" width="100" style="border-radius:15px; box-shadow: 0 10px 20px rgba(0,0,0,0.5);">
                    <div style="flex-grow:1;">
                        <div style="color:#1DB954; font-weight:bold; font-size:0.8rem;">{track['artists'][0]['name'].upper()}</div>
                        <div style="font-size:1.6rem; font-weight:900; color:white;">{track['name']}</div>
                        <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; font-weight:bold; text-decoration:none;">LISTEN ON SPOTIFY →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if track.get('preview_url'):
                st.audio(track['preview_url'])
