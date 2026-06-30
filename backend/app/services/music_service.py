from app.models.schemas import Track
import logging

logger = logging.getLogger(__name__)

EMOTION_MUSIC_MAP = {
    "Happy": {
        "query": "happy upbeat hindi bollywood songs",
        "playlist_name": "Good Vibes Only ☀️",
    },
    "Sad": {
        "query": "sad emotional hindi bollywood songs",
        "playlist_name": "Dil Ka Dard 🌧️",
    },
    "Angry": {
        "query": "intense powerful energetic songs",
        "playlist_name": "Aag Laga Do 🔥",
    },
    "Fearful": {
        "query": "calm soothing peaceful hindi songs",
        "playlist_name": "Sukoon 🌿",
    },
    "Surprised": {
        "query": "exciting energetic bollywood songs",
        "playlist_name": "Surprise Twist! ⚡",
    },
    "Disgusted": {
        "query": "chill lo-fi relaxing hindi songs",
        "playlist_name": "Chill Karo 🎧",
    },
    "Neutral": {
        "query": "focus instrumental hindi background music",
        "playlist_name": "Apna Zone 🎵",
    },
}


async def get_tracks_for_emotion(emotion: str, limit: int = 10) -> tuple[list[Track], str]:
    config = EMOTION_MUSIC_MAP.get(emotion, EMOTION_MUSIC_MAP["Neutral"])
    playlist_name = config["playlist_name"]

    FALLBACK_TRACKS = {
        "Happy": [
            ("Badtameez Dil - Yeh Jawaani Hai Deewani", "Pritam", "II2EO3Fh1Zs"),
            ("Balam Pichkari - Yeh Jawaani Hai Deewani", "Pritam", "v-tSMQA44jg"),
            ("Gallan Goodiyaan - Dil Dhadakne Do", "Shankar Ehsaan Loy", "sKqrMpZIboo"),
            ("London Thumakda - Queen", "Amit Trivedi", "wZFkMWKkNAI"),
            ("Nagada Sang Dhol - Ram Leela", "Sanjay Leela Bhansali", "NqJGEaURgq8"),
            ("Ghungroo - War", "Vishal & Shekhar", "qFkNATtMO_A"),
            ("Zingaat - Dhadak", "Ajay-Atul", "nFMgRnT6ANk"),
            ("Kar Gayi Chull - Kapoor & Sons", "Amaal Mallik", "ZfMWLDIgBOY"),
            ("Saturday Saturday - Humpty Sharma Ki Dulhania", "Shahid Mallya", "eGABcm0CNZY"),
            ("Tamma Tamma Again - Badrinath Ki Dulhania", "Tanishk Bagchi", "9oJk_7RqfcE"),
        ],
        "Sad": [
            ("Tujhe Bhula Diya - Anjaana Anjaani", "Vishal-Shekhar", "Fmtmbp5HZXM"),
            ("Channa Mereya - Ae Dil Hai Mushkil", "Pritam", "bzMLCOpYoqs"),
            ("Agar Tum Saath Ho - Tamasha", "A.R. Rahman", "sKqrMpZIboo"),
            ("Kabira - Yeh Jawaani Hai Deewani", "Pritam", "8hy5GIFszuE"),
            ("Phir Le Aya Dil - Barfi", "Pritam", "1lhzGOxXMV0"),
            ("Tere Bina - Guru", "A.R. Rahman", "p0kjaHUzIng"),
            ("Main Dhoondne Ko Zamaane Mein - Heartless", "Arijit Singh", "cbDFcgXgmEY"),
            ("Arijit Singh Mashup - Sad Songs", "Arijit Singh", "pXTmg7LVTTU"),
            ("Hamari Adhuri Kahani - Title Track", "Jeet Gannguli", "l_MyUGq7pgs"),
            ("Sanam Re - Sanam Re", "Mithoon", "2AyFBmQ3lFw"),
        ],
        "Angry": [
            ("Sher Khul Gaye - Fighter", "Vishal-Shekhar", "zOkfGIToUBU"),
            ("Deva Deva - Brahmastra", "Pritam", "pPuEOJIGQmc"),
            ("War Anthem - War", "Vishal-Shekhar", "wKzkhFGuAJM"),
            ("Sultan Title Track", "Vishal-Shekhar", "ABXH3VUG47s"),
            ("Dangal Title Track", "Pritam", "0xyxtzD54rM"),
            ("Zinda - Bhaag Milkha Bhaag", "Shankar Ehsaan Loy", "1xqXXnBTFoM"),
            ("Bhaiyya Ji - Khel Khel Mein", "Various", "04F4xlWSFh0"),
            ("Rocky Title Track", "Various", "XAMQKaHCe0g"),
            ("Jai Ho - Dabangg", "Sajid-Wajid", "eVTXPUF4Oz4"),
            ("Policegiri - Policegiri", "Various", "kXYiU_JCYtU"),
        ],
        "Fearful": [
            ("Tera Yaar Hoon Main - Sonu Ke Titu Ki Sweety", "Rochak Kohli", "UfcAVejslrU"),
            ("Kun Faya Kun - Rockstar", "A.R. Rahman", "T94PHkCQBBQ"),
            ("Dil Dhadakne Do - Title Track", "Shankar Ehsaan Loy", "rOLx_2NKZHY"),
            ("Tu Hi Re - Bombay", "A.R. Rahman", "5l4JLOJ7IFk"),
            ("Roja Title Track", "A.R. Rahman", "bLHMQNVg_-o"),
            ("Luka Chuppi - Rang De Basanti", "A.R. Rahman", "HlQHANMgzfM"),
            ("O Paalanhaare - Lagaan", "A.R. Rahman", "b9nVkRbHVOA"),
            ("Yeh Jo Des Hai Tera - Swades", "A.R. Rahman", "7maJOI3QMu0"),
            ("Tere Bina - Guru", "A.R. Rahman", "hN_q-_nGv4U"),
            ("Dil Se Re - Dil Se", "A.R. Rahman", "TJ6Mzvh3XCc"),
        ],
        "Surprised": [
            ("Malhari - Bajirao Mastani", "Sanjay Leela Bhansali", "II2EO3Fh1Zs"),
            ("Tattad Tattad - Ram Leela", "Sanjay Leela Bhansali", "djV11Xbc914"),
            ("Jumme Ki Raat - Kick", "Himesh Reshammiya", "MmZexg8sxyk"),
            ("Lat Lag Gayee - Race 2", "Pritam", "a5uQMwRMHcs"),
            ("Desi Beat - Bodyguard", "Anu Malik", "5NV6Rdv1h3I"),
            ("Lungi Dance - Chennai Express", "Yo Yo Honey Singh", "4NRXx6pzkjw"),
            ("Party On My Mind - Race 2", "Pritam", "CZ_J8W9tMZM"),
            ("Disco Deewane - Student of the Year", "Vishal-Shekhar", "XXYlFuWEuKI"),
            ("Character Dheela - Ek Main Aur Ekk Tu", "Amit Trivedi", "umwAIGgCMDA"),
            ("Ainvayi Ainvayi - Band Baaja Baaraat", "Salim-Sulaiman", "xMV-vMGEPoc"),
        ],
        "Disgusted": [
            ("Safar - Jab Harry Met Sejal", "Pritam", "5qap5aO4i9A"),
            ("Ilahi - Yeh Jawaani Hai Deewani", "Pritam", "jfKfPfyJRdk"),
            ("Phir Bhi Tumko Chahunga - Half Girlfriend", "Mithoon", "umwAIGgCMDA"),
            ("Ae Dil Hai Mushkil - Title Track", "Pritam", "xMV-vMGEPoc"),
            ("Sooha Saaha - Highway", "A.R. Rahman", "a6ZuGMqaWCU"),
            ("Patakha Guddi - Highway", "A.R. Rahman", "bLHMQNVg_-o"),
            ("Nadaan Parindey - Rockstar", "A.R. Rahman", "HlQHANMgzfM"),
            ("Sadda Haq - Rockstar", "A.R. Rahman", "b9nVkRbHVOA"),
            ("Dooba Dooba Rehta Hoon - Silk Route", "Silk Route", "7SNGE7f86JI"),
            ("Tum Se Hi - Jab We Met", "Pritam", "ePbwxPBJgMg"),
        ],
        "Neutral": [
            ("Ik Vaari Aa - Raazi", "Shankar Ehsaan Loy", "tKi9Z-f6qX4"),
            ("Ae Watan - Raazi", "Shankar Ehsaan Loy", "xMV-vMGEPoc"),
            ("Kesariya - Brahmastra", "Pritam", "BddP6PYo2gs"),
            ("Raataan Lambiyan - Shershaah", "Tanishk Bagchi", "LXZT3OXOMH4"),
            ("Tere Jaisa Yaar Kahan - Yaarana", "R.D. Burman", "MQpWj_TlKaE"),
            ("Dost Dost Na Raha - Sangam", "Shankar Jaikishan", "8RmCHBDs_pk"),
            ("Zindagi Na Milegi Dobara - Title", "Shankar Ehsaan Loy", "TWcyIpul8OE"),
            ("Senorita - ZNMD", "Shankar Ehsaan Loy", "ssdgB-j6Gm0"),
            ("Khaabon Ke Parinday - ZNMD", "Shankar Ehsaan Loy", "m7ESJ4WNKCE"),
            ("Ik Junoon - ZNMD", "Shankar Ehsaan Loy", "hN_q-_nGv4U"),
        ],
    }

    song_list = FALLBACK_TRACKS.get(emotion, FALLBACK_TRACKS["Neutral"])

    tracks = []
    for i, (name, artist, video_id) in enumerate(song_list[:limit]):
        tracks.append(Track(
            id=video_id,
            name=name,
            artist=artist,
            album="YouTube Music",
            preview_url=None,
            spotify_url=f"https://www.youtube.com/watch?v={video_id}",
            image_url=f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
            duration_ms=210000,
        ))

    return tracks, playlist_name