import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. הגדרות דף בסיסיות ---
st.set_page_config(page_title="VibeLab Global Ultra", page_icon="🎧", layout="centered")

# אתחול שפה (ברירת מחדל אנגלית)
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. מילון נתונים (אנגלית, עברית, רוסית, ערבית) ---
DATA = {
    'EN': {
        'title': 'VIBELAB',
        'subtitle': 'The Global AI Music Curator',
        'name': 'Your Name',
        'genre': 'Select Genre',
        'vibe': 'Current Vibe',
        'artist': 'Choose Artist',
        'btn': 'GET MY MUSIC ⚡',
        'genres': {
            "Pop/Rock": {
                "Party": ["Taylor Swift", "Queen", "Dua Lipa"],
                "Chill": ["Billie Eilish", "Coldplay", "Lana Del Rey"],
                "Gym": ["Linkin Park", "Imagine Dragons", "The Weeknd"]
            },
            "Hip Hop": {
                "Party": ["Drake", "Travis Scott", "Cardi B"],
                "Chill": ["Kendrick Lamar", "Post Malone", "J. Cole"],
                "Gym": ["Eminem", "Kanye West", "21 Savage"]
            }
        }
    },
    'HE': {
        'title': 'VIBELAB',
        'subtitle': 'אוצר המוזיקה הבינלאומי',
        'name': 'השם שלך',
        'genre': 'בחר ז\'אנר',
        'vibe': 'מה הוויב?',
        'artist': 'בחר זמר/ת',
        'btn': 'תביא לי מוזיקה ⚡',
        'genres': {
            "מזרחית": {
                "מסיבה": ["אייל גולן", "עומר אדם", "אושר כהן", "ליאור נרקיס"],
                "רגוע": ["ישי ריבו", "פאר טסי", "עדן חסון", "איתי לוי"],
                "כושר": ["שרק", "נס וסטילה", "אושר כהן"]
            },
            "ישראלי/פופ": {
                "מסיבה": ["נועה קירל", "סטטיק", "אנה זק"],
                "רגוע": ["חנן בן ארי", "עידן רייכל", "אביתר בנאי"],
                "כושר": ["טונה", "רביד פלוטניק", "התקווה 6"]
            }
        }
    },
    'RU': {
        'title': 'VIBELAB',
        'subtitle': 'Твой музыкальный гид',
        'name': 'Ваше имя',
        'genre': 'Жанр',
        'vibe': 'Настроение',
        'artist': 'Артист',
        'btn': 'ПОЕХАЛИ ⚡',
        'genres': {
            "Russian Pop": {
                "Вечеринка": ["Zivert", "Artik & Asti", "Jony"],
                "Релакс": ["HammAli & Navai", "Мот"],
                "Спорт": ["Niletto", "Morgenshtern"]
            }
        }
    },
    'AR': {
        'title': 'VIBELAB',
        'subtitle': 'تجربة الموسيقى الذكية',
        'name': 'الاسم',
        'genre': 'النوع',
        'vibe': 'الجو العام',
        'artist': 'الفنان',
        'btn': 'ابدأ الموسيقى ⚡',
        'genres': {
            "Arabic": {
                "حفلة": ["Amr Diab", "Mohamed Ramadan", "Saad Lamjarred"],
                "استرخاء": ["Sherine", "Fairuz", "Elissa"],
                "رياضة": ["Wegz", "Marwan Pablo"]
            }
        }
    }
}

# --- 3. עיצוב נקי ללא שגיאות (CSS) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), 
        url('https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=2000');
        background-size: cover;
    }
    .main-title {
        color: #1DB954; font-family: 'Inter', sans-serif; font-size: 60px;
        font-weight: 900; text-align: center; margin-bottom: 0px;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 30px; border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 20px;
    }
    label { color: #1DB954 !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. חיבור לספוטיפיי ---
@st.cache_resource
def connect_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = connect_spotify()

# --- 5. ממשק המשתמש ---
# כפתורי שפה בראש הדף
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🇺🇸 English"): st.session_state.lang = 'EN'
with c2: 
    if st.button("🇮🇱 עברית"): st.session_state.lang = 'HE'
with c3: 
    if st.button("🇷🇺 Russian"): st.session_state.lang = 'RU'
with c4: 
    if st.button("🇸🇦 Arabic"): st.session_state.lang = 'AR'

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color:#aaa;">{L["subtitle"]}</p>', unsafe_allow_html=True)

# פאנל בחירה
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    user_name = st.text_input(L['name'], placeholder="...")
    
    col_left, col_right = st.columns(2)
    with col_left:
        genre_choice = st.selectbox(L['genre'], list(L['genres'].keys()))
    with col_right:
        vibe_choice = st.selectbox(L['vibe'], list(L['genres'][genre_choice].keys()))
    
    artist_choice = st.selectbox(L['artist'], L['genres'][genre_choice][vibe_choice])
    
    if st.button(L['btn'], use_container_width=True):
        if not user_name:
            st.warning("Please enter your name")
        elif not sp:
            st.error("Spotify Connection Error")
        else:
            with st.spinner('Syncing...'):
                try:
                    res = sp.search(q=f"artist:{artist_choice}", limit=12, type='track')
                    if res and res['tracks']['items']:
                        st.session_state.tracks = res['tracks']['items']
                        st.balloons()
                except:
                    st.error("Spotify is overwhelmed. Please wait 10 seconds.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. תצוגת תוצאות ---
if st.session_state.tracks:
    st.write(f"### {user_name}'s Playlist ({vibe_choice})")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.6); padding:15px; border-radius:15px; margin-bottom:10px; display:flex; align-items:center; gap:15px; border-left:4px solid #1DB954;">
            <img src="{t['album']['images'][0]['url']}" width="60" style="border-radius:10px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold;">{t['name']}</div>
                <div style="color:#1DB954; font-size:0.8rem;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="background:#1DB954; color:white; padding:8px 15px; border-radius:50px; text-decoration:none; font-size:0.8rem; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
