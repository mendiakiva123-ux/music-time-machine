import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# פונקציה לטעינת המפתחות בצורה בטוחה מה-Secrets
def get_spotify_conn():
    try:
        # בדיקה אם המפתחות קיימים ב-Secrets של Streamlit
        cid = st.secrets.get("CLIENT_ID")
        csec = st.secrets.get("CLIENT_SECRET")
        
        if not cid or not csec:
            return None
            
        auth_manager = SpotifyClientCredentials(client_id=cid.strip(), client_secret=csec.strip())
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        return None

# אתחול החיבור
sp = get_spotify_conn()

st.set_page_config(page_title="Music Time Machine", page_icon="🎵")
st.title("⚡ Music Time Machine")

# בדיקה אם המפתחות עובדים
if sp is None:
    st.error("Missing Credentials! Please check your Streamlit Secrets.")
    st.info("וודא שבתוך ה-Secrets רשום CLIENT_ID ו-CLIENT_SECRET באותיות גדולות.")
    st.stop()

# ממשק המשתמש
user_name = st.text_input("הכנס את שמך")
dob = st.date_input("מה תאריך הלידה שלך?", min_value=datetime(1950, 1, 1))
genre = st.selectbox("בחר ז'אנר מועדף", ['Pop', 'Rock', 'Hip Hop', 'Jazz', 'Electronic'])

if st.button("בנה לי פסקול! ✨"):
    if user_name:
        st.success(f"היי {user_name}! המכונה מתחילה לעבוד על התאריך {dob}...")
        # כאן המערכת תבצע את החיפוש (הקוד המלא ששלחתי לך קודם כולל את פונקציית החיפוש)
