import os
import pickle


class EmotionPredict:
    def __init__(self, model_path=None, vectorizer_path=None, label_encoder_path=None):
        # 기본 경로 설정 (패키지 내부 경로 사용)
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.model_path = model_path or os.path.join(base_path, 'emotion_mlp_model.sav')
        self.vectorizer_path = vectorizer_path or os.path.join(base_path, 'emotion_vectorizer.pkl')
        self.label_encoder_path = label_encoder_path or os.path.join(base_path, 'emotion_label_encoder.pkl')

        # 파일 존재 여부 확인
        for path, name in [(self.model_path, "모델"), (self.vectorizer_path, "벡터라이저"), (self.label_encoder_path, "레이블 인코더")]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"{name} 파일이 존재하지 않습니다: {path}")

        # 모델, 벡터라이저, 레이블 인코더 로드
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        with open(self.vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(self.label_encoder_path, 'rb') as f:
            self.label_encoder = pickle.load(f)

    def predict(self, text: str) -> str:
        # 감정에 해당하는 이모티콘 매핑
        emotion_to_emoji = {
            "분노": "😡",
            "기쁨": "😊",
            "불안": "😰",
            "당황": "😳",
            "슬픔": "😢",
            "상처": "💔"
        }

        # 입력 텍스트 벡터화 및 감정 예측
        input_vector = self.vectorizer.transform([text])
        predicted_label = self.model.predict(input_vector)
        emotion = self.label_encoder.inverse_transform(predicted_label)[0]
        emoji = emotion_to_emoji.get(emotion, "❓")

        return f"예측된 감정: {emotion}, 이모티콘: {emoji}"




