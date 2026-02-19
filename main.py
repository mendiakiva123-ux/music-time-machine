import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# הגדרות דף ועיצוב
st.set_page_config(page_title="Music Time Machine", page_icon="🎵", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1db954); color: white; }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border-radius: 20px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 15px; }
    .stButton>button { width: 100%; background: #1DB954 !important; color: white !important; border-radius: 50px !important; font-weight: bold !important; border: none !important; height: 50px; }
</style>
""", unsafe_allow_html=True)

# חיבור בטוח לספוטיפיי (עם Cache כדי שלא יקרוס)
@st.cache_resource
def get_spotify_conn():
    try:
        cid = st.secrets.get("CLIENT_ID")
        csec = st.secrets.get("CLIENT_SECRET")
        if not cid or not csec: return None
        auth_manager = SpotifyClientCredentials(client_id=cid.strip(), client_secret=csec.strip())
        return spotipy.Spotify(auth_manager=auth_manager)
    except:
        return None

sp = get_spotify_conn()

# פונקציית חיפוש מהירה עם Cache
@st.cache_data(show_spinner=False)
def search_songs_cached(birth_year, target_date, genre):
    results_list = []
    current_year = datetime.now().year
    
    # חיפוש שיר אחד לכל שנה
    for year in range(birth_year, current_year + 1):
        query = f"genre:{genre} year:{year}"
        try:
            search_results = sp.search(q=query, limit=20, type='track')
            for track in search_results['tracks']['items']:
                rel_date = track['album'].get('release_date', "")
                # בודק אם השיר שוחרר ביום ההולדת (חודש ויום)
                if rel_date.endswith(target_date):
                    results_list.append({
                        "year": year,
                        "name": track['name'],
                        "artist": track['artists'][0]['name'],
                        "image": track['album']['images'][0]['url'] if track['album']['images'] else "",
                        "url": track['external_urls']['spotify']
                    })
                    break
        except: continue
    return results_list

# ממשק המשתמש
st.title("🎸 Music Time Machine")

if sp is None:
    st.error("Missing Credentials! Please check your Streamlit Secrets.")
    st.stop()

with st.sidebar:
    st.header("הגדרות פסקול")
    user_name = st.text_input("הכנס שם", value="מנדי")
    dob = st.date_input("תאריך לידה", value=datetime(2004, 7, 25), min_value=datetime(1950, 1, 1))
    genre = st.selectbox("בחר ז'אנר", ['Pop', 'Rock', 'Hip Hop', 'Jazz', 'Electronic', 'Metal'])
    run_button = st.button("בנה לי פסקול! ✨")

if run_button:
    st.balloons()
    month_day = dob.strftime("-%m-%d") # פורמט של חודש-יום
    
    with st.spinner(f"סורק את ארכיון המוזיקה עבור {user_name}..."):
        final_results = search_songs_cached(dob.year, month_day, genre)
    
    if final_results:
        st.subheader(f"הנה השירים ששוחררו בימי ההולדת שלך מאז {dob.year}:")
        for s in final_results:
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="{s['image']}" width="80" style="border-radius: 10px;">
                    <div>
                        <h4 style="margin:0;">שנת {s['year']}: {s['name']}</h4>
                        <p style="margin:0; opacity:0.8;">אמן: {s['artist']}</p>
                        <a href="{s['url']}" target="_blank" style="color: #1DB954; text-decoration: none; font-weight: bold;">האזן בספוטיפיי 🎧</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("לא מצאנו שירים ששוחררו בדיוק ביום ובחודש האלו. נסה לבחור ז'אנר אחר (כמו Pop או Rock) שהם נפוצים יותר!")
