import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. הגדרות דף בסיסיות ---
st.set_page_config(page_title="VibeLab Global", page_icon="🎧", layout="centered")

# ניהול שפה
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. מילון נתונים (ז'אנרים ווייבים בלבד) ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'sub': 'AI Global Music Curator',
        'name': 'Name', 'genre': 'Genre', 'vibe': 'Vibe', 'btn': 'GENERATE VIBE ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno", "Jazz", "Electronic"],
        'vibes': ["Party", "Chill", "Gym", "Focus"]
    },
    'HE': {
        'title': 'VIBELAB', 'sub': 'אוצר המוזיקה החכם',
        'name': 'שם', 'genre': 'ז\'אנר', 'vibe': 'אווירה', 'btn': 'צור פלייליסט ⚡',
        'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ", "אלקטרוני"],
        'vibes': ["מסיבה", "רגוע", "כושר", "ריכוז"]
    },
    'RU': {
        'title': 'VIBELAB', 'sub': 'Музыкальный гид',
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

# --- 3. עיצוב נקי ופשוט (חסין שגיאות) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { color: #1DB954; text-align: center; font-size: 50px; font-weight: 800; }
    .stButton>button { background-color: #1DB954 !important; color: white !important; font-weight: bold; border-radius: 8px; width: 100%; height: 50px; border: none; }
    label { color: #1DB954 !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. חיבור לספוטיפיי ---
@st.cache_resource
def connect_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = connect_sp()

# --- 5. ממשק המשתמש ---
# כפתורי שפה בולטים למעלה
c1, c2, c3, c4 = st.columns(4)
if c1.button("🇺🇸 EN"): st.session_state.lang = 'EN'
if c2.button("🇮🇱 HE"): st.session_state.lang = 'HE'
if c3.button("🇷🇺 RU"): st.session_state.lang = 'RU'
if c4.button("🇸🇦 AR"): st.session_state.lang = 'AR'

L = DATA[st.session_state.lang]

st.markdown(f"<h1>{L['title']}</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#888;'>{L['sub']}</p>", unsafe_allow_html=True)

# קלט מהמשתמש
u_name = st.text_input(L['name'], placeholder="...")
col_left, col_right = st.columns(2)
with col_left:
    u_genre = st.selectbox(L['genre'], L['genres'])
with col_right:
    u_vibe = st.selectbox(L['vibe'], L['vibes'])

if st.button(L['btn']):
    if not u_name:
        st.warning("Please enter your name")
    elif not sp:
        st.error("Spotify Connection Failed")
    else:
        with st.spinner('Curating...'):
            try:
                # חיפוש ישיר של שירים לפי ז'אנר ווייב
                query = f"genre:{u_genre} {u_vibe}"
                if st.session_state.lang == 'HE' and u_genre == "מזרחית":
                    query = f"מזרחית {u_vibe}" # טיפול מיוחד למזרחית
                
                res = sp.search(q=query, limit=12, type='track')
                if res and res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
                else:
                    st.warning("No tracks found for this vibe. Try another!")
            except:
                st.error("Spotify is busy. Wait 5 seconds.")

# --- 6. תצוגת תוצאות ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s {u_vibe} Selection:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:10px; display:flex; align-items:center; gap:15px; border-left:4px solid #1DB954;">
            <img src="{t['album']['images'][0]['url']}" width="50" style="border-radius:5px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:14px;">{t['name']}</div>
                <div style="color:#1DB954; font-size:12px;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold; font-size:12px;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
