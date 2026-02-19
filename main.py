import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import random

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Music Time Machine",
    page_icon="🎵",
    layout="wide"
)

# --- 2. LUXURY UI DESIGN (CSS) ---
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
    }
</style>
""", unsafe_allow_html=True)


# --- 3. SPOTIFY API CONNECTION ---
@st.cache_resource
def init_spotify():
    try:
        # Pulling credentials from Streamlit Secrets
        if "CLIENT_ID" not in st.secrets or "CLIENT_SECRET" not in st.secrets:
            return None

        client_id = st.secrets["b7e4ccf806ef4a2195d92cdfa30f9705"]
        client_secret = st.secrets["232f29ea99ea489d9d744e843ec8342a"]

        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception:
        return None


sp = init_spotify()


# --- 4. DATA FETCHING ---
def get_songs_for_birthday(birth_year, target_date_md, genre):
    if not sp: return []
    tracks_list = []
    current_year = datetime.now().year

    for year in range(birth_year, current_year + 1):
        query = f"genre:{genre} year:{year}"
        try:
            results = sp.search(q=query, limit=50, type='track')
            for track in results['tracks']['items']:
                release_date = track['album'].get('release_date', "")
                if release_date.endswith(target_date_md):
                    tracks_list.append({
                        "year": year,
                        "name": track['name'],
                        "artist": track['artists'][0]['name'],
                        "image": track['album']['images'][0]['url'] if track['album']['images'] else "",
                        "preview": track.get('preview_url'),
                        "url": track['external_urls']['spotify']
                    })
                    break
        except:
            continue
    return tracks_list


# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center;'>⚡ Music Time Machine</h1>", unsafe_allow_html=True)

if not sp:
    st.error("Missing Credentials! Please check your Streamlit Secrets.")
    st.stop()

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        user_name = st.text_input("Username", placeholder="Enter your name...")
    with col2:
        dob = st.date_input("Birthday", min_value=datetime(1950, 1, 1))
    with col3:
        genre = st.selectbox("Genre", ['Pop', 'Rock', 'Hip Hop', 'Electronic', 'Jazz', 'Metal'])

    if st.button("Generate Soundtrack ✨"):
        if user_name:
            st.balloons()
            target_md = dob.strftime("-%m-%d")
            with st.spinner("Travelling through time..."):
                results = get_songs_for_birthday(dob.year, target_md, genre)

            if results:
                st.subheader(f"Hey {user_name}, here is your life soundtrack:")
                for s in results:
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; align-items: center; gap: 20px;">
                            <img src="{s['image']}" width="90" style="border-radius: 12px;">
                            <div>
                                <h3 style="margin: 0;">{s['year']}: {s['name']}</h3>
                                <p style="margin: 0; opacity: 0.7;">By {s['artist']}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if s['preview']:
                        st.audio(s['preview'])
                    else:
                        st.info(f"🔗 [Listen on Spotify]({s['url']})")
            else:
                st.warning("No hits found for this specific date. Try another genre!")
    st.markdown('</div>', unsafe_allow_html=True)
