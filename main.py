import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# הגדרות דף פרימיום
st.set_page_config(page_title="VibeLab Ultra", page_icon="⚡", layout="wide")

# אתחול זיכרון (Session State) למניעת קריסות
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []

# פיצ'ר רקע מתחלף: בוחר תמונה מקצועית אחרת בכל Refresh
bg_images = [
    "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=1920", # אולפן
    "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=1920", # תקליטן
    "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920", # הופעה
    "https://images.unsplash.com/photo-1514525253361-bee8718a74a2?q=80&w=1920"  # מועדון
]
selected_bg = random.choice(bg_images)

# עיצוב CSS מתקדם - דגש על קריאות ויוקרה
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&family=Montserrat:wght@900&display=swap" rel="stylesheet">
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), url('{selected_bg}');
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* כותרת VIBELAB ענקית ומעוצבת */
    .hero-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 90px;
        text-align: center;
        background: linear-gradient(to right, #1DB954, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: -3px;
    }}

    /* טקסטים של השאלות - בולטים מאוד */
    label {{
        font-family: 'Assistant', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        background: rgba(29, 185, 84, 0.2);
        padding: 5px 15px;
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 10px !important;
    }}

    /* עיצוב שדות הקלט */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: white !important;
        color: black !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        border: 3px solid #1DB954 !important;
        border-radius: 15px !important;
    }}

    /* כרטיסיות שירים מקצועיות */
    .track-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: 0.3s;
    }}
    .track-card:hover {{
        border-color: #1DB954;
        transform: translateY(-5px);
    }}

    /* כפתור יצירה */
    .stButton>button {{
        background: #1DB954 !important;
        color: black !important;
        font-weight: 900 !important;
        width: 100%;
        border-radius: 50px !important;
        padding: 20px !important;
        font-size: 1.4rem !important;
        border: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# פונקציית התחברות בטוחה (מונעת את השגיאה שקיבלת)
def get_spotify_client():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=csec)
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception:
        return None

sp = get_spotify_client()

# --- גוף האתר ---

st.markdown('<h1 class="hero-title">VIBELAB</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.2rem; opacity:0.8;">הופכים כל רגע לפסקול מושלם</p>', unsafe_allow_html=True)

# סרגל צד להיסטוריה (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='color:#1DB954;'>🕒 היסטוריה</h2>", unsafe_allow_html=True)
    for i, item in enumerate(reversed(st.session_state.playlist_history)):
        if st.button(f"🎵 {item['genre']} - {item['vibe']}", key=f"h_{i}"):
            st.session_state.current_tracks = item['tracks']

# קלט מהמשתמש
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    user_name = st.text_input("איך לקרוא לך?", "מנדי")
with c2:
    genre = st.selectbox("סגנון מוזיקלי", ["Rock", "Techno", "Pop", "Hip Hop", "Israeli", "Jazz", "Metal"])
with c3:
    vibe = st.selectbox("מה הוויב שלך כעת?", ["Party Mode", "Gym Flow", "Late Night", "Deep Chill", "Morning Energy"])

if st.button("Generate My Experience ⚡"):
    if not sp:
        st.error("שגיאה בחיבור לספוטיפיי. אנא בדוק את ה-Secrets ועשה Reboot.")
    else:
        with st.spinner('יוצרים את הקסם...'):
            try:
                results = sp.search(q=f"genre:{genre} {vibe}", limit=10, type='track')
                if results['tracks']['items']:
                    tracks = results['tracks']['items']
                    st.session_state.current_tracks = tracks
                    st.session_state.playlist_history.append({'genre': genre, 'vibe': vibe, 'tracks': tracks})
                    st.balloons()
                else:
                    st.warning("לא מצאנו שירים בדיוק לזה, נסה לשנות סגנון!")
            except Exception as e:
                st.error("ספוטיפיי עמוסה כרגע. נסה שוב בעוד דקה.")

# הצגת התוצאות
if st.session_state.current_tracks:
    st.markdown(f"### ✨ {user_name}, הנה מה שמצאנו עבורך:")
    for track in st.session_state.current_tracks:
        st.markdown(f"""
        <div class="track-card">
            <div style="display:flex; align-items:center; gap:20px;">
                <img src="{track['album']['images'][0]['url']}" width="100" style="border-radius:15px;">
                <div style="flex-grow:1;">
                    <div style="color:#1DB954; font-weight:800;">{track['artists'][0]['name']}</div>
                    <div style="font-size:1.5rem; font-weight:900;">{track['name']}</div>
                    <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; font-weight:bold; text-decoration:none;">PLAY FULL SONG ➜</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # נגן שמע בטוח (לא קורס אם אין דגימה)
        if track.get('preview_url'):
            st.audio(track['preview_url'])
