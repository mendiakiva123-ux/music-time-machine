import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. הגדרות דף ---
st.set_page_config(page_title="VibeLab Infinity", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. מילון נתונים (ז'אנרים ווייבים בלבד) ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'sub': 'AI Music Curator',
        'name': 'Your Name', 'genre': 'Genre', 'vibe': 'Vibe', 'btn': 'GET THE VIBE ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno", "Jazz", "Latin"],
        'vibes': ["Party Mode", "Chill & Relax", "Gym Energy", "Deep Focus"]
    },
    'HE': {
        'title': 'VIBELAB', 'sub': 'אוצר המוזיקה החכם',
        'name': 'שם המשתמש', 'genre': 'ז\'אנר', 'vibe': 'אווירה', 'btn': 'צור חוויה ⚡',
        'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ", "אלקטרוני"],
        'vibes': ["מסיבה", "רגוע", "כושר", "ריכוז"]
    },
    'RU': {
        'title': 'VIBELAB', 'sub': 'Музыкальный гиד',
        'name': 'Имя', 'genre': 'Жанр', 'vibe': 'Вайб', 'btn': 'ИГРАТЬ ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno"],
        'vibes': ["Вечеринка", "Релакс", "Спорт", "Фокус"]
    },
    'AR': {
        'title': 'VIBELAB', 'sub': 'تجربة الموسيقى الذكية',
        'name': 'الاسم', 'genre': 'النوع', 'vibe': 'الجو', 'btn': 'ابدأ ⚡',
        'genres': ["Arabic Pop", "Mahraganat", "Classic", "Hip Hop"],
        'vibes': ["حفلة", "استرخاء", "رياضة", "تركيز"]
    }
}

# --- 3. עיצוב חסין (Clean & Simple) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1 { color: #1DB954; text-align: center; font-family: 'Inter', sans-serif; font-weight: 900; }
    p { text-align: center; color: #888; }
    .stButton>button { background-color: #1DB954 !important; color: white !important; font-weight: bold; border-radius: 10px; width: 100%; height: 3em; }
    label { color: #1DB954 !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

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

# --- 5. ממשק המשתמש ---
# כפתורי שפה מהירים
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🇺🇸 EN"): st.session_state.lang = 'EN'
with c2: 
    if st.button("🇮🇱 HE"): st.session_state.lang = 'HE'
with c3: 
    if st.button("🇷🇺 RU"): st.session_state.lang = 'RU'
with c4: 
    if st.button("🇸🇦 AR"): st.session_state.lang = 'AR'

L = DATA[st.session_state.lang]

st.title(L['title'])
st.write(L['sub'])

# קלט משתמש
u_name = st.text_input(L['name'], placeholder="...")
col_a, col_b = st.columns(2)
with col_a:
    u_genre = st.selectbox(L['genre'], L['genres'])
with col_b:
    u_vibe = st.selectbox(L['vibe'], L['vibes'])

if st.button(L['btn']):
    if not u_name:
        st.error("Name required")
    elif not sp:
        st.error("Spotify Error")
    else:
        with st.spinner('Curating...'):
            try:
                # חיפוש חכם: משלב את השפה, הז'אנר והווייב
                search_query = f"{u_genre} {u_vibe}"
                results = sp.search(q=search_query, limit=12, type='track')
                
                if results['tracks']['items']:
                    st.session_state.tracks = results['tracks']['items']
                else:
                    st.warning("No results found. Try another mix.")
            except Exception as e:
                st.error("Spotify limit reached. Wait 10 seconds.")

# --- 6. הצגת התוצאות ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s {u_vibe} Mix:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:12px; margin-bottom:8px; display:flex; align-items:center; gap:15px; border-left:4px solid #1DB954;">
            <img src="{t['album']['images'][0]['url']}" width="50" style="border-radius:5px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:15px;">{t['name']}</div>
                <div style="color:#1DB954; font-size:12px;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold; font-size:13px;">LISTEN</a>
        </div>
        """, unsafe_allow_html=True)
