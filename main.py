import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Elite", page_icon="💎", layout="centered")

# אתחול משתני מערכת
if 'lang' not in st.session_state: st.session_state.lang = 'HE'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. PREMIUM CSS (GLASSMORPHISM) ---
st.markdown(r"""
<style>
    .stApp { 
        background: radial-gradient(circle at top right, #1db95422, #050505), #050505;
        color: white; 
    }
    .main-title { 
        font-size: 65px; font-weight: 900; text-align: center; 
        background: linear-gradient(to bottom, #ffffff, #1DB954);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px; letter-spacing: -2px;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .stButton>button { 
        background: #1DB954 !important; color: black !important; 
        font-weight: 900 !important; border-radius: 12px !important; 
        height: 52px !important; border: none !important;
    }
    .song-card { 
        background: rgba(255, 255, 255, 0.02); padding: 16px; border-radius: 20px; 
        margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.05);
        display: flex; align-items: center; gap: 16px; transition: 0.3s;
    }
    .pop-bar { background: #333; height: 4px; width: 100%; border-radius: 2px; margin-top: 8px; overflow: hidden; }
    .pop-fill { background: #1DB954; height: 100%; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# --- 3. MULTILINGUAL DATA ---
DATA = {
    'EN': {'title': 'VIBELAB', 'sub': 'PREMIUM EXPERIENCE', 'name': 'Full Name', 'btn': 'GENERATE ⚡', 'genres': ["Pop", "Hip Hop", "Techno", "Rock", "Jazz"], 'vibes': ["Party", "Chill", "Gym", "Focus"]},
    'HE': {'title': 'VIBELAB', 'sub': 'אוצרות מוזיקה פרימיום', 'name': 'שם מלא', 'btn': 'צור חוויה ⚡', 'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ", "אלקטרוני"], 'vibes': ["מסיבה", "רגוע", "כושר", "ריכוז"]},
    'RU': {'title': 'VIBELAB', 'sub': 'ПРЕМИУМ ВАЙБ', 'name': 'Имя', 'btn': 'СОЗДАТЬ ⚡', 'genres': ["Pop", "Rock", "Hip Hop", "Techno"], 'vibes': ["Вечеринка", "Релакс", "Спорт", "Фокус"]},
    'AR': {'title': 'VIBELAB', 'sub': 'تجربة موسيقية فاخرة', 'name': 'الاسم', 'btn': 'ابدأ ⚡', 'genres': ["Arabic Pop", "Classic", "Mahraganat"], 'vibes': ["حفلة", "استرخاء", "رياضة"]}
}

# --- 4. SPOTIFY CONNECTION (STABLE VERSION) ---
@st.cache_resource(show_spinner=False)
def get_spotify_client():
    try:
        # ניקוי רווחים מהסיקרטים למניעת שגיאות חיבור
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=csec)
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        st.error(f"Connection Error: Check your Secrets")
        return None

sp = get_spotify_client()

# פונקציית חיפוש עם Cache למניעת השגיאה של ה-5 שניות
@st.cache_data(ttl=600) # זוכר תוצאות ל-10 דקות
def fetch_tracks(query):
    if sp:
        return sp.search(q=query, limit=12, type='track')
    return None

# --- 5. UI LAYOUT ---
c_langs = st.columns(4)
lang_map = [("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]
for i, (label, code) in enumerate(lang_map):
    if c_langs[i].button(label, key=f"lang_{code}"):
        st.session_state.lang = code
        st.rerun()

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#555; font-weight:bold; letter-spacing:2px;'>{L['sub']}</p>", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
u_name = st.text_input(L['name'], placeholder="...")
c1, c2 = st.columns(2)
with c1: u_genre = st.selectbox("Genre", L['genres'])
with c2: u_vibe = st.selectbox("Vibe", L['vibes'])

if st.button(L['btn'], use_container_width=True):
    if not u_name:
        st.warning("Please enter your name")
    else:
        with st.spinner('Syncing...'):
            query = f"{u_genre} {u_vibe} hits"
            results = fetch_tracks(query)
            if results and results['tracks']['items']:
                st.session_state.tracks = results['tracks']['items']
                st.balloons()
            else:
                st.error("Could not find tracks. Try another combination.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. DISPLAY ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s {st.session_state.lang} Selection")
    for t in st.session_state.tracks:
        pop = t['popularity']
        st.markdown(f"""
        <div class="song-card">
            <img src="{t['album']['images'][0]['url']}" width="70" style="border-radius:12px;">
            <div style="flex-grow:1;">
                <div style="font-weight:900; font-size:1.1rem; color:white;">{t['name']}</div>
                <div style="color:#1DB954; font-size:0.9rem; font-weight:700;">{t['artists'][0]['name']}</div>
                <div class="pop-bar"><div class="pop-fill" style="width:{pop}%;"></div></div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="text-decoration:none;">
                <div style="background:white; color:black; padding:10px 18px; border-radius:10px; font-weight:900; font-size:0.7rem;">PLAY</div>
            </a>
        </div>
        """, unsafe_allow_html=True)
