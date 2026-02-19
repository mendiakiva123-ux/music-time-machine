import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# הגדרות עיצוב
st.set_page_config(page_title="My Life Soundtrack", page_icon="🎵", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b0d11; color: white; }
    .song-card { background: #1b1e23; border-radius: 15px; padding: 20px; margin-bottom: 15px; border: 1px solid #2d3239; }
    .year-label { color: #1DB954; font-weight: bold; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# פונקציית חיבור חסינה לשגיאות
@st.cache_resource
def init_sp():
    try:
        # שליפת המפתחות וניקוי רווחים אוטומטי
        cid = st.secrets.get("CLIENT_ID", "").strip()
        csec = st.secrets.get("CLIENT_SECRET", "").strip()
        
        if not cid or not csec:
            st.error("המפתחות חסרים ב-Secrets!")
            return None
            
        auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=csec)
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        st.error(f"שגיאת התחברות לספוטיפיי: {e}")
        return None

sp = init_sp()

st.title("🎵 הפסקול של החיים שלי")

# בדיקה שהחיבור עובד לפני שממשיכים
if sp:
    with st.sidebar:
        st.header("הגדרות המסע")
        name = st.text_input("שם", value="מנדי")
        birth_year = st.number_input("שנת לידה", min_value=1950, max_value=2026, value=2004)
        genre = st.selectbox("ז'אנר מועדף", ["Pop", "Rock", "Hip Hop", "Dance"])
        go = st.button("צא לדרך! ✨")

    if go:
        current_year = datetime.now().year
        st.balloons()
        st.subheader(f"👋 היי {name}, הנה הלהיטים שליוו אותך:")

        for year in range(birth_year, current_year + 1):
            age = year - birth_year
            query = f"year:{year} genre:{genre}"
            try:
                results = sp.search(q=query, limit=1, type='track')
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    st.markdown(f"""
                    <div class="song-card">
                        <span class="year-label">{year} (גיל {age})</span>
                        <div style="display: flex; align-items: center; gap: 20px; margin-top: 10px;">
                            <img src="{track['album']['images'][0]['url']}" width="70" style="border-radius: 8px;">
                            <div>
                                <h4 style="margin:0;">{track['name']}</h4>
                                <p style="margin:0; opacity:0.7;">{track['artists'][0]['name']}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if track['preview_url']:
                        st.audio(track['preview_url'])
            except Exception:
                continue
else:
    st.warning("המערכת מחכה להגדרת המפתחות ב-Streamlit Cloud.")
