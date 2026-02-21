import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# הגדרות דף
st.set_page_config(page_title="VibeTune Pro", page_icon="🎵", layout="wide")

# עיצוב UI יוקרתי, בהיר וקריא
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1493225255756-d9584f8606e9?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        margin-top: 20px;
    }
    h1, h2, h3, p, label {
        color: #1a1a1a !important; /* טקסט כהה וברור */
        font-weight: bold !important;
    }
    .song-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 10px solid #1DB954;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .spotify-link {
        background-color: #1DB954;
        color: white !important;
        padding: 10px 20px;
        border-radius: 50px;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# פונקציית חיבור לספוטיפיי
@st.cache_resource
def init_spotify():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))
    except Exception as e:
        return None

sp = init_spotify()

# תוכן האתר בתוך מיכל בהיר
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; font-size: 50px;">🎶 VibeTune Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;">הפלייליסט המושלם מחכה לך כאן</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("איך לקרוא לך?", "מנדי")
    with col2:
        genre = st.selectbox("בחר סגנון מוזיקה", 
                            ["Rock", "Pop", "Hip Hop", "Metal", "Electronic", "Jazz", "R&B", "Israeli", "Classic"])
    with col3:
        mood = st.selectbox("מה הווייב שלך?", 
                           ["Energetic", "Relaxed", "Happy", "Dark", "Party", "Focus"])

    generate_btn = st.button("🚀 צור לי פלייליסט מקצועי")
    st.markdown('</div>', unsafe_allow_html=True)

if generate_btn:
    if sp:
        st.balloons()
        st.markdown(f"<h2 style='color: white !important; text-shadow: 2px 2px 4px #000;'>✨ הפלייליסט של {name}:</h2>", unsafe_allow_html=True)
        
        # בניית שאילתת חיפוש
        query = f"genre:{genre} {mood}"
        try:
            results = sp.search(q=query, limit=10, type='track')
            
            if results['tracks']['items']:
                for track in results['tracks']['items']:
                    # כרטיסיית שיר מעוצבת ובהירה
                    st.markdown(f"""
                    <div class="song-card">
                        <img src="{track['album']['images'][0]['url']}" width="100" style="border-radius: 8px;">
                        <div style="flex-grow: 1;">
                            <h3 style="margin:0;">{track['name']}</h3>
                            <p style="margin:0; color: #666 !important;">{track['artists'][0]['name']}</p>
                            <a href="{track['external_urls']['spotify']}" target="_blank" class="spotify-link">האזן בספוטיפיי 🎧</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # השמעת דגימה במידה וקיימת
                    if track.get('preview_url'):
                        st.audio(track['preview_url'])
            else:
                st.warning("לא מצאנו שירים שמתאימים בדיוק לשילוב הזה. נסה שילוב אחר!")
        except Exception as e:
            st.error("הייתה שגיאה בתקשורת עם ספוטיפיי. נסה שוב בעוד רגע.")
    else:
        st.error("חסרים מפתחות גישה (Secrets). וודא שהגדרת אותם ב-Streamlit.")
