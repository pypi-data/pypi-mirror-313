import pickle
import os

emoji = { 0: '😞', 1: '😊', 2: '😌', 3: '😠', 4: '😟', 5: '😵'}


def load_model_and_vectorizer():
    # 파일을 정대경로로 불러오면 에러가 나서 os를 이용해 동적으로 불러옴
    base_path = os.path.dirname(os.path.abspath(__file__))
    # 학습한 모델을 저장한 파일 불러오기
    model_path = 'pymood/emoji_model'
    model_path = os.path.join(base_path,'emoji_model')

    # 문자를 벡터화한 파일 불러오기
    vectorizer_path = 'pymood/text_vectorizer'
    vectorizer_path = os.path.join(base_path,'text_vectorizer')

    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    return model, vectorizer

# 이모티콘 예측 함수
def analysis_emotion(text):
    model, vectorizer = load_model_and_vectorizer()

    # 입력받은 text를 vectorize해서 text_vector에 저장
    text_vector = vectorizer.transform([text])

    # vectorized된 데이터를 바탕으로 감정분석
    # list에 하나의 이모티콘이 저장됨
    prediction = model.predict(text_vector)
    
    return emoji[prediction[0]]
