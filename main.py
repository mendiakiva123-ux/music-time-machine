import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Global", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. MULTI-LANGUAGE & VIBE ENGINE ---
# המבנה עכשיו מחולק לפי שפה -> ז'אנר -> אווירה -> אמנים
DATA = {
    'EN': {
        'title': 'VIBELAB',
        'subtitle': 'SMART MUSIC EXPERIENCE',
        'name_label': 'Name',
        'genre_label': 'Genre',
        'vibe_label': 'What is your vibe?',
        'artist_label': 'Curated Artists',
        'btn': 'GENERATE VIBE ⚡',
        'vibes': ["Party Mode", "Chill & Relax", "Gym Energy"],
        'genres': {
            "Pop": {
                "Party Mode": ["Dua Lipa", "Justin Bieber", "Katy Perry"],
                "Chill & Relax": ["Billie Eilish", "Lana Del Rey", "Olivia Rodrigo"],
                "Gym Energy": ["The Weeknd", "Rihanna", "Ariana Grande"]
            },
            "Rock": {
                "Party Mode": ["Queen", "Bon Jovi", "AC/DC"],
                "Chill & Relax": ["Pink Floyd", "Radiohead", "Coldplay"],
                "Gym Energy": ["Linkin Park", "Imagine Dragons", "Foo Fighters"]
            }
        }
    },
    'HE': {
        'title': 'וייב-לאב',
        'subtitle': 'חווית מוזיקה חכמה',
        'name_label': 'שם',
        'genre_label': 'בחר ז\'אנר',
        'vibe_label': 'מה הוויב שלך?',
        'artist_label': 'אמנים מומלצים לוויב הזה',
        'btn': 'צור פלייליסט ⚡',
        'vibes': ["מסיבה וארנבי", "רגוע ורומנטי", "אנרגיה לחדר כושר"],
        'genres': {
            "מזרחית": {
                "מסיבה וארנבי": ["אייל גולן", "עומר אדם", "אושר כהן", "ליאור נרקיס"],
                "רגוע ורומנטי": ["ישי ריבו", "פאר טסי", "עדן חסון", "איתי לוי"],
                "אנרגיה לחדר כושר": ["סטטיק", "נס וסטילה", "שרק", "אושר כהן"]
            },
            "ישראלי": {
                "מסיבה וארנבי": ["נועה קירל", "אנה זק", "מרגי"],
                "רגוע ורומנטי": ["חנן בן ארי", "אביתר בנאי", "עידן רייכל"],
                "אנרגיה לחדר כושר": ["טונה", "רביד פלוטניק", "התקווה 6"]
            }
        }
    },
    'RU': {
        'title': 'VIBELAB',
        'subtitle': 'УМНЫЙ МУЗЫКАЛЬНЫЙ ОПЫТ',
        'name_label': 'Имя',
        'genre_label': 'Жанр',
        'vibe_label': 'Твое настроение?',
        'artist_label': 'Рекомендуемые артисты',
        'btn': 'СОЗДАТЬ ⚡',
        'vibes': ["Вечеринка", "Релакс", "Спорт"],
        'genres': {
            "Pop RU": {
                "Вечеринка": ["Zivert", "Artik & Asti", "Jony"],
                "Релакс": ["HammAli & Navai", "Мот"],
                "Спорт": ["Niletto", "Morgenshtern"]
            }
        }
    },
    'AR': {
        'title': 'VIBELAB',
        'subtitle': 'تجربة الموسيقى الذكية',
        'name_label': 'الاسم',
        'genre_label': 'النوع',
        'vibe_label': 'ما هو الجو؟',
        'artist_label': 'الفنانين المقترحين',
        'btn': 'انطلق ⚡',
        'vibes': ["حفلة", "استرخاء", "رياضة"],
        'genres': {
            "Arabic": {
                "حفلة": ["Amr Diab", "Mohamed Ramadan", "Saad Lamjarred"],
                "استرخاء": ["Sherine", "Fairuz", "Elissa"],
                "رياضة": ["Wegz", "Marwan Pablo"]
            }
        }
    }
}

# --- 3. UI DESIGN ---
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
    }}
    .main-title {{
        font-family: 'Inter', sans-serif;
        font-size: clamp(40px, 8vw, 65px);
        color: #1DB954;
        text-align: center;
        text-shadow: 0 0 20px rgba(29, 185, 84, 0.4);
        margin-bottom: 0px;
    }}
    .glass-box {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }}
    label {{ color: #1DB954 !important; font-weight: 900 !important; }}
</style>
""", unsafe_allow_html=True)

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

# --- 5. INTERFACE ---
# Language selection - Clean Buttons
st.write("")
lc1, lc2, lc3, lc4 = st.columns(4)
with lc1: 
    if st.button("🇺🇸 EN"): st.session_state.lang = 'EN'
with lc2: 
    if st.button("🇮🇱 HE"): st.session_state.lang = 'HE'
with lc3: 
    if st.button("🇷🇺 RU"): st.session_state.lang = 'RU'
with lc4: 
    if st.button("🇸🇦 AR"): st.session_state.lang = 'AR'

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color:#aaa;">{L["subtitle"]}</p>', unsafe_allow_html=True)

st.markdown('<div class="glass-box">', unsafe_allow_html=True)
u_name = st.text_input(L['name_label'], placeholder="...")

# פילטר 1: ז'אנר
u_genre = st.selectbox(L['genre_label'], list(L['genres'].keys()))

# פילטר 2: וויב (מותאם לזמרים)
u_vibe = st.selectbox(L['vibe_label'], list(L['genres'][u_genre].keys()))

# פילטר 3: זמרים (משתנה לפי הז'אנר והוויב שנבחרו!)
available_artists = L['genres'][u_genre][u_vibe]
u_artist = st.selectbox(L['artist_label'], available_artists)

if st.button(L['btn'], use_container_width=True):
    if not u_name:
        st.error("Enter Name")
    else:
        with st.spinner('Building...'):
            try:
                # חיפוש חכם בספוטיפיי לפי האמן הנבחר
                res = sp.search(q=f"artist:{u_artist}", limit=10, type='track')
                if res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
            except:
                st.error("Spotify is busy. Wait 5 seconds.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. RESULTS ---
if st.session_state.tracks:
    st.write(f"### For {u_name} | {u_vibe}:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.6); padding:12px; border-radius:15px; margin-bottom:10px; display:flex; align-items:center; gap:15px; border-left:4px solid #1DB954;">
            <img src="{t['album']['images'][0]['url']}" width="55" style="border-radius:8px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:1rem;">{t['name']}</div>
                <div style="color:#1DB954; font-size:0.8rem;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="background:#1DB954; color:white; padding:8px 12px; border-radius:50px; text-decoration:none; font-size:0.7rem; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
