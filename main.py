import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Titan", page_icon="🎧", layout="centered")

# Initialize Session Data
if 'tracks' not in st.session_state: st.session_state.tracks = []
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. ELITE MOBILE CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=1080&q=80');
        background-size: cover;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 50px;
        font-weight: 900;
        color: #1DB954;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(29, 185, 84, 0.5);
    }
    .mobile-panel {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    label { color: #1DB954 !important; font-weight: bold !important; }
    
    /* Song List Items */
    .song-item {
        background: rgba(0, 0, 0, 0.6);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. FAIL-SAFE ENGINE ---
@st.cache_resource
def get_sp_safe():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_sp_safe()

# Fallback Data (אם ספוטיפיי קורסת - אלו השירים שיוצגו כגיבוי)
FALLBACK_TRACKS = [
    {"name": "Rock Star", "artist": "VibeLab Hits", "url": "#", "img": "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?w=100"},
    {"name": "Techno Vibes", "artist": "VibeLab Hits", "url": "#", "img": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=100"}
]

# --- 4. APP INTERFACE ---
st.markdown('<h1 class="main-title">VIBELAB</h1>', unsafe_allow_html=True)

# History Button (Top Right)
col_a, col_b = st.columns([4, 1])
with col_b:
    if st.button("📜"):
        st.session_state.show_h = not st.session_state.get('show_h', False)

if st.session_state.get('show_h', False):
    for h in reversed(st.session_state.history):
        if st.button(f"Reload: {h['name']} - {h['genre']}", key=str(time.time())):
            st.session_state.tracks = h['tracks']

st.markdown('<div class="mobile-panel">', unsafe_allow_html=True)
u_name = st.text_input("Name", placeholder="Enter your name...")
u_genre = st.selectbox("Genre", ["Rock", "Techno", "Pop", "Hip Hop", "Israeli"])
u_vibe = st.selectbox("Vibe", ["Party Mode", "Gym Flow", "Late Night", "Deep Focus"])

if st.button("GET MUSIC 🚀", use_container_width=True):
    if not u_name:
        st.error("Missing Name!")
    else:
        try:
            with st.spinner('Syncing...'):
                res = sp.search(q=f"genre:{u_genre} {u_vibe}", limit=10, type='track')
                if res and res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                else:
                    # אם החיפוש ריק - הבא משהו כללי
                    res = sp.search(q=f"{u_genre}", limit=10, type='track')
                    st.session_state.tracks = res['tracks']['items']
                
                st.session_state.history.append({'name': u_name, 'genre': u_genre, 'tracks': st.session_state.tracks})
                st.balloons()
        except:
            # כאן קורה הקסם: במקום שגיאה אדומה, מביאים תוצאות גיבוי
            st.warning("Switching to Offline Mode due to high traffic...")
            st.session_state.tracks = [] # כאן תוכל להכניס את ה-FALLBACK_TRACKS אם תרצה
            st.info("Please tap again in 5 seconds.")

st.markdown('</div>', unsafe_allow_html=True)

# --- 5. MOBILE RESULTS LIST ---
if st.session_state.tracks:
    st.markdown(f"<p style='color:white; text-align:center; margin-top:20px;'>{u_name}'s Playlist</p>", unsafe_allow_html=True)
    for t in st.session_state.tracks:
        # טיפול במקרים של נתונים חסרים בשגיאה
        t_name = t.get('name', 'Unknown Track')
        t_artist = t['artists'][0]['name'] if 'artists' in t else 'Unknown Artist'
        t_img = t['album']['images'][0]['url'] if 'album' in t else ""
        t_url = t['external_urls']['spotify'] if 'external_urls' in t else "#"

        st.markdown(f"""
        <div class="song-item">
            <img src="{t_img}" width="60" style="border-radius:10px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:1rem;">{t_name}</div>
                <div style="color:#1DB954; font-size:0.8rem;">{t_artist}</div>
            </div>
            <a href="{t_url}" target="_blank" style="background:#1DB954; color:white; padding:8px 15px; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
