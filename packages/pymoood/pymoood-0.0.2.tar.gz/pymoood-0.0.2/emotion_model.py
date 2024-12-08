import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

# 데이터 로드
file_path = '/mnt/data/emotion_emoji_dataset.csv'
data = pd.read_csv(file_path)

# 1. 텍스트 데이터 벡터화
vectorizer = TfidfVectorizer(max_features=5000)  # TF-IDF를 사용하여 텍스트 데이터를 수치화
X = vectorizer.fit_transform(data['지금 내 감정 서술'])

# 2. 이모지 데이터 인코딩
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(data['이모지'])

# 3. 학습/테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. MLPClassifier 모델 생성
mlp_model = MLPClassifier(hidden_layer_sizes=(64, 64), activation='relu', solver='adam', max_iter=500, random_state=42)

# 5. 모델 학습
print("Training the MLP model...")
mlp_model.fit(X_train, y_train)

# 6. 테스트 데이터로 예측 수행
y_pred = mlp_model.predict(X_test)

# 7. 성능 평가
accuracy = accuracy_score(y_test, y_pred)
classification = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

# 성능 평가 출력
print("\nMLP Model Accuracy:", accuracy)
print("\nClassification Report:\n", classification)

# 8. 모델 저장
model_path = '/mnt/data/emotion_emoji_mlp_model.sav'
vectorizer_path = '/mnt/data/emotion_emoji_vectorizer.pkl'
label_encoder_path = '/mnt/data/emotion_emoji_label_encoder.pkl'

# 모델과 관련 객체 저장
with open(model_path, 'wb') as f:
    pickle.dump(mlp_model, f)

with open(vectorizer_path, 'wb') as f:
    pickle.dump(vectorizer, f)

with open(label_encoder_path, 'wb') as f:
    pickle.dump(label_encoder, f)

print("모델 및 관련 객체들이 저장되었습니다.")