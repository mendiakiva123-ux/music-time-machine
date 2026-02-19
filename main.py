import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# הגדרות דף
st.set_page_config(page_title="My Life Soundtrack", page_icon="🎵", layout="wide")

# עיצוב מודרני
st.markdown("""
<style>
    .stApp { background-color: #0b0d11; color: white; }
    .song-card { 
        background: #1b1e23; 
        border-radius: 15px; 
        padding: 20px; 
        margin-bottom: 15px;
        border: 1px solid #2d3239;
    }
    .year-label { color: #1DB954; font-weight: bold; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# חיבור לספוטיפיי
@st.cache_resource
def init_sp():
    cid = st.secrets.get("CLIENT_ID")
    csec = st.secrets.get("CLIENT_SECRET")
    if not cid or not csec: return None
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid.strip(), client_secret=csec.strip()))

sp = init_sp()

st.title("🎵 הפסקול של החיים שלי")

if not sp:
    st.error("Missing Credentials in Secrets!")
    st.stop()

# סרגל צד
with st.sidebar:
    st.header("הגדרות")
    name = st.text_input("איך קוראים לך?", value="מנדי")
    birth_year = st.number_input("שנת לידה", min_value=1950, max_value=2026, value=2004)
    genre = st.selectbox("ז'אנר מועדף", ["Pop", "Rock", "Hip Hop", "R&B", "Dance"])
    go = st.button("צא לדרך! ✨")

if go:
    current_year = datetime.now().year
    st.balloons()
    st.subheader(f"👋 היי {name}, הנה הלהיטים שליוו אותך בכל שנה:")

    # חיפוש לפי שנה (הרבה יותר קליל ונותן תוצאות תמיד)
    for year in range(birth_year, current_year + 1):
        age = year - birth_year
        # מחפשים את השיר הכי פופולרי בשנה הזו לפי ז'אנר
        query = f"year:{year} genre:{genre}"
        results = sp.search(q=query, limit=1, type='track')
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            with st.container():
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
                st.audio(track['preview_url']) if track['preview_url'] else st.caption("אין דגימת שמע - חפשו בספוטיפיי!")
