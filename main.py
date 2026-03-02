import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. CONFIG & PERFORMANCE ---
st.set_page_config(page_title="VibeLab Ultimate", page_icon="⚡", layout="wide")

# פונקציית חיפוש עם זיכרון מטמון למהירות מקסימלית
@st.cache_data(ttl=3600)
def search_tracks(_sp_instance, query):
    try:
        return _sp_instance.search(q=query, limit=15, type='track')['tracks']['items']
    except:
        return []

# --- 2. MULTI-LANG DATA ---
DATA = {
    'EN': {
        'title': 'VIBELAB ELITE', 'name': 'Full Name', 'btn': 'GENERATE VIBE ⚡',
        'genres': ["Pop", "Hip Hop", "Rock", "Techno", "Lofi", "R&B", "EDM"],
        'vibes': ["Party", "Chill", "Workout", "Focus", "Deep Focus", "Romantic"],
        'history': 'Recent Mixes', 'placeholder': 'Type your name...'
    },
    'HE': {
        'title': 'VIBELAB אולטימטיבי', 'name': 'שם מלא', 'btn': 'צור חוויה ⚡',
        'genres': ["מזרחית", "פופ", "היפ הופ", "ישראלי", "טכנו", "אלקטרוני", "ים תיכוני"],
        'vibes': ["מסיבה", "רגוע", "אימון", "ריכוז", "רומנטי", "שבת"],
        'history': 'היסטוריית מיקסים', 'placeholder': 'איך קוראים לך?'
    }
}

# --- 3. DYNAMIC UI (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Assistant', sans-serif; background: #050505; color: white; }
    .main-title { background: linear-gradient(90deg, #1DB954, #00cdff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 60px; font-weight: 900; text-align: center; }
    .stButton>button { border-radius: 12px; height: 3.5rem; background: #1DB954 !important; color: white !important; font-weight: bold; border: none; transition: 0.3s; width: 100%; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #1DB954; }
    .song-box { background: rgba(255,255,255,0.07); padding: 15px; border-radius: 15px; margin-bottom: 10px; border-right: 5px solid #1DB954; display: flex; align-items: center; gap: 15px; }
    .platform-card { border: 1px solid #333; padding: 10px; border-radius: 10px; text-align: center; cursor: pointer; }
</style>
""", unsafe_allow_html=True)

# --- 4. SESSION MANAGEMENT ---
if 'lang' not in st.session_state: st.session_state.lang = 'HE'
if 'history' not in st.session_state: st.session_state.history = []
if 'platform' not in st.session_state: st.session_state.platform = 'Spotify'

# --- 5. SIDEBAR & SETTINGS ---
with st.sidebar:
    st.markdown("### 🌐 Language / שפה")
    col_l1, col_l2 = st.columns(2)
    if col_l1.button("🇮🇱 HE"): st.session_state.lang = 'HE'
    if col_l2.button("🇺🇸 EN"): st.session_state.lang = 'EN'
    
    st.divider()
    st.markdown(f"### 🕒 {DATA[st.session_state.lang]['history']}")
    for h in st.session_state.history[-5:]:
        st.caption(f"🎵 {h}")

# --- 6. MAIN INTERFACE ---
L = DATA[st.session_state.lang]
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)

# בחירת פלטפורמה
p_col1, p_col2 = st.columns(2)
with p_col1:
    if st.button("Spotify 🟢"): st.session_state.platform = 'Spotify'
with p_col2:
    if st.button("Apple Music 🔴"): st.session_state.platform = 'Apple'

st.info(f"Platform: **{st.session_state.platform}**")

# קלט משתמש
u_name = st.text_input(L['name'], placeholder=L['placeholder'])
c1, c2 = st.columns(2)
with c1: u_genre = st.selectbox("Genre / ז'אנר", L['genres'])
with c2: u_vibe = st.selectbox("Vibe / אווירה", L['vibes'])

# --- 7. EXECUTION ---
if st.button(L['btn']):
    if not u_name:
        st.warning("Please enter your name / נא להזין שם")
    else:
        try:
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                client_id=st.secrets["CLIENT_ID"], 
                client_secret=st.secrets["CLIENT_SECRET"]
            ))
            
            with st.spinner('Building your Vibe...'):
                query = f"{u_genre} {u_vibe}"
                tracks = search_tracks(sp, query)
                
                if tracks:
                    st.session_state.history.append(f"{u_name}: {u_genre}")
                    st.balloons()
                    
                    st.markdown(f"### ✨ {u_name}'s Special Mix:")
                    for t in tracks:
                        # בחירת לינק לפי פלטפורמה (ב-Apple זה יחפש כרגע, כי אין API פתוח כמו ספוטיפיי ללא אישור)
                        link = t['external_urls']['spotify'] if st.session_state.platform == 'Spotify' else f"https://music.apple.com/search?term={t['name']}"
                        
                        st.markdown(f"""
                        <div class="song-box">
                            <img src="{t['album']['images'][0]['url']}" width="60" style="border-radius:10px;">
                            <div style="flex-grow:1; {'text-align:right' if st.session_state.lang == 'HE' else ''}">
                                <div style="font-weight:bold; font-size:16px;">{t['name']}</div>
                                <div style="color:#1DB954;">{t['artists'][0]['name']}</div>
                            </div>
                            <a href="{link}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">LISTEN</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("No results found. Try changing the genre.")
        except Exception as e:
            st.error("Connection Error. Make sure your SECRETS are configured.")
