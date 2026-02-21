import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. הגדרות דף ---
st.set_page_config(page_title="VibeLab Global", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. מילון נתונים רב-לשוני ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'sub': 'Global AI Music Curator',
        'name': 'Your Name', 'genre': 'Genre', 'vibe': 'Vibe', 'art': 'Artist', 'btn': 'GET MUSIC ⚡',
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
        'title': 'VIBELAB', 'sub': 'אוצר המוזיקה הבינלאומי',
        'name': 'שם המשתמש', 'genre': 'ז\'אנר', 'vibe': 'אווירה', 'art': 'זמר/ת', 'btn': 'תביא לי מוזיקה ⚡',
        'genres': {
            "מזרחית": {
                "מסיבה": ["אייל גולן", "עומר אדם", "אושר כהן", "ליאור נרקיס"],
                "רגוע": ["פאר טסי", "ישי ריבו", "עדן חסון", "איתי לוי"],
                "כושר": ["סטטיק", "שרק", "נס וסטילה", "אושר כהן"]
            },
            "ישראלי/פופ": {
                "מסיבה": ["נועה קירל", "סטטיק", "אנה זק"],
                "רגוע": ["חנן בן ארי", "עידן רייכל", "אביתר בנאי"],
                "כושר": ["טונה", "רביד פלוטניק", "התקווה 6"]
            }
        }
    },
    'RU': {
        'title': 'VIBELAB', 'sub': 'Музыкальный гид',
        'name': 'Имя', 'genre': 'Жанр', 'vibe': 'Вайб', 'art': 'Артист', 'btn': 'ИГРАТЬ ⚡',
        'genres': {
            "Pop RU": {
                "Party": ["Zivert", "Artik & Asti", "Jony"],
                "Chill": ["HammAli & Navai", "Мот"],
                "Gym": ["Niletto", "Morgenshtern"]
            }
        }
    },
    'AR': {
        'title': 'VIBELAB', 'sub': 'تجربة الموسيقى الذكية',
        'name': 'الاسم', 'genre': 'النوع', 'vibe': 'الجو', 'art': 'الفنان', 'btn': 'ابدأ ⚡',
        'genres': {
            "Arabic": {
                "Party": ["Amr Diab", "Mohamed Ramadan", "Saad Lamjarred"],
                "Chill": ["Sherine", "Fairuz", "Elissa"],
                "Gym": ["Wegz", "Marwan Pablo"]
            }
        }
    }
}

# --- 3. עיצוב נקי (ללא מלבנים) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .main-title { color: #1DB954; font-size: 50px; font-weight: 900; text-align: center; }
    label { color: #1DB954 !important; font-weight: bold !important; }
    div.stButton > button { background-color: #1DB954 !important; color: white !important; width: 100%; border-radius: 10px; height: 50px; font-weight: bold; }
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
# כפתורי שפה בולטים
cols = st.columns(4)
langs = [("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]
for i, (label, code) in enumerate(langs):
    if cols[i].button(label): st.session_state.lang = code

L = DATA[st.session_state.lang]

st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:gray;'>{L['sub']}</p>", unsafe_allow_html=True)

# אזור הקלט - נקי וללא מסגרות שחורות
u_name = st.text_input(L['name'], placeholder="...")
c1, c2 = st.columns(2)
with c1:
    u_genre = st.selectbox(L['genre'], list(L['genres'].keys()))
with c2:
    u_vibe = st.selectbox(L['vibe'], list(L['genres'][u_genre].keys()))

u_artist = st.selectbox(L['art'], L['genres'][u_genre][u_vibe])

if st.button(L['btn']):
    if not u_name:
        st.error("Please enter your name")
    else:
        with st.spinner('Syncing...'):
            try:
                res = sp.search(q=f"artist:{u_artist}", limit=12, type='track')
                st.session_state.tracks = res['tracks']['items']
                st.balloons()
            except:
                st.error("Spotify is busy. Wait 10s.")

# --- 6. תצוגת תוצאות ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s Playlist:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:12px; margin-bottom:8px; display:flex; align-items:center; gap:15px; border-left:4px solid #1DB954;">
            <img src="{t['album']['images'][0]['url']}" width="50" style="border-radius:5px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold;">{t['name']}</div>
                <div style="color:#1DB954; font-size:0.8rem;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
