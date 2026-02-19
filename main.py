import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st.set_page_config(page_title="Music Journey", layout="centered")

# פונקציית חיבור אולטרה-בטוחה
def connect_to_spotify():
    try:
        # שליפה וניקוי רווחים אגרסיבי
        cid = st.secrets["CLIENT_ID"].replace('"', '').replace("'", "").strip()
        csec = st.secrets["CLIENT_SECRET"].replace('"', '').replace("'", "").strip()
        
        auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=csec)
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        st.error(f"שגיאת הגדרות: {e}")
        return None

sp = connect_to_spotify()

st.title("🎵 פסקול אישי")

if sp:
    name = st.text_input("שם המשתמש:", "מנדי")
    year = st.number_input("שנת לידה:", 1950, 2026, 2004)
    
    if st.button("תביא לי שיר! ✨"):
        try:
            # חיפוש הכי פשוט שיש כדי לוודא שזה עובד
            results = sp.search(q=f"year:{year}", limit=1, type='track')
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                st.success(f"היי {name}, השיר שמצאנו משנת {year} הוא:")
                st.header(f"{track['name']} - {track['artists'][0]['name']}")
                st.image(track['album']['images'][0]['url'], width=300)
                if track['preview_url']:
                    st.audio(track['preview_url'])
            else:
                st.warning("לא מצאנו שיר לשנה הזו.")
        except Exception as e:
            st.error(f"החיבור הצליח אבל החיפוש נכשל: {e}")
else:
    st.warning("המערכת לא מצליחה להתחבר. בדוק את ה-Secrets שלך שוב.")
