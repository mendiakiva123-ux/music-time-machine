import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# הגדרות עיצוב מתקדמות
st.set_page_config(page_title="My Life Soundtrack", page_icon="🎵", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b0d11; color: white; }
    .song-card { background: #1b1e23; border-radius: 15px; padding: 20px; margin-bottom: 15px; border: 1px solid #2d3239; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .year-label { color: #1DB954; font-weight: bold; font-size: 1.3rem; border-bottom: 2px solid #1DB954; padding-bottom: 5px; }
    .artist-name { color: #b3b3b3; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# חיבור לספוטיפיי
@st.cache_resource
def init_sp():
    try:
        cid = st.secrets.get("CLIENT_ID", "").strip()
        csec = st.secrets.get("CLIENT_SECRET", "").strip()
        if not cid or not csec: return None
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))
    except: return None

sp = init_sp()

st.title("🎵 הפסקול של החיים שלי")

if not sp:
    st.error("Missing Credentials! Please check your Streamlit Secrets.")
    st.stop()

# סרגל צד
with st.sidebar:
    st.header("הגדרות")
    name = st.text_input("שם", value="מנדי")
    birth_year = st.number_input("שנת לידה", min_value=1950, max_value=2026, value=2004)
    genre = st.selectbox("ז'אנר", ["Pop", "Rock", "Hip Hop", "Dance", "Electronic"])
    go = st.button("צא לדרך! ✨")

# הצגת התוצאות
if go:
    current_year = datetime.now().year
    st.balloons()
    st.subheader(f"👋 היי {name}, הנה הלהיטים שליוו אותך מאז {birth_year}:")

    # לולאת שנים
    for year in range(birth_year, current_year + 1):
        # חיפוש להיטים מובילים לשנה ולז'אנר
        query = f"year:{year} genre:{genre}"
        try:
            results = sp.search(q=query, limit=5, type='track')
            if results['tracks']['items']:
                # לוקחים את השיר הכי פופולרי מהתוצאות
                track = results['tracks']['items'][0]
                age = year - birth_year
                
                with st.container():
                    st.markdown(f"""
                    <div class="song-card">
                        <div class="year-label">{year} - גיל {age}</div>
                        <div style="display: flex; align-items: center; gap: 20px; margin-top: 15px;">
                            <img src="{track['album']['images'][0]['url']}" width="100" style="border-radius: 10px;">
                            <div>
                                <h3 style="margin:0;">{track['name']}</h3>
                                <p class="artist-name">{track['artists'][0]['name']}</p>
                                <a href="{track['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">האזן בספוטיפיי 🎧</a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if track['preview_url']:
                        st.audio(track['preview_url'])
            else:
                st.write(f"🔍 לא נמצא שיר לשנת {year}")
        except:
            continue
