import os
import pickle
import webbrowser
from googleapiclient.discovery import build


class EmotionPredictor:
    def __init__(self):
        base_path = os.path.dirname(__file__)
        self.model_path = os.path.join(base_path, "emotion_for_playlist_model.sav")
        self.vectorizer_path = os.path.join(base_path, "vectorizer_for_playlist.sav")

        with open(self.model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)
        with open(self.vectorizer_path, 'rb') as vec_file:
            self.vectorizer = pickle.load(vec_file)

    def predict_emotion(self, text):
        vec_text = self.vectorizer.transform([text])
        predicted_emotion = self.model.predict(vec_text)
        return predicted_emotion[0]


class YouTubeRecommender:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.emotion_to_keywords = {
            "기쁨": "happy songs",
            "슬픔": "sad songs",
            "분노": "angry songs",
            "불안": "calming songs",
            "당황": "uplifting songs",
            "상처": "healing songs",
        }

    def search_youtube(self, query):
        request = self.youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=3
        )
        response = request.execute()
        videos = []
        for item in response["items"]:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            videos.append((title, f"https://www.youtube.com/watch?v={video_id}"))
        return videos

    def get_recommendations(self, emotion):
        if emotion not in self.emotion_to_keywords:
            return []
        query = self.emotion_to_keywords[emotion]
        return self.search_youtube(query)

