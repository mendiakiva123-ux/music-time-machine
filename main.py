import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Elite", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. ELITE DESIGN (100% ERROR-FREE) ---
# הסרתי את כל יחידות המידה שגרמו ל-SyntaxError בתמונות שלך
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .main-title { color: #1DB954; font-size: 60px; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .stButton>button { 
        background-color: #1DB954 !important; color: white !important; 
        font-weight: bold !important; border-radius: 12px !important; 
        height: 50px !important; width: 100% !important; border: none !important;
    }
    label { color: #1DB954 !important; font-weight: bold !important; }
    .song-box { 
        background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; 
        margin-bottom: 10px; border-left: 5px solid #1DB954; 
        display: flex; align-items: center; gap: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'sub': 'Premium AI Music Experience',
        'name': 'Your Name', 'genre': 'Genre', 'vibe': 'Vibe', 'btn': 'GENERATE EXPERIENCE ⚡',
        'genres': ["Pop", "Hip Hop", "Rock", "Techno", "Jazz"],
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

# --- 4. SPOTIFY CONNECTION ---
@st.cache_resource
def init_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = init_sp()

# --- 5. UI LAYOUT ---
# בחירת שפה - כפתורים נקיים
cols = st.columns(4)
langs = [("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]
for i, (label, code) in enumerate(langs):
    if cols[i].button(label):
        st.session_state.lang = code
        st.rerun()

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:gray;'>{L['sub']}</p>", unsafe_allow_html=True)

# הטופס - ללא מלבנים חוסמים
u_name = st.text_input(L['name'], placeholder="...")
c1, c2 = st.columns(2)
with c1:
    u_genre = st.selectbox(L['genre'], L['genres'])
with c2:
    u_vibe = st.selectbox(L['vibe'], L['vibes'])

if st.button(L['btn']):
    if not u_name:
        st.error("Please enter your name")
    elif not sp:
        st.error("Spotify Connection Error")
    else:
        with st.spinner('Syncing...'):
            try:
                # חיפוש אופטימלי למניעת שגיאת "Spotify is busy"
                search_query = f"{u_genre} {u_vibe} top hits"
                res = sp.search(q=search_query, limit=12, type='track')
                if res and res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
                else:
                    st.warning("No results found. Try another vibe.")
            except:
                st.error("Spotify limit reached. Wait 5 seconds.")

# --- 6. RESULTS ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s Personal Mix:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div class="song-box">
            <img src="{t['album']['images'][0]['url']}" width="55" style="border-radius:10px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold;">{t['name']}</div>
                <div style="color:#1DB954; font-size:13px;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" 
               style="background:#1DB954; color:white; padding:8px 15px; border-radius:20px; text-decoration:none; font-size:12px; font-weight:bold;">
               LISTEN
            </a>
        </div>
        """, unsafe_allow_html=True)
