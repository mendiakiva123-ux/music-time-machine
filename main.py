import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import pandas as pd

# --- הגדרות דף ---
st.set_page_config(page_title="Music Time Machine 2.0", page_icon="🚀", layout="wide")

# --- עיצוב CSS מתקדם ---
st.markdown("""
<style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 50px; font-weight: 800; text-align: center; background: linear-gradient(90deg, #1DB954, #191414); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 30px; }
    .song-card { background: #181818; border-radius: 15px; padding: 20px; transition: 0.3s; border-left: 5px solid #1DB954; margin-bottom: 20px; }
    .song-card:hover { transform: scale(1.02); background: #282828; }
    .age-badge { background: #1DB954; color: black; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# --- חיבור לספוטיפיי ---
@st.cache_resource
def get_spotify():
    cid = st.secrets.get("CLIENT_ID")
    csec = st.secrets.get("CLIENT_SECRET")
    if not cid or not csec: return None
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))

sp = get_spotify()

# --- פונקציות עזר ---
@st.cache_data(show_spinner=False)
def get_life_soundtrack(birth_year, genre):
    current_year = datetime.now().year
    milestones = {
        0: "נולדת!",
        6: "עולה לכיתה א'",
        13: "בר/בת מצווה",
        17: "סיום תיכון",
        20: "תחילת החיים הבוגרים"
    }
    
    soundtrack = []
    for age, event in milestones.items():
        year = birth_year + age
        if year > current_year: continue
        
        # חיפוש הלהיט הכי גדול באותה שנה
        query = f"genre:{genre} year:{year}"
        results = sp.search(q=query, limit=1, type='track')
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            soundtrack.append({
                "age": age,
                "year": year,
                "event": event,
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "image": track['album']['images'][0]['url'],
                "preview": track['preview_url'],
                "url": track['external_urls']['spotify']
            })
    return soundtrack

# --- ממשק משתמש ---
st.markdown('<h1 class="main-title">🚀 Music Time Machine 2.0</h1>', unsafe_allow_html=True)

if not sp:
    st.error("מפתחות ספוטיפיי חסרים! בדוק את ה-Secrets.")
    st.stop()

# סרגל צד להזנת נתונים
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", width=50)
    st.header("הגדרות המסע")
    name = st.text_input("שם המטייל בזמן", value="מנדי")
    dob = st.date_input("תאריך לידה", value=datetime(2004, 7, 25))
    genre = st.selectbox("ז'אנר מועדף", ["Pop", "Rock", "Hip Hop", "Electronic", "Metal", "R&B"])
    btn = st.button("צא לדרך! ⚡")

if btn:
    st.balloons()
    st.subheader(f"👋 היי {name}, הנה התחנות המוזיקליות של החיים שלך:")
    
    with st.spinner("מתחבר ללוויין ספוטיפיי..."):
        tracks = get_life_soundtrack(dob.year, genre)
    
    if tracks:
        # תצוגת תוצאות במבנה של ציר זמן
        for t in tracks:
            with st.container():
                st.markdown(f"""
                <div class="song-card">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <img src="{t['image']}" width="100" style="border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                        <div style="flex-grow: 1;">
                            <span class="age-badge">גיל {t['age']} - {t['year']}</span>
                            <h3 style="margin: 10px 0 5px 0; color: #1DB954;">{t['event']}</h3>
                            <p style="font-size: 18px; margin: 0;"><b>{t['name']}</b> | {t['artist']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    if t['preview']:
                        st.audio(t['preview'])
                with col2:
                    st.markdown(f"[🎧 פתח בספוטיפיי המלא]({t['url']})")
                    
        # בונוס: סטטיסטיקה קטנה
        st.divider()
        st.info(f"💡 הידעת? בשנת {dob.year} הז'אנר {genre} היה אחראי על אלפי להיטים!")
    else:
        st.warning("לא מצאנו נתונים. נסה לשנות את הז'אנר.")
