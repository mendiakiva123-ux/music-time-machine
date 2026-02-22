import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. הגדרות דף ---
st.set_page_config(page_title="VibeLab Elite", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. עיצוב חסין (SAFE CSS) ---
# שימוש במחרוזת גולמית (r"") למניעת שגיאות Syntax
UI_STYLE = r"""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { color: #1DB954; font-size: 55px; font-weight: 900; text-align: center; }
    .stButton>button { 
        background-color: #1DB954 !important; color: white !important; 
        font-weight: bold; border-radius: 12px; height: 50px; width: 100%; border: none;
    }
    label { color: #1DB954 !important; font-weight: bold !important; }
    .song-box { 
        background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; 
        margin-bottom: 10px; border-left: 5px solid #1DB954; 
        display: flex; align-items: center; gap: 15px;
    }
</style>
"""
st.markdown(UI_STYLE, unsafe_allow_html=True)

# --- 3. נתונים (בלי זמרים) ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'sub': 'Premium AI Music Experience',
        'name': 'Full Name', 'genre': 'Genre', 'vibe': 'Vibe', 'btn': 'GENERATE VIBE ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno", "Jazz"],
        'vibes': ["Party Mode", "Chill & Relax", "Gym Energy", "Deep Focus"]
    },
    'HE': {
        'title': 'VIBELAB', 'sub': 'חווית מוזיקה בסטנדרט גבוה',
        'name': 'שם מלא', 'genre': 'ז\'אנר', 'vibe': 'מה הוויב?', 'btn': 'צור את הקסם ⚡',
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
        'name': 'الاسم', 'genre': 'النوع', 'vibe': 'الجو', 'btn': 'انطلق ⚡',
        'genres': ["Arabic Pop", "Mahraganat", "Classic", "Hip Hop"],
        'vibes': ["حفلة", "استرخاء", "رياضة", "تركيز"]
    }
}

# --- 4. חיבור לספוטיפיי ---
@st.cache_resource
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_sp()

# --- 5. ממשק משתמש ---
# כפתורי שפה (ניקוי המלבנים)
c_lang = st.columns(4)
languages = [("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]
for i, (label, code) in enumerate(languages):
    if c_lang[i].button(label):
        st.session_state.lang = code
        st.rerun()

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:gray; margin-top:-15px;'>{L['sub']}</p>", unsafe_allow_html=True)

# הטופס הראשי
u_name = st.text_input(L['name'], placeholder="...")
col1, col2 = st.columns(2)
with col1:
    u_genre = st.selectbox(L['genre'], L['genres'])
with col2:
    u_vibe = st.selectbox(L['vibe'], L['vibes'])

if st.button(L['btn']):
    if not u_name:
        st.warning("Please enter your name")
    elif not sp:
        st.error("Spotify Connection Error")
    else:
        with st.spinner('Syncing...'):
            try:
                # חיפוש שירים (Tracks) ישיר - הכי יציב
                search_query = f"{u_genre} {u_vibe} hits"
                res = sp.search(q=search_query, limit=10, type='track')
                if res and res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
                else:
                    st.warning("No results. Try another vibe.")
            except:
                st.error("Spotify limit reached. Wait 5 seconds.")

# --- 6. הצגת תוצאות ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s {u_vibe} Selection:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div class="song-box">
            <img src="{t['album']['images'][0]['url']}" width="55" style="border-radius:10px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold;">{t['name']}</div>
                <div style="color:#1DB954; font-size:13px;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold; font-size:13px;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
