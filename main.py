import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Infinity", page_icon="🎧", layout="wide", initial_sidebar_state="collapsed")

# זיכרון פנימי חכם
if 'history' not in st.session_state: st.session_state.history = []
if 'tracks' not in st.session_state: st.session_state.tracks = []
if 'last_request' not in st.session_state: st.session_state.last_request = 0

# --- 2. 4K STABLE DESIGN ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), 
        url('https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&w=3840&q=100');
        background-size: cover;
        background-attachment: fixed;
    }
    .hero-title {
        font-family: 'Arial Black', sans-serif;
        font-size: 80px;
        text-align: center;
        color: #1DB954;
        text-shadow: 0 0 30px rgba(29, 185, 84, 0.5);
        margin-top: -30px;
    }
    .ui-box {
        background: rgba(0, 0, 0, 0.9);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #1DB954;
        margin-bottom: 20px;
    }
    label { color: #1DB954 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .stTextInput>div>div>input { background-color: white !important; color: black !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. FAIL-SAFE CONNECTION ---
@st.cache_resource(show_spinner=False)
def get_sp_client():
    try:
        # וידוא שהמפתחות נקיים מרווחים
        cid = st.secrets["CLIENT_ID"].strip()
        csc = st.secrets["CLIENT_SECRET"].strip()
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csc))
    except:
        return None

sp = get_sp_client()

# --- 4. INTERFACE ---
st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)

# כפתור היסטוריה בולט
col_t, col_h = st.columns([4, 1])
with col_h:
    if st.button("📜 HISTORY ARCHIVE"):
        st.info("Check the left sidebar! ←")

st.markdown('<div class="ui-box">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    # שם נקי ללא טקסט ברירת מחדל
    u_name = st.text_input("Name", placeholder="Type your name here...")
with c2:
    # סגנון Rock תמיד מופיע
    u_genre = st.selectbox("Genre", ["Rock", "Techno", "Pop", "Hip Hop", "Israeli", "Jazz"])
with c3:
    u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill"])

if st.button("GENERATE EXPERIENCE ⚡"):
    current_time = time.time()
    # מניעת לחיצות כפולות (חייב לעבור 3 שניות בין לחיצה ללחיצה)
    if current_time - st.session_state.last_request < 3:
        st.warning("Slow down! Please wait 3 seconds.")
    elif not sp:
        st.error("Connection Error: Check your Spotify Credentials in Streamlit Secrets.")
    elif not u_name:
        st.warning("Please enter a name first.")
    else:
        st.session_state.last_request = current_time
        with st.spinner('Syncing with Spotify...'):
            try:
                # חיפוש חכם
                query = f"genre:{u_genre} {u_vibe}"
                results = sp.search(q=query, limit=12, type='track')
                
                if results and results['tracks']['items']:
                    st.session_state.tracks = results['tracks']['items']
                    st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': results['tracks']['items']})
                    st.balloons()
                else:
                    st.error("No tracks found. Try a different Vibe.")
            except Exception as e:
                # טיפול שקט בשגיאת Limit
                st.error("Spotify API is overloaded. Please wait 30 seconds and try again.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. RESULTS ---
if st.session_state.tracks:
    st.markdown(f"<h2 style='color:white; text-align:center;'>FOR {u_name.upper()}</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, track in enumerate(st.session_state.tracks):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.1); padding:15px; border-radius:15px; margin-bottom:10px; border-left:5px solid #1DB954; display:flex; align-items:center; gap:15px;">
                <img src="{track['album']['images'][0]['url']}" width="80" style="border-radius:10px;">
                <div>
                    <div style="color:#1DB954; font-weight:bold;">{track['artists'][0]['name']}</div>
                    <div style="font-size:1.2rem; font-weight:bold; color:white;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none;">PLAY NOW →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Archive")
    for i, h in enumerate(reversed(st.session_state.history)):
        if st.button(f"{h['name']} - {h['genre']} ({i+1})", key=f"h_{i}"):
            st.session_state.tracks = h['tracks']
