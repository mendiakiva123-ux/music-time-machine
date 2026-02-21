import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# הגדרות דף מתקדמות
st.set_page_config(page_title="VibeTune AI", page_icon="🎵", layout="wide")

# עיצוב CSS יוקרתי ומקצועי (רקעים משתנים, צבעים חיים, כרטיסיות זכוכית)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.1);
    }
    .spotify-btn {
        background-color: #1DB954;
        color: white !important;
        text-decoration: none;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    .main-header {
        font-size: 60px;
        font-weight: 800;
        background: -webkit-linear-gradient(#1DB954, #19e68c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# חיבור בטוח לספוטיפיי
@st.cache_resource
def init_sp():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))
    except Exception as e:
        st.error("שגיאת חיבור לספוטיפיי - וודא שה-Secrets תקינים.")
        return None

sp = init_sp()

st.markdown('<h1 class="main-header">VibeTune AI</h1>', unsafe_allow_html=True)
st.write("<p style='text-align: center; font-size: 1.2rem;'>הדור הבא של יצירת הפלייליסטים האישיים</p>", unsafe_allow_html=True)

# ממשק משתמש משופר
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("איך קוראים לך?", "מנדי")
    with c2:
        genre = st.selectbox("ז'אנר מועדף", ["Pop", "Deep House", "Classic Rock", "Israeli", "Techno", "Hip Hop"])
    with c3:
        mood = st.select_slider("מה הווייב?", options=["Relaxed", "Chill", "Happy", "Energetic", "Pure Party"])
    go = st.button("🚀 צור פלייליסט חלומי")
    st.markdown('</div>', unsafe_allow_html=True)

if go:
    if not sp:
        st.stop()
        
    st.balloons()
    st.subheader(f"✨ {name}, הפסקול המדויק עבורך:")
    
    # חיפוש חכם
    query = f"genre:{genre} {mood}"
    try:
        results = sp.search(q=query, limit=12, type='track')
        
        if results['tracks']['items']:
            # יצירת גריד של כרטיסיות
            cols = st.columns(2)
            for idx, track in enumerate(results['tracks']['items']):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="glass-card" style="margin-bottom: 20px;">
                        <div style="display: flex; gap: 20px;">
                            <img src="{track['album']['images'][0]['url']}" width="120" style="border-radius: 12px;">
                            <div>
                                <h3 style="margin:0;">{track['name']}</h3>
                                <p style="color: #b3b3b3;">{track['artists'][0]['name']}</p>
                                <a href="{track['external_urls']['spotify']}" target="_blank" class="spotify-btn">Play on Spotify 🎧</a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # פתרון הבאג מהפעם הקודמת - בדיקה אם יש Preview
                    preview = track.get('preview_url')
                    if preview:
                        st.audio(preview)
        else:
            st.warning("לא נמצאו שירים לשילוב הזה, נסה ז'אנר אחר!")
            
    except Exception as e:
        st.error("הייתה תקלה קטנה בחיפוש, נסה שוב בעוד רגע.")
