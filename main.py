import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# --- הגדרות דף ---
st.set_page_config(page_title="Music Time Machine 2.0", page_icon="🚀", layout="wide")

# --- עיצוב CSS ---
st.markdown("""
<style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 50px; font-weight: 800; text-align: center; background: linear-gradient(90deg, #1DB954, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .song-card { background: #181818; border-radius: 15px; padding: 20px; border-left: 5px solid #1DB954; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- חיבור לספוטיפיי עם ניקוי שגיאות ---
@st.cache_resource
def get_spotify():
    try:
        cid = st.secrets.get("CLIENT_ID")
        csec = st.secrets.get("CLIENT_SECRET")
        
        if not cid or not csec:
            return None
            
        # .strip() מוחק רווחים מיותרים שגורמים לשגיאת ה-Oauth שקיבלת
        auth_manager = SpotifyClientCredentials(
            client_id=cid.strip(), 
            client_secret=csec.strip()
        )
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        st.error(f"שגיאת חיבור: {e}")
        return None

sp = get_spotify()

# --- פונקציית החיפוש ---
@st.cache_data(show_spinner=False)
def get_life_soundtrack(birth_year, genre):
    if not sp: return []
    current_year = datetime.now().year
    milestones = {0: "נולדת!", 6: "כיתה א'", 13: "בר מצווה", 17: "סיום תיכון"}
    
    soundtrack = []
    for age, event in milestones.items():
        year = birth_year + age
        if year > current_year: continue
        
        try:
            # הוספנו טיפול בשגיאות לכל חיפוש בנפרד
            query = f"genre:{genre} year:{year}"
            results = sp.search(q=query, limit=1, type='track')
            if results and results['tracks']['items']:
                track = results['tracks']['items'][0]
                soundtrack.append({
                    "age": age, "year": year, "event": event,
                    "name": track['name'], "artist": track['artists'][0]['name'],
                    "image": track['album']['images'][0]['url'],
                    "url": track['external_urls']['spotify'],
                    "preview": track.get('preview_url')
                })
        except:
            continue
    return soundtrack

# --- ממשק משתמש ---
st.markdown('<h1 class="main-title">🚀 Music Time Machine</h1>', unsafe_allow_html=True)

if sp is None:
    st.error("❌ שגיאת אימות! המפתחות ב-Secrets לא תקינים.")
    st.stop()

with st.sidebar:
    st.header("הגדרות")
    name = st.text_input("שם", value="מנדי")
    dob = st.date_input("תאריך לידה", value=datetime(2004, 7, 25))
    genre = st.selectbox("ז'אנר", ["Pop", "Rock", "Hip Hop", "Electronic"])
    btn = st.button("צא לדרך! ⚡")

if btn:
    tracks = get_life_soundtrack(dob.year, genre)
    if tracks:
        st.balloons()
        for t in tracks:
            st.markdown(f"""
            <div class="song-card">
                <h3 style="color:#1DB954;">גיל {t['age']} ({t['year']}) - {t['event']}</h3>
                <div style="display: flex; gap: 20px;">
                    <img src="{t['image']}" width="80" style="border-radius:10px;">
                    <div>
                        <p style="font-size:18px; margin:0;"><b>{t['name']}</b></p>
                        <p style="opacity:0.8;">{t['artist']}</p>
                        <a href="{t['url']}" target="_blank" style="color:#1DB954;">האזן בספוטיפיי</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if t['preview']:
                st.audio(t['preview'])
    else:
        st.warning("לא נמצאו שירים. נסה ז'אנר אחר!")
