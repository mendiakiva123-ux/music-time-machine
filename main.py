import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 1. SETUP ---
st.set_page_config(page_title="VibeLab", page_icon="🎧")

# אתחול שפה בזיכרון
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. DATA ---
DATA = {
    'EN': {
        'title': 'VIBELAB', 'name': 'Your Name', 'genre': 'Genre', 'vibe': 'Vibe', 'btn': 'GET MUSIC ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno"],
        'vibes': ["Party", "Chill", "Gym"]
    },
    'HE': {
        'title': 'VIBELAB', 'name': 'שם', 'genre': 'ז\'אנר', 'vibe': 'אווירה', 'btn': 'תביא מוזיקה ⚡',
        'genres': ["מזרחית", "ישראלי", "פופ", "היפ הופ"],
        'vibes': ["מסיבה", "רגוע", "כושר"]
    },
    'RU': {
        'title': 'VIBELAB', 'name': 'Имя', 'genre': 'Жанр', 'vibe': 'Вайб', 'btn': 'ИГРАТЬ ⚡',
        'genres': ["Pop", "Rock", "Hip Hop", "Techno"],
        'vibes': ["Вечеринка", "Релакс", "Спорт"]
    },
    'AR': {
        'title': 'VIBELAB', 'name': 'الاسم', 'genre': 'النوع', 'vibe': 'الجو', 'btn': 'ابدأ ⚡',
        'genres': ["Arabic Pop", "Classic", "Hip Hop"],
        'vibes': ["حفلة", "استرخاء", "رياضة"]
    }
}

# --- 3. SPOTIFY ---
@st.cache_resource
def get_spotify():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["CLIENT_ID"].strip(),
            client_secret=st.secrets["CLIENT_SECRET"].strip()
        ))
    except: return None

sp = get_spotify()

# --- 4. UI ---
# כפתורי שפה פשוטים (ללא עיצוב שביר)
c1, c2, c3, c4 = st.columns(4)
if c1.button("EN"): st.session_state.lang = 'EN'
if c2.button("HE"): st.session_state.lang = 'HE'
if c3.button("RU"): st.session_state.lang = 'RU'
if c4.button("AR"): st.session_state.lang = 'AR'

L = DATA[st.session_state.lang]

st.title(L['title'])

# טופס פשוט
u_name = st.text_input(L['name'])
u_genre = st.selectbox(L['genre'], L['genres'])
u_vibe = st.selectbox(L['vibe'], L['vibes'])

if st.button(L['btn']):
    if not u_name:
        st.error("Enter Name")
    elif not sp:
        st.error("Spotify Connection Failed")
    else:
        with st.spinner('Loading...'):
            try:
                # חיפוש ישיר
                query = f"{u_genre} {u_vibe}"
                res = sp.search(q=query, limit=12, type='track')
                st.session_state.tracks = res['tracks']['items']
                st.balloons()
            except:
                st.error("Too many requests. Wait 10 seconds.")

# --- 5. RESULTS ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s List:")
    for t in st.session_state.tracks:
        # הצגת שיר בצורה נקייה
        col_img, col_txt = st.columns([1, 4])
        with col_img:
            st.image(t['album']['images'][0]['url'], width=60)
        with col_txt:
            st.markdown(f"**{t['name']}** \n{t['artists'][0]['name']}")
            st.link_button("PLAY", t['external_urls']['spotify'])
        st.divider()
