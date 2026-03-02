import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# --- 1. CONFIG & SESSION ---
st.set_page_config(page_title="VibeLab Elite", page_icon="🎧", layout="centered")

if 'lang' not in st.session_state: st.session_state.lang = 'HE'
if 'tracks' not in st.session_state: st.session_state.tracks = []

# --- 2. CLEAN & FAST UI ---
st.markdown(r"""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { color: #1DB954; font-size: 55px; font-weight: 900; text-align: center; margin-bottom: 0px;}
    .stButton>button { 
        background-color: #1DB954 !important; color: black !important; 
        font-weight: bold; border-radius: 12px; height: 50px; border: none;
    }
    .song-box { 
        background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; 
        margin-bottom: 10px; border-left: 5px solid #1DB954; display: flex; align-items: center; gap: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA ---
DATA = {
    'EN': {'title': 'VIBELAB', 'name': 'Full Name', 'btn': 'GENERATE ⚡', 'genres': ["Pop", "Hip Hop", "Rock"], 'vibes': ["Party", "Chill"]},
    'HE': {'title': 'VIBELAB', 'name': 'שם מלא', 'btn': 'צור חוויה ⚡', 'genres': ["מזרחית", "פופ", "היפ הופ"], 'vibes': ["מסיבה", "רגוע"]},
    'RU': {'title': 'VIBELAB', 'name': 'Имя', 'btn': 'СОЗДАТЬ ⚡', 'genres': ["Pop", "Rock"], 'vibes': ["Вечеринка", "Релакс"]},
    'AR': {'title': 'VIBELAB', 'name': 'الاسم', 'btn': 'انطلق ⚡', 'genres': ["Arabic Pop", "Mahraganat"], 'vibes': ["حفلة", "استرخاء"]}
}

# --- 4. SAFE CONNECTION ---
@st.cache_resource(show_spinner=False)
def get_sp():
    try:
        cid = st.secrets["CLIENT_ID"].strip()
        csec = st.secrets["CLIENT_SECRET"].strip()
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=csec))
    except: return None

sp = get_sp()

# --- 5. INTERFACE ---
c_lang = st.columns(4)
for i, (l, c) in enumerate([("🇺🇸 EN", "EN"), ("🇮🇱 HE", "HE"), ("🇷🇺 RU", "RU"), ("🇸🇦 AR", "AR")]):
    if c_lang[i].button(l):
        st.session_state.lang = c
        st.rerun()

L = DATA[st.session_state.lang]
st.markdown(f'<h1 class="main-title">{L["title"]}</h1>', unsafe_allow_html=True)

u_name = st.text_input(L['name'], placeholder="...")
c1, c2 = st.columns(2)
with c1: u_genre = st.selectbox("Genre", L['genres'])
with c2: u_vibe = st.selectbox("Vibe", L['vibes'])

# מנגנון חיפוש חסין תקיעות
if st.button(L['btn'], use_container_width=True):
    if not u_name:
        st.warning("Please enter your name")
    elif not sp:
        st.error("Check Spotify Credentials in Secrets")
    else:
        with st.spinner('Loading...'):
            try:
                # שימוש ב-search ישיר עם טיפול בשגיאות
                res = sp.search(q=f"{u_genre} {u_vibe}", limit=10, type='track')
                if res:
                    st.session_state.tracks = res['tracks']['items']
                    st.balloons()
            except Exception as e:
                st.error("Spotify is sleeping. Try again in 1 minute.")

# --- 6. RESULTS ---
if st.session_state.tracks:
    st.write(f"### {u_name}'s Mix:")
    for t in st.session_state.tracks:
        st.markdown(f"""
        <div class="song-box">
            <img src="{t['album']['images'][0]['url']}" width="55" style="border-radius:8px;">
            <div style="flex-grow:1;">
                <div style="font-weight:bold;">{t['name']}</div>
                <div style="color:#1DB954; font-size:13px;">{t['artists'][0]['name']}</div>
            </div>
            <a href="{t['external_urls']['spotify']}" target="_blank" style="color:#1DB954; text-decoration:none; font-weight:bold;">PLAY</a>
        </div>
        """, unsafe_allow_html=True)
