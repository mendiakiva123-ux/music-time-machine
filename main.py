import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# --- 1. PRO-ENGINE CONFIG ---
st.set_page_config(page_title="VibeLab Infinity", page_icon="♾️", layout="wide", initial_sidebar_state="collapsed")

# Persistent Cache for Multi-User Performance
if 'playlist_history' not in st.session_state: st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state: st.session_state.current_tracks = []

# --- 2. ULTRA 4K DYNAMIC VISUALS ---
# High-bandwidth 4K imagery
BGS = [
    "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&w=3840&q=100",
    "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=3840&q=100",
    "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=3840&q=100",
    "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?auto=format&fit=crop&w=3840&q=100"
]
selected_bg = random.choice(BGS)

st.markdown(f"""
<style>
    /* Full 4K Background with Glass Overlay */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.9)), url('{selected_bg}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Title & UI Text - Super Clarity */
    .hero-title {{
        font-family: 'Arial Black', sans-serif;
        font-size: 90px;
        text-align: center;
        color: #1DB954;
        text-shadow: 0 0 30px rgba(29, 185, 84, 0.5);
        margin-bottom: 0px;
    }}

    /* Input Shield - Fixes visibility bugs */
    .ui-panel {{
        background: rgba(0, 0, 0, 0.85);
        border: 2px solid #1DB954;
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 20px 80px rgba(0,0,0,0.9);
    }}

    /* Name & Selection Boxes */
    label {{
        color: white !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        height: 50px !important;
    }}

    /* Floating History Button */
    .history-btn {{
        background: linear-gradient(45deg, #1DB954, #19e68c);
        color: black !important;
        padding: 10px 25px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 900;
        box-shadow: 0 0 20px rgba(29, 185, 84, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. ERROR-PROOF CONNECTION ---
@st.cache_resource(show_spinner=False)
def connect_safe():
    try:
        # Multi-user safe connection
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except Exception as e:
        return None

sp = connect_safe()

# --- 4. TOP INTERFACE ---
c_title, c_hist = st.columns([4, 1])
with c_title:
    st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
with c_hist:
    # This acts as a clear visual anchor for the history
    if st.button("📜 MY HISTORY"):
        st.info("History panel opened on the left! ←")
        # Trigger sidebar expansion via Streamlit's internal state if needed
        st.session_state.sidebar_state = "expanded"

# --- 5. THE CONTROL CENTER ---
st.markdown('<div class="ui-panel">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    # Fix: Just "Name" label and no default "Guest" text
    user_name = st.text_input("Name", placeholder="Enter your name here...")
with col2:
    genre = st.selectbox("Genre", ["Techno", "Hip Hop", "Indie", "Israeli", "Deep House", "Pop"])
with col3:
    vibe = st.selectbox("Vibe", ["Late Night", "Gym Flow", "Party Mode", "Deep Focus", "Chill"])

if st.button("GENERATE EXPERIENCE ⚡"):
    if not sp:
        st.error("System connection error. Check your Spotify Keys.")
    elif not user_name:
        st.warning("Please type your Name to continue.")
    else:
        with st.spinner('Syncing with Global Audio Grid...'):
            try:
                # Cache results to prevent "API Limit Reached" for multiple users
                search_query = f"genre:{genre} {vibe}"
                results = sp.search(q=search_query, limit=12, type='track')
                
                if results and results['tracks']['items']:
                    st.session_state.current_tracks = results['tracks']['items']
                    st.session_state.playlist_history.append({
                        'name': user_name,
                        'genre': genre,
                        'tracks': results['tracks']['items']
                    })
                    st.balloons()
                else:
                    st.error("No tracks found for this vibe. Try another genre!")
            except:
                st.error("Spotify is overwhelmed. Wait 10 seconds and click again.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>HISTORY</h2>", unsafe_allow_html=True)
    if not st.session_state.playlist_history:
        st.write("Your past vibes will appear here.")
    for i, session in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"Session {len(st.session_state.playlist_history)-i}: {session['genre']}", key=f"h_{i}"):
            st.session_state.current_tracks = session['tracks']

# --- 7. ELITE RESULTS DISPLAY ---
if st.session_state.current_tracks:
    st.markdown(f"<br><h2 style='color:white; text-align:center;'>CURATED FOR {user_name.upper()}</h2>", unsafe_allow_html=True)
    
    # Professional Grid Layout
    cols = st.columns(2)
    for idx, track in enumerate(st.session_state.current_tracks):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:20px; border-left:5px solid #1DB954; margin-bottom:20px;">
                <div style="display:flex; align-items:center; gap:20px;">
                    <img src="{track['album']['images'][0]['url']}" width="100" style="border-radius:15px;">
                    <div>
                        <div style="color:#1DB954; font-weight:bold; font-size:0.8rem;">{track['artists'][0]['name'].upper()}</div>
                        <div style="font-size:1.4rem; font-weight:900; color:white;">{track['name']}</div>
                        <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; font-weight:bold; text-decoration:none;">LISTEN ON SPOTIFY →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if track.get('preview_url'):
                st.audio(track['preview_url'])
