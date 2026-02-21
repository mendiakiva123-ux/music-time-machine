import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. הגדרות דף ---
st.set_page_config(page_title="VibeLab Global", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. מילון נתונים (ללא זמרים - רק ז'אנרים ווייבים) ---
DATA = {
    'EN': {
        'title': 'VIBELAB',
        'sub': 'AI Global Music Curator',
        'name': 'Your Name', 'genre': 'Select Genre', 'vibe': 'Current Vibe', 'btn': 'GENERATE VIBE ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno", "Jazz"],
        'vibes': ["Party Mode", "Chill & Relax", "Gym Energy", "Deep Focus"]
    },
    'HE': {
        'title': 'VIBELAB',
        'sub': 'אוצר המוזיקה החכם',
        'name': 'השם שלך', 'genre': 'בחר ז\'אנר', 'vibe': 'מה הוויב?', 'btn': 'תביא לי מוזיקה ⚡',
        'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ", "אלקטרוני"],
        'vibes': ["מסיבה", "רגוע", "אימון", "ריכוז"]
    },
    'RU': {
        'title': 'VIBELAB', 'sub': 'Твой музыкальный гид',
        'name': 'Имя', 'genre': 'Жанр', 'vibe': 'Вайб', 'btn': 'ИГРАТЬ ⚡',
        'genres': ["Russian Pop", "Russian Rock", "Hip Hop", "Techno"],
        'vibes': ["Вечеринка", "Релакс", "Спорт", "Фокус"]
    },
    'AR': {
        'title': 'VIBELAB', 'sub': 'تجربة الموسيقى الذكية',
        'name': 'الاسم', 'genre': 'النوع', 'vibe': 'الجو', 'btn': 'ابدأ ⚡',
        'genres': ["Arabic Pop", "Mahraganat", "Classic", "Hip Hop"],
        'vibes': ["حفلة", "استرخاء", "رياضة", "تركيز"]
    }
}

# --- 3. עיצוב חסין ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .main-title { color: #1DB954; font-size: 55px; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .stButton>button { background-color: #1DB954 !important; color: white !important; font-weight: bold; width: 100%; border-radius: 12px; height: 50px; }
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
# בורר שפה
c_lang = st.columns(4)
langs = [("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]
for i, (label, code) in enumerate(langs):
    if c_lang[i].button(label):
        st.session_state.lang = code
        st.rerun()

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:gray;'>{L['sub']}</p>", unsafe_allow_html=True)

# פאנל קלט אוטומטי
u_name = st.text_input(L['name'], placeholder="...")
col1, col2 = st.columns(2)
with col1:
    u_genre = st.selectbox(L['genre'], L['genres'])
with col2:
    u_vibe = st.selectbox(L['vibe'], L['vibes'])

if st.button(L['btn']):
    if not u_name:
        st.error("Please enter a name")
    elif not sp:
        st.error("Spotify connection failed")
    else:
        with st.spinner('Curating your playlist...'):
            try:
                # חיפוש חכם שמשלב ז'אנר ווייב
                query = f"{u_genre} {u_vibe}"
                res = sp.search(q=query, limit=12, type='track')
                
                if res and res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
                else:
                    st.warning("No results found. Try another combination.")
            except:
                st.error("Spotify is busy. Try again in 5 seconds.")

# --- 6. תצוגת תוצאות ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s {u_vibe} Mix:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:12px; margin-bottom:8px; display:flex; align-items:center; gap:15px; border-left:4px solid #1DB954;">
            <img src="{t['album']['images'][0]['url']}" width="55" style="border-radius:8px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold;">{t['name']}</div>
                <div style="color:#1DB954; font-size:0.8rem;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold; font-size:0.9rem;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
