import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. SETUP ---
st.set_page_config(page_title="VIBELAB", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'results' not in st.session_state: st.session_state.results = []

# --- 2. DATA ENGINE (Genres & Vibes Only) ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'sub': 'Global AI Curator',
        'name': 'Name', 'genre': 'Genre', 'vibe': 'Vibe', 'btn': 'GET THE VIBE ⚡',
        'genres': ["Pop", "Hip Hop", "Rock", "Techno", "Jazz", "Electronic"],
        'vibes': ["Party", "Chill", "Workout", "Focus"]
    },
    'HE': {
        'title': 'VIBELAB', 'sub': 'אוצר המוזיקה החכם',
        'name': 'שם', 'genre': 'ז\'אנר', 'vibe': 'אווירה', 'btn': 'צור חוויה ⚡',
        'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ", "אלקטרוני"],
        'vibes': ["מסיבה", "רגוע", "כושר", "ריכוז"]
    },
    'RU': {
        'title': 'VIBELAB', 'sub': 'Музыкальный гиד',
        'name': 'Имя', 'genre': 'Жанр', 'vibe': 'Вайб', 'btn': 'ИГРАТЬ ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno"],
        'vibes': ["Вечеринка", "Релакс", "Спорт", "Фокус"]
    },
    'AR': {
        'title': 'VIBELAB', 'sub': 'تجربة الموسيقى الذكية',
        'name': 'الاسم', 'genre': 'النوع', 'vibe': 'الجو', 'btn': 'ابدأ ⚡',
        'genres': ["Arabic Pop", "Mahraganat", "Classic", "Hip Hop"],
        'vibes': ["حفلة", "استرخاء", "رياضة", "تركيز"]
    }
}

# --- 3. CLEAN DESIGN (No Syntax Errors) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1 { color: #1DB954; text-align: center; font-size: 60px; font-weight: 900; margin-top: -50px; }
    .stButton>button { background-color: #1DB954 !important; color: white !important; font-weight: bold; border-radius: 10px; height: 55px; border: none; transition: 0.3s; }
    label { color: #1DB954 !important; font-weight: bold !important; }
    .result-card { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #1DB954; display: flex; align-items: center; gap: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 4. SPOTIFY CONNECTION ---
@st.cache_resource
def init_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = init_spotify()

# --- 5. UI ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("🇺🇸 EN"): st.session_state.lang = 'EN'
if c2.button("🇮🇱 HE"): st.session_state.lang = 'HE'
if c3.button("🇷🇺 RU"): st.session_state.lang = 'RU'
if c4.button("🇸🇦 AR"): st.session_state.lang = 'AR'

L = DATA[st.session_state.lang]

st.markdown(f"<h1>{L['title']}</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center; color:#888; margin-top:-20px;'>{L['sub']}</p>", unsafe_allow_html=True)

# Main Form
u_name = st.text_input(L['name'], placeholder="...")
col_l, col_r = st.columns(2)
with col_l:
    u_genre = st.selectbox(L['genre'], L['genres'])
with col_r:
    u_vibe = st.selectbox(L['vibe'], L['vibes'])

if st.button(L['btn'], use_container_width=True):
    if not u_name:
        st.error("Please enter your name")
    elif not sp:
        st.error("Connection Error")
    else:
        with st.spinner('Syncing with Spotify...'):
            try:
                # Search for Playlists (Faster & More Accurate)
                query = f"{u_genre} {u_vibe}"
                search_res = sp.search(q=query, limit=1, type='playlist')
                
                if search_res['playlists']['items']:
                    playlist_id = search_res['playlists']['items'][0]['id']
                    tracks = sp.playlist_tracks(playlist_id, limit=12)
                    st.session_state.results = tracks['items']
                    st.balloons()
                else:
                    # Fallback to direct track search
                    tracks = sp.search(q=query, limit=12, type='track')
                    st.session_state.results = [{'track': t} for t in tracks['tracks']['items']]
            except:
                st.error("Spotify is overwhelmed. Try again in 5 seconds.")

# --- 6. RESULTS ---
if st.session_state.results:
    st.write(f"### {u_name}, here is your {u_vibe} mix:")
    for item in st.session_state.results:
        t = item.get('track')
        if not t: continue
        st.markdown(f"""
        <div class="result-card">
            <img src="{t['album']['images'][0]['url']}" width="55" style="border-radius:8px;">
            <div style="flex-grow:1;">
                <div style="color:white; font-weight:bold; font-size:16px;">{t['name']}</div>
                <div style="color:#1DB954; font-size:13px;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="background:#1DB954; color:white; padding:8px 15px; border-radius:20px; text-decoration:none; font-size:12px; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
