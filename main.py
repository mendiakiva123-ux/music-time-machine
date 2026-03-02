import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Elite", page_icon="💎", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. PREMIUM CSS (GLASSMORPHISM) ---
st.markdown(r"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at top right, #1db95422, #050505), #050505;
        font-family: 'Inter', sans-serif;
        color: white; 
    }
    .main-title { 
        font-size: 72px; font-weight: 900; text-align: center; 
        background: linear-gradient(to bottom, #ffffff, #1DB954);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px; letter-spacing: -2px;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .stButton>button { 
        background: #1DB954 !important; color: black !important; 
        font-weight: 900 !important; border-radius: 12px !important; 
        height: 52px !important; border: none !important; transition: 0.4s !important;
        text-transform: uppercase;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(29,185,84,0.4); }
    .song-card { 
        background: rgba(255, 255, 255, 0.02); padding: 16px; border-radius: 20px; 
        margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.05);
        display: flex; align-items: center; gap: 16px; transition: 0.3s;
    }
    .song-card:hover { background: rgba(255, 255, 255, 0.08); border-color: #1DB954; }
    .pop-bar { background: #333; height: 4px; width: 100%; border-radius: 2px; margin-top: 8px; overflow: hidden; }
    .pop-fill { background: #1DB954; height: 100%; border-radius: 2px; }
    label { color: #888 !important; font-size: 0.9rem !important; margin-bottom: 5px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. MULTILINGUAL DATA ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'sub': 'ULTRA PREMIUM CURATION', 'name_lbl': 'YOUR NAME',
        'gen_lbl': 'GENRE', 'vib_lbl': 'VIBE', 'btn': 'GENERATE EXPERIENCE ⚡',
        'genres': ["Pop", "Hip Hop", "Techno", "Rock", "Latin Hits", "Jazz", "80s Retro", "Lofi"],
        'vibes': ["Party Mode", "Chill & Relax", "Gym Energy", "Deep Focus", "Night Drive"],
        'dl': "📥 DOWNLOAD LIST"
    },
    'HE': {
        'title': 'VIBELAB', 'sub': 'אוצרות מוזיקה בסטנדרט הייטק', 'name_lbl': 'שם מלא',
        'gen_lbl': 'סגנון', 'vib_lbl': 'אווירה', 'btn': 'צור חוויה ⚡',
        'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ", "אלקטרוני", "חסידי", "רוק", "נוסטלגיה"],
        'vibes': ["מסיבה", "רגוע", "כושר", "ריכוז", "נסיעת לילה"],
        'dl': "📥 הורד רשימת שירים"
    },
    'RU': {
        'title': 'VIBELAB', 'sub': 'ПРЕМИАЛЬНЫЙ КУРАТОР', 'name_lbl': 'ВАШЕ ИМЯ',
        'gen_lbl': 'ЖАНР', 'vib_lbl': 'ВАЙБ', 'btn': 'СОЗДАТЬ ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno", "Deep House", "Russian Hits"],
        'vibes': ["Вечеринка", "Релакс", "Спорт", "Фокус", "Ночная езда"],
        'dl': "📥 СКАЧАТЬ СПИСОК"
    },
    'AR': {
        'title': 'VIBELAB', 'sub': 'تجربة موسيقية فاخرة', 'name_lbl': 'الاسم الكامل',
        'gen_lbl': 'النوع', 'vib_lbl': 'الجو', 'btn': 'ابدأ التجربة ⚡',
        'genres': ["Arabic Pop", "Classic", "Mahraganat", "Hip Hop", "Techno"],
        'vibes': ["حفلة", "استرخاء", "رياضة", "تركيز", "قيادة ليلية"],
        'dl': "📥 تحميل القائمة"
    }
}

# --- 4. SPOTIFY ---
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
c_langs = st.columns(4)
lang_map = [("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]
for i, (label, code) in enumerate(lang_map):
    if c_langs[i].button(label):
        st.session_state.lang = code
        st.rerun()

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#555; font-weight:bold; letter-spacing:3px; margin-top:-15px;'>{L['sub']}</p>", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
u_name = st.text_input(L['name_lbl'], placeholder="Type here...")

col1, col2 = st.columns(2)
with col1: u_genre = st.selectbox(L['gen_lbl'], L['genres'])
with col2: u_vibe = st.selectbox(L['vib_lbl'], L['vibes'])

btn_main, btn_surp = st.columns([4, 1])
do_search = btn_main.button(L['btn'])
do_surprise = btn_surp.button("🎲")
st.markdown('</div>', unsafe_allow_html=True)

search_q = None
if do_search: search_q = f"{u_genre} {u_vibe} hits"
elif do_surprise:
    u_genre, u_vibe = random.choice(L['genres']), random.choice(L['vibes'])
    search_q = f"{u_genre} {u_vibe} hits"
    st.toast(f"🎲 Random: {u_genre} + {u_vibe}")

if search_q:
    if not u_name: st.warning("Please enter your name")
    elif not sp: st.error("Spotify Connection Failed")
    else:
        with st.spinner('Syncing with Spotify...'):
            try:
                res = sp.search(q=search_q, limit=12, type='track')
                st.session_state.tracks = res['tracks']['items']
                st.balloons()
            except: st.error("Spotify Limit. Wait 5s.")

# --- 6. DISPLAY RESULTS ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s {u_vibe} Universe")
    
    list_txt = "\n".join([f"{t['name']} - {t['artists'][0]['name']}" for t in st.session_state.tracks])
    st.download_button(L['dl'], list_txt, file_name="vibelab_list.txt")

    for t in st.session_state.tracks:
        pop = t['popularity']
        preview = t.get('preview_url')
        st.markdown(f"""
        <div class="song-card">
            <img src="{t['album']['images'][0]['url']}" width="70" style="border-radius:12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
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
        if preview:
            st.audio(preview)
