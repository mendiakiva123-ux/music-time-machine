import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import random

# --- הגדרות עמוד פרימיום ---
st.set_page_config(
    page_title="Music Time Machine | פס הקול של חייך",
    page_icon="🎸",
    layout="wide"
)

# --- עיצוב CSS ברמה הכי גבוהה בשוק (Glassmorphism & Neon) ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1db954);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1DB954, #191414) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 15px !important;
        font-weight: bold !important;
        border: none !important;
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)


# --- פונקציית התחברות עם CACHING לעמידה בעומס ---
@st.cache_resource
def get_spotify_client(client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)


# הכנס את המפתחות שלך כאן
CLIENT_ID = "b7e4ccf806ef4a2195d92cdfa30f9705"
CLIENT_SECRET = "232f29ea99ea489d9d744e843ec8342a"

sp = get_spotify_client(CLIENT_ID, CLIENT_SECRET)


# --- חיפוש שירים עם CACHING למניעת כפילויות ---
@st.cache_data(show_spinner=False)
def search_songs_by_date(birth_year, target_md, selected_genre):
    songs = []
    current_year = datetime.now().year
    for year in range(birth_year, current_year + 1):
        query = f"genre:{selected_genre} year:{year}"
        results = sp.search(q=query, limit=50, type='track')
        for track in results['tracks']['items']:
            release_date = track['album'].get('release_date', "")
            if release_date.endswith(target_md):
                songs.append({
                    "year": year,
                    "name": track['name'],
                    "artist": track['artists'][0]['name'],
                    "image": track['album']['images'][0]['url'] if track['album']['images'] else "",
                    "preview": track.get('preview_url'),
                    "url": track['external_urls']['spotify']
                })
                break
    return songs


# --- ממשק האתר ---
st.markdown("<h1 style='text-align: center;'>⚡ Music Time Machine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8;'>חוויה מוזיקלית אישית המבוססת על יום הלידה שלכם</p>",
            unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("שם המשתמש", placeholder="הכנס שם...")
    with c2:
        dob = st.date_input("תאריך לידה", min_value=datetime(1950, 1, 1), max_value=datetime.now())
    with c3:
        genre = st.selectbox("סגנון מוזיקלי", ['Pop', 'Rock', 'Hip Hop', 'Electronic', 'Jazz', 'Metal', 'R&B'])

    submit = st.button("צור את פס הקול שלי ✨")
    st.markdown('</div>', unsafe_allow_html=True)

if submit and name:
    st.balloons()
    target_md = dob.strftime("-%m-%d")
    results = search_songs_by_date(dob.year, target_md, genre)

    if results:
        for s in results:
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="{s['image']}" width="100" style="border-radius: 10px;">
                    <div>
                        <h3 style="margin:0;">{s['year']}: {s['name']}</h3>
                        <p style="margin:0; opacity:0.7;">{s['artist']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if s['preview']:
                st.audio(s['preview'])
            else:
                st.info(f"🔗 [האזנה מלאה בספוטיפיי]({s['url']})")
    else:
        st.warning("לא מצאנו שירים לתאריך המדויק הזה. נסה לשנות ז'אנר!")

# --- Sidebar AI (תיקון השגיאה) ---
st.sidebar.title("🤖 AI Insights")
if dob:
    # תיקון טווח השנים בשגיאה
    safe_end_year = max(dob.year, 2024)
    suggested_year = random.randint(dob.year, safe_end_year)
    st.sidebar.write(f"היי {name}, ה-AI מזהה שנת {suggested_year} כשנה משמעותית עבורך!")