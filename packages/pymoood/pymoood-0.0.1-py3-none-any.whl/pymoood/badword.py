
import re
import os

# 욕설을 필터링하는 함수
def filter_profanity(text):
    c_d = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(c_d, "badword_lsit.txt")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    
    # 욕설 목록 로드
    with open(file_path, "r", encoding="utf-8") as f:
        bad_words = [line.strip() for line in f.readlines()]

    for word in bad_words:
        # 해당 욕설을 '*'로 교체
        pattern = r'\b' + re.escape(word) + r'\b'
        text = re.sub(pattern, '*' * len(word), text, flags=re.IGNORECASE)
    
    return text

