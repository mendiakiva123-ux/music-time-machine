import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Elite", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. ELITE CSS (SAFE MODE) ---
# הפרדה מוחלטת של העיצוב למניעת SyntaxError
UI_STYLE = """
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), 
        url('https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
    }
    .main-title {
        color: #1DB954;
        font-family: 'Inter', sans-serif;
        font-size: 65px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: -2px;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1DB954, #19a34a) !important;
        color: white !important;
        font-weight: 900 !important;
        border: none !important;
        height: 55px !important;
        border-radius: 15px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    label { color: #1DB954 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .song-card {
        background: rgba(0, 0, 0, 0.5);
        padding: 15px;
        border-radius: 18px;
        border-left: 5px solid #1DB954;
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 12px;
    }
</style>
"""
st.markdown(UI_STYLE, unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'sub': 'Premium AI Music Experience',
        'name': 'Full Name', 'genre': 'Musical Genre', 'vibe': 'Current Vibe', 'btn': 'GENERATE EXPERIENCE ⚡',
        'genres': ["Pop", "Hip Hop", "Rock", "Techno", "Jazz", "Electronic"],
        'vibes': ["Party Mode", "Chill & Relax", "Gym Energy", "Deep Focus"]
    },
    'HE': {
        'title': 'VIBELAB', 'sub': 'חווית מוזיקה בסטנדרט גבוה',
        'name': 'שם מלא', 'genre': 'ז\'אנר מוזיקלי', 'vibe': 'מה הוויב?', 'btn': 'צור את הקסם ⚡',
        'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ", "אלקטרוני"],
        'vibes': ["מסיבה", "רגוע", "כושר", "ריכוז"]
    },
    'RU': {
        'title': 'VIBELAB', 'sub': 'Музыка премиум-класса',
        'name': 'Имя', 'genre': 'Жанр', 'vibe': 'Вайб', 'btn': 'СОЗДАТЬ ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno"],
        'vibes': ["Вечеринка", "Релакс", "Спорт", "Фокус"]
    },
    'AR': {
        'title': 'VIBELAB', 'sub': 'تجربة موسيقية متميزة',
        'name': 'الاسم الكامل', 'genre': 'النوع', 'vibe': 'الجو العام', 'btn': 'انطلق ⚡',
        'genres': ["Arabic Pop", "Mahraganat", "Classic", "Hip Hop"],
        'vibes': ["حفلة", "استرخاء", "رياضة", "تركيز"]
    }
}

# --- 4. SPOTIFY CONNECTION ---
@st.cache_resource
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_sp()

# --- 5. UI LAYOUT ---
# Language Selectors (Premium Buttons)
l_cols = st.columns([1,1,1,1])
if l_cols[0].button("🇺🇸 EN"): st.session_state.lang = 'EN'
if l_cols[1].button("🇮🇱 HE"): st.session_state.lang = 'HE'
if l_cols[2].button("🇷🇺 RU"): st.session_state.lang = 'RU'
if l_cols[3].button("🇸🇦 AR"): st.session_state.lang = 'AR'

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color:#888; margin-top:-15px; font-weight:500;">{L["sub"]}</p>', unsafe_allow_html=True)

# Main Input Panel
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
u_name = st.text_input(L['name'], placeholder="...")
c1, c2 = st.columns(2)
with c1:
    u_genre = st.selectbox(L['genre'], L['genres'])
with c2:
    u_vibe = st.selectbox(L['vibe'], L['vibes'])

if st.button(L['btn'], use_container_width=True):
    if not u_name:
        st.error("Please provide a name")
    elif not sp:
        st.error("Spotify Connection Failed")
    else:
        with st.spinner('Syncing with Spotify Global...'):
            try:
                # חיפוש חכם שמשלב ז'אנר ואווירה לקבלת תוצאות מדויקות
                query = f"{u_genre} {u_vibe} hits"
                res = sp.search(q=query, limit=12, type='track')
                if res and res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
                else:
                    st.warning("No results found. Try a different vibe.")
            except:
                st.error("Spotify is overwhelmed. Wait 5 seconds.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. DISPLAY RESULTS ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s {u_vibe} Experience:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div class="song-card">
            <img src="{t['album']['images'][0]['url']}" width="60" style="border-radius:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:1.1rem;">{t['name']}</div>
                <div style="color:#1DB954; font-size:0.9rem; font-weight:500;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" 
               style="background:#1DB954; color:white; padding:10px 20px; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:bold; box-shadow: 0 4px 15px rgba(29,185,84,0.3);">
               PLAY
            </a>
        </div>
        """, unsafe_allow_html=True)
