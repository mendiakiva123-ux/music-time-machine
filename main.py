import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Elite", page_icon="🎧", layout="wide")

# --- 2. CSS & DESIGN (יוקרה בינלאומית) ---
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    .stApp { background-color: #0b0d11; color: white; font-family: 'Inter', sans-serif; }
    .main-title { color: #1DB954; font-size: 50px; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .song-box { 
        background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; 
        margin-bottom: 12px; border-left: 5px solid #1DB954; display: flex; align-items: center; gap: 15px;
        transition: 0.3s;
    }
    .song-box:hover { background: rgba(255,255,255,0.1); transform: scale(1.01); }
    .stButton>button { 
        background: linear-gradient(90deg, #1DB954, #19e68c) !important; color: black !important; 
        font-weight: bold; border-radius: 12px; height: 50px; border: none; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA & LANGUAGES ---
DATA = {
    'EN': {
        'title': 'VIBELAB ELITE', 'name': 'Your Name', 'btn': 'GENERATE MIX ⚡',
        'genres': ["Pop", "Hip Hop", "Rock", "Techno", "R&B", "Country"],
        'vibes': ["Party", "Chill", "Workout", "Romantic"]
    },
    'HE': {
        'title': 'VIBELAB אולטימטיבי', 'name': 'שם מלא', 'btn': 'צור חוויה ⚡',
        'genres': ["מזרחית", "פופ", "היפ הופ", "ישראלי", "טכנו", "ים תיכוני"],
        'vibes': ["מסיבה", "רגוע", "אימון", "ריכוז"]
    }
}

if 'lang' not in st.session_state: st.session_state.lang = 'HE'
if 'platform' not in st.session_state: st.session_state.platform = 'Spotify'

# --- 4. SPOTIFY CONNECTION ---
def get_sp():
    try:
        # וודא שהשמות ב-Secrets הם בדיוק אלו
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))
    except Exception as e:
        st.error(f"Error connecting to Spotify: {e}")
        return None

# --- 5. UI LAYOUT ---
with st.sidebar:
    st.markdown("### 🌐 Language / שפה")
    if st.button("🇮🇱 עברית"): st.session_state.lang = 'HE'
    if st.button("🇺🇸 English"): st.session_state.lang = 'EN'
    
    st.divider()
    st.markdown("### 📱 Platform")
    if st.button("Spotify 🟢"): st.session_state.platform = 'Spotify'
    if st.button("Apple Music 🔴"): st.session_state.platform = 'Apple'

L = DATA[st.session_state.lang]
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)

# INPUTS
u_name = st.text_input(L['name'], placeholder="...")
col1, col2 = st.columns(2)
with col1: u_genre = st.selectbox("Genre / ז'אנר", L['genres'])
with col2: u_vibe = st.selectbox("Vibe / אווירה", L['vibes'])

# --- 6. SEARCH LOGIC ---
if st.button(L['btn']):
    if not u_name:
        st.warning("Please enter your name")
    else:
        sp = get_sp()
        if sp:
            with st.spinner('Fetching tracks...'):
                # בניית שאילתה חכמה - מחפש את הז'אנר והווייב
                query = f"{u_genre} {u_vibe}"
                results = sp.search(q=query, limit=12, type='track')
                tracks = results['tracks']['items']
                
                if tracks:
                    st.balloons()
                    st.success(f"Hey {u_name}, here is your {u_vibe} mix!")
                    
                    for t in tracks:
                        link = t['external_urls']['spotify'] if st.session_state.platform == 'Spotify' else f"https://music.apple.com/search?term={t['name']} {t['artists'][0]['name']}"
                        
                        st.markdown(f"""
                        <div class="song-box">
                            <img src="{t['album']['images'][0]['url']}" width="65" style="border-radius:10px;">
                            <div style="flex-grow:1; {'text-align:right' if st.session_state.lang == 'HE' else ''}">
                                <div style="font-weight:bold; font-size:18px;">{t['name']}</div>
                                <div style="color:#1DB954; font-size:14px;">{t['artists'][0]['name']}</div>
                            </div>
                            <a href="{link}" target="_blank" style="background:#1DB954; color:black; padding:8px 15px; border-radius:20px; text-decoration:none; font-weight:bold; font-size:12px;">LISTEN</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("No tracks found. Try a different combination!")
