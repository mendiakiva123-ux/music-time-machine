import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# הגדרות דף ברמה הגבוהה ביותר
st.set_page_config(page_title="VibeLab | Personal Soundtrack", page_icon="🎧", layout="wide")

# אתחול Session State לשמירת היסטוריית פלייליסטים (כדי שלא ייעלמו)
if 'playlist_history' not in st.session_state:
    st.session_state.playlist_history = []
if 'current_tracks' not in st.session_state:
    st.session_state.current_tracks = []

# עיצוב CSS יוקרתי (Dark Mode, פונטים של גוגל, Glassmorphism)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700;800&display=swap" rel="stylesheet">
<style>
    * { font-family: 'Assistant', sans-serif; }
    .stApp {
        background: radial-gradient(circle at top right, #1e1e2e, #111119);
        color: #ffffff;
    }
    .glass-header {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 30px;
    }
    .track-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .track-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: scale(1.02);
        border-color: #1DB954;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1DB954, #19e68c);
        color: black !important;
        font-weight: 800;
        border-radius: 50px;
        padding: 15px 40px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(29, 185, 84, 0.4);
        transform: translateY(-2px);
    }
    .spotify-link {
        color: #1DB954 !important;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.9rem;
    }
    /* התאמתSidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# חיבור לספוטיפיי
@st.cache_resource
def connect_spotify():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))
    except:
        return None

sp = connect_spotify()

# סרגל צד - היסטוריית פלייליסטים
with st.sidebar:
    st.markdown("### 🕒 היסטוריית פלייליסטים")
    if st.session_state.playlist_history:
        for i, entry in enumerate(reversed(st.session_state.playlist_history)):
            if st.button(f"🎼 {entry['name']} - {entry['genre']}", key=f"hist_{i}"):
                st.session_state.current_tracks = entry['tracks']
    else:
        st.write("כאן יופיעו הפלייליסטים הקודמים שלך")

# תוכן ראשי
st.markdown('<div class="glass-header">', unsafe_allow_html=True)
st.markdown('<h1 style="font-size: 3.5rem; margin-bottom: 0;">VibeLab</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.2rem; opacity: 0.8;">הופכים את הרגש שלך למוזיקה</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# אזור הקלט
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    user_name = st.text_input("איך לקרוא לך?", placeholder="למשל: מנדי")
with col2:
    selected_genre = st.selectbox("סגנון מוזיקלי", 
                                ["Rock", "Techno", "Hip Hop", "Indie", "Israeli", "Classic Rock", "Jazz", "Metal", "Blues"])
with col3:
    selected_vibe = st.selectbox("מה האווירה?", 
                                ["Late Night", "Gym Flow", "Work Focus", "Party Mode", "Deep Chill", "Morning Vibes"])

if st.button("צור את החוויה שלי ✨"):
    if sp and user_name:
        with st.spinner('מזקקים את הצלילים המושלמים...'):
            q = f"genre:{selected_genre} {selected_vibe}"
            results = sp.search(q=q, limit=10, type='track')
            
            if results['tracks']['items']:
                st.session_state.current_tracks = results['tracks']['items']
                # שמירה להיסטוריה
                st.session_state.playlist_history.append({
                    'name': user_name,
                    'genre': selected_genre,
                    'tracks': results['tracks']['items']
                })
                st.balloons()
            else:
                st.error("לא מצאנו התאמה מדויקת, נסה לשנות מעט את הבחירה.")

# תצוגת התוצאות (נשמרת גם אחרי גלישה)
if st.session_state.current_tracks:
    st.markdown(f"### הפסקול הנוכחי שלך:")
    for track in st.session_state.current_tracks:
        with st.markdown(f'<div class="track-card">', unsafe_allow_html=True):
            c1, c2 = st.columns([1, 5])
            with c1:
                st.image(track['album']['images'][0]['url'], width=100)
            with c2:
                st.markdown(f"#### {track['name']}")
                st.markdown(f"**{track['artists'][0]['name']}**")
                st.markdown(f'<a href="{track["external_urls"]["spotify"]}" target="_blank" class="spotify-link">פתח בספוטיפיי ➜</a>', unsafe_allow_html=True)
                
                preview = track.get('preview_url')
                if preview:
                    st.audio(preview)
        st.markdown('</div>', unsafe_allow_html=True)
