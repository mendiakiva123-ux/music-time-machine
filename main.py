import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

# --- 1. CONFIG ---
st.set_page_config(page_title="VibeLab Global", page_icon="🌍", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. MULTI-LANGUAGE DICTIONARY ---
DATA = {
    'EN': {
        'title': 'VIBELAB',
        'subtitle': 'GLOBAL MUSIC EXPERIENCE',
        'name_label': 'Name',
        'genre_label': 'Select Genre',
        'artist_label': 'Top Artists',
        'btn': 'GENERATE VIBE ⚡',
        'genres': {
            "Pop": ["Taylor Swift", "The Weeknd", "Billie Eilish", "Justin Bieber"],
            "Rock": ["Queen", "Arctic Monkeys", "Linkin Park", "Imagine Dragons"],
            "Hip Hop": ["Drake", "Travis Scott", "Kendrick Lamar", "Kanye West"],
            "Techno": ["Charlotte de Witte", "Boris Brejcha", "Solomun"]
        }
    },
    'HE': {
        'title': 'וייב-לאב',
        'subtitle': 'חווית מוזיקה בינלאומית',
        'name_label': 'שם',
        'genre_label': 'בחר ז\'אנר',
        'artist_label': 'זמרים מובילים',
        'btn': 'צור פלייליסט ⚡',
        'genres': {
            "מזרחית": ["אייל גולן", "אושר כהן", "עומר אדם", "פאר טסי", "עדן חסון"],
            "פופ ישראלי": ["נועה קירל", "חנן בן ארי", "סטטיק", "אנה זק"],
            "רוק ישראלי": ["טונה", "רביד פלוטניק", "ברי סחרוף", "שלמה ארצי"]
        }
    },
    'RU': {
        'title': 'VIBELAB',
        'subtitle': 'МУЗЫКАЛЬНЫЙ ОПЫТ',
        'name_label': 'Имя',
        'genre_label': 'Жанр',
        'artist_label': 'Артисты',
        'btn': 'СОЗДАТЬ VIBE ⚡',
        'genres': {
            "Russian Pop": ["Zivert", "Jony", "Artik & Asti", "Niletto"],
            "Russian Rock": ["Би-2", "Кино", "ДДТ", "Ленинград"],
            "Hip Hop RU": ["Morgenshtern", "Scriptonite", "Oxxxymiron"]
        }
    },
    'AR': {
        'title': 'VIBELAB',
        'subtitle': 'تجربة الموسيقى العالمية',
        'name_label': 'الاسم',
        'genre_label': 'اختر النوع',
        'artist_label': 'الفنانين',
        'btn': 'انطلق ⚡',
        'genres': {
            "Arabic Pop": ["Amr Diab", "Nancy Ajram", "Elissa", "Mohamed Hamaki"],
            "Mahraganat": ["Hassan Shakosh", "Wegz", "Marwan Pablo"],
            "Classic Arabic": ["Fairuz", "Umm Kulthum", "Abdel Halim Hafez"]
        }
    }
}

# --- 3. PRO DESIGN (4K & CLEAN) ---
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
    }}
    .main-title {{
        font-family: 'Inter', sans-serif;
        font-size: 60px;
        font-weight: 900;
        color: #1DB954;
        text-align: center;
        text-shadow: 0 0 20px rgba(29, 185, 84, 0.4);
    }}
    .glass-box {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    label {{ color: #1DB954 !important; font-weight: bold !important; }}
</style>
""", unsafe_allow_html=True)

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

# --- 5. INTERFACE ---
# Language Selector Header
st.write("---")
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🇺🇸 English"): st.session_state.lang = 'EN'
with c2: 
    if st.button("🇮🇱 עברית"): st.session_state.lang = 'HE'
with c3: 
    if st.button("🇷🇺 Русский"): st.session_state.lang = 'RU'
with c4: 
    if st.button("🇸🇦 العربية"): st.session_state.lang = 'AR'

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color:#aaa;">{L["subtitle"]}</p>', unsafe_allow_html=True)

st.markdown('<div class="glass-box">', unsafe_allow_html=True)
u_name = st.text_input(L['name_label'], placeholder="...")
u_genre = st.selectbox(L['genre_label'], list(L['genres'].keys()))
u_artist = st.selectbox(L['artist_label'], L['genres'][u_genre])

if st.button(L['btn'], use_container_width=True):
    if not u_name:
        st.error("Name required!")
    else:
        with st.spinner('Fetching hits...'):
            try:
                res = sp.search(q=f"artist:{u_artist}", limit=10, type='track')
                if res['tracks']['items']:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
            except:
                st.error("Connection Error. Try again.")
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. DISPLAY RESULTS ---
if st.session_state.tracks:
    st.write(f"### Curated for {u_name}:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.6); padding:15px; border-radius:15px; margin-bottom:10px; display:flex; align-items:center; gap:15px; border-left:4px solid #1DB954;">
            <img src="{t['album']['images'][0]['url']}" width="60" style="border-radius:8px;">
            <div style="flex-grow:1;">
                <div style="color:#1DB954; font-size:0.8rem;">{t['artists'][0]['name']}</div>
                <div style="color:white; font-weight:bold;">{t['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="background:#1DB954; color:white; padding:8px 15px; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
