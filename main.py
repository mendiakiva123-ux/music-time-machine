import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. הגדרות דף ---
st.set_page_config(page_title="VibeLab Elite", page_icon="🎧", layout="centered")

# --- 2. עיצוב (CSS) ---
st.markdown(r"""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { color: #1DB954; font-size: 50px; font-weight: 900; text-align: center; }
    .stButton>button { 
        background-color: #1DB954 !important; color: black !important; 
        font-weight: bold; border-radius: 12px; height: 50px; border: none; width: 100%;
    }
    .song-box { 
        background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; 
        margin-bottom: 10px; border-left: 5px solid #1DB954; display: flex; align-items: center; gap: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. נתונים ושפות (Default: EN) ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'name': 'Full Name', 'btn': 'GENERATE ⚡', 
        'genres': ["Pop", "Hip Hop", "Rock", "Techno", "R&B", "Electronic", "Lofi"], 
        'vibes': ["Party", "Chill", "Workout", "Focus", "Romantic"]
    },
    'HE': {
        'title': 'VIBELAB', 'name': 'שם מלא', 'btn': 'צור חוויה ⚡', 
        'genres': ["מזרחית", "פופ", "היפ הופ", "ישראלי", "טכנו", "אלקטרוני", "ים תיכוני"], 
        'vibes': ["מסיבה", "רגוע", "אימון", "ריכוז", "רומנטי"]
    },
    'RU': {
        'title': 'VIBELAB', 'name': 'Имя', 'btn': 'СОЗДАТЬ ⚡', 
        'genres': ["Pop", "Rock", "Hip Hop", "Deep House", "Russian Pop"], 
        'vibes': ["Вечеринка", "Релакс", "Тренировка", "Фокус"]
    },
    'AR': {
        'title': 'VIBELAB', 'name': 'الاسم', 'btn': 'انطلق ⚡', 
        'genres': ["Arabic Pop", "Mahraganat", "Tarab", "Hip Hop"], 
        'vibes': ["حفلة", "استرخاء", "تمرین", "تركيز"]
    }
}

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 4. חיבור לספוטיפיי ---
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except Exception as e:
        st.error("Authentication Error: Check your Streamlit Secrets.")
        return None

# --- 5. ממשק משתמש ---
# בחירת שפה
c_lang = st.columns(4)
langs = [("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]
for i, (label, code) in enumerate(langs):
    if c_lang[i].button(label):
        st.session_state.lang = code
        st.rerun()

L = DATA[st.session_state.lang]
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)

# בחירות משתמש
u_name = st.text_input(L['name'], placeholder="...")
c1, c2 = st.columns(2)
with c1: u_genre = st.selectbox("Genre", L['genres'])
with c2: u_vibe = st.selectbox("Vibe", L['vibes'])

# לוגיקת חיפוש
if st.button(L['btn']):
    if not u_name:
        st.warning("Please enter your name")
    else:
        sp = get_sp()
        if sp:
            with st.spinner('Loading...'):
                try:
                    # חיפוש משולב ז'אנר ואווירה
                    query = f"{u_genre} {u_vibe}"
                    res = sp.search(q=query, limit=10, type='track')
                    if res and res['tracks']['items']:
                        st.session_state.tracks = res['tracks']['items']
                        st.balloons()
                    else:
                        st.error("No results found for this combination.")
                except Exception as e:
                    st.error("Spotify Search Error. Try again in a moment.")

# --- 6. תוצאות ---
if st.session_state.tracks:
    st.markdown(f"### {u_name}'s Mix:")
    for t in st.session_state.tracks:
        # בדיקה אם יש תמונה לאלבום (למניעת שגיאות תצוגה)
        img_url = t['album']['images'][0]['url'] if t['album']['images'] else ""
        
        st.markdown(f"""
        <div class="song-box">
            <img src="{img_url}" width="55" style="border-radius:8px;">
            <div style="flex-grow:1; {'text-align:right' if st.session_state.lang == 'HE' or st.session_state.lang == 'AR' else ''}">
                <div style="font-weight:bold;">{t['name']}</div>
                <div style="color:#1DB954; font-size:13px;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
