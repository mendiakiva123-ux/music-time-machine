import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# הגדרות דף ועיצוב
st.set_page_config(page_title="AI Playlist Generator", page_icon="🎧", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { font-size: 45px; font-weight: 900; text-align: center; color: #1DB954; text-shadow: 2px 2px 10px rgba(29, 185, 84, 0.3); }
    .card { background: #1b1e23; border-radius: 15px; padding: 20px; border: 1px solid #333; margin-bottom: 10px; }
    .spotify-green { color: #1DB954; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# חיבור לספוטיפיי עם ניקוי מפתחות
@st.cache_resource
def init_spotify():
    try:
        cid = st.secrets["CLIENT_ID"].strip().replace('"', '')
        csec = st.secrets["CLIENT_SECRET"].strip().replace('"', '')
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))
    except Exception as e:
        st.error(f"שגיאת חיבור: {e}")
        return None

sp = init_spotify()

st.markdown('<h1 class="main-title">🎧 AI Playlist Generator</h1>', unsafe_allow_html=True)
st.write("<p style='text-align: center;'>ענה על כמה שאלות וניצור לך את הפלייליסט המושלם!</p>", unsafe_allow_html=True)

if not sp:
    st.warning("⚠️ המפתחות ב-Secrets לא מוגדרים נכון. וודא שאין רווחים מיותרים.")
    st.stop()

# שאלון למשתמש
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("איך קוראים לך?", "מנדי")
        year = st.slider("שנת לידה (בשביל הנוסטלגיה)", 1960, 2024, 2004)
    with col2:
        genre = st.selectbox("ז'אנר מועדף", ["Pop", "Rock", "Hip Hop", "Electronic", "Jazz", "Metal"])
        vibe = st.radio("מה הווייב שלך עכשיו?", ["אנרגטי ⚡", "רגוע ☕", "מסיבה 🎉", "עצוב 🌧️"])

if st.button("🚀 צור לי פלייליסט!"):
    st.balloons()
    st.subheader(f"🔥 הפלייליסט של {name}:")
    
    # הגדרת מילות חיפוש לפי הווייב
    vibe_map = {
        "אנרגטי ⚡": "workout upbeat",
        "רגוע ☕": "chill acoustic",
        "מסיבה 🎉": "party dance",
        "עצוב 🌧️": "sad deep"
    }
    
    query = f"genre:{genre} {vibe_map[vibe]}"
    
    try:
        # חיפוש של 10 שירים שמתאימים לז'אנר ולווייב
        results = sp.search(q=query, limit=10, type='track')
        
        if results['tracks']['items']:
            for track in results['tracks']['items']:
                with st.markdown(f'<div class="card">', unsafe_allow_html=True):
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        st.image(track['album']['images'][0]['url'], width=100)
                    with c2:
                        st.markdown(f"<span class='spotify-green'>שיר:</span> {track['name']}", unsafe_allow_html=True)
                        st.markdown(f"<span class='spotify-green'>אמן:</span> {track['artists'][0]['name']}", unsafe_allow_html=True)
                        if track['preview_url']:
                            st.audio(track['preview_url'])
                        st.markdown(f"[🔗 האזן בספוטיפיי]({track['external_urls']['spotify']})")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("לא מצאנו שירים שמתאימים לשילוב הזה. נסה לשנות ז'אנר!")
            
    except Exception as e:
        st.error(f"אירעה שגיאה במהלך יצירת הפלייליסט: {e}")
