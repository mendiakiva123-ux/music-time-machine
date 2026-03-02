import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. הגדרות דף ---
st.set_page_config(page_title="VibeLab Elite", page_icon="🎧", layout="centered")

# --- 2. עיצוב (CSS) חסין ומקצועי ---
st.markdown(r"""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { color: #1DB954; font-size: 55px; font-weight: 900; text-align: center; margin-bottom: 20px;}
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

# --- 3. נתונים מורחבים ב-4 שפות ---
# ברירת מחדל אנגלית - הוספתי את כל הסגנונות שביקשת
DATA = {
    'EN': {
        'title': 'VIBELAB ELITE', 'name': 'Full Name', 'btn': 'GENERATE MIX ⚡', 
        'genres': ["Pop", "Rock", "Hip Hop", "Techno", "Metal", "Jazz", "R&B", "Electronic", "Lofi", "Country"], 
        'vibes': ["Party", "Chill", "Workout", "Focus", "Romantic", "Deep Focus"],
        'labels': {'genre': 'Select Genre', 'vibe': 'Select Vibe'}
    },
    'HE': {
        'title': 'VIBELAB', 'name': 'שם מלא', 'btn': 'צור חוויה ⚡', 
        'genres': ["מזרחית", "פופ", "רוק", "היפ הופ", "ישראלי", "טכנו", "מטאל", "ג'אז", "אלקטרוני", "ים תיכוני"], 
        'vibes': ["מסיבה", "רגוע", "אימון", "ריכוז", "רומנטי", "שבת"],
        'labels': {'genre': 'בחר ז'אנר', 'vibe': 'בחר אווירה'}
    },
    'RU': {
        'title': 'VIBELAB', 'name': 'Имя', 'btn': 'СОЗДАТЬ ⚡', 
        'genres': ["Pop", "Rock", "Hip Hop", "Metal", "Jazz", "Deep House", "Russian Pop"], 
        'vibes': ["Вечеринка", "Релакс", "Тренировка", "Фокус", "Романтика"],
        'labels': {'genre': 'Выберите жанр', 'vibe': 'Выберите вайб'}
    },
    'AR': {
        'title': 'VIBELAB', 'name': 'الاسم', 'btn': 'انطلق ⚡', 
        'genres': ["Arabic Pop", "Mahraganat", "Rock", "Tarab", "Hip Hop", "Techno"], 
        'vibes': ["حفلة", "استرخاء", "تمرین", "تركيز", "رومانسي"],
        'labels': {'genre': 'اختر النوع', 'vibe': 'اختر الأجواء'}
    }
}

# הגדרת ברירת מחדל לאנגלית
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 4. חיבור לספוטיפיי ---
def get_sp():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except Exception:
        st.error("Authentication Error: Check your Streamlit Secrets.")
        return None

# --- 5. ממשק משתמש דינמי ---
# כפתורי שפה בראש הדף
c_lang = st.columns(4)
langs = [("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]
for i, (label, code) in enumerate(langs):
    if c_lang[i].button(label):
        st.session_state.lang = code
        st.rerun()

L = DATA[st.session_state.lang]
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)

# קלטים שמשתנים לפי השפה
u_name = st.text_input(L['name'], placeholder="...")
c1, c2 = st.columns(2)
with c1: u_genre = st.selectbox(L['labels']['genre'], L['genres'])
with c2: u_vibe = st.selectbox(L['labels']['vibe'], L['vibes'])

# לוגיקת חיפוש חסינה
if st.button(L['btn']):
    if not u_name:
        st.warning("Please enter your name")
    else:
        sp = get_sp()
        if sp:
            with st.spinner('Loading...'):
                try:
                    # חיפוש משולב
                    query = f"{u_genre} {u_vibe}"
                    res = sp.search(q=query, limit=12, type='track')
                    
                    # אם לא נמצאו תוצאות בחיפוש המשולב, נחפש רק לפי ז'אנר (חסינות)
                    if not res['tracks']['items']:
                        res = sp.search(q=u_genre, limit=12, type='track')
                        
                    if res and res['tracks']['items']:
                        st.session_state.tracks = res['tracks']['items']
                        st.balloons()
                    else:
                        st.error("No results found. Try a different genre.")
                except Exception:
                    st.error("Search failed. Check your connection.")

# --- 6. תצוגת תוצאות ---
if st.session_state.tracks:
    st.markdown(f"### {u_name}'s Mix:")
    # כיוון טקסט (RTL/LTR)
    is_rtl = st.session_state.lang in ['HE', 'AR']
    alignment = "right" if is_rtl else "left"
    
    for t in st.session_state.tracks:
        img_url = t['album']['images'][0]['url'] if t['album']['images'] else ""
        
        st.markdown(f"""
        <div class="song-box" style="direction: {'rtl' if is_rtl else 'ltr'};">
            <img src="{img_url}" width="60" style="border-radius:10px;">
            <div style="flex-grow:1; text-align: {alignment};">
                <div style="font-weight:bold; font-size:16px;">{t['name']}</div>
                <div style="color:#1DB954; font-size:14px;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
