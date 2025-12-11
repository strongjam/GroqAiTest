import os
from groq import Groq

# API 키 설정
api_key = "your_groq_api_key_here"

# Groq 클라이언트 생성
client = Groq(api_key=api_key)

# 간단한 채팅 완성 요청
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "안녕하세요! 간단한 인사말을 해주세요.",
        }
    ],
    model="llama-3.3-70b-versatile",  # Groq의 인기 모델
)

# 결과 출력
print("Groq API 응답:")
print(chat_completion.choices[0].message.content)
