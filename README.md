# Groq AI Test Playground

Groq API를 사용한 AI 모델 테스트 및 실험 환경입니다.

## 주요 기능

- 🤖 **다중 모델 지원**: Llama, Mixtral, Gemma, Qwen 등 다양한 AI 모델 선택 가능
- 👁️ **Vision 모델 지원**: 이미지 업로드 및 분석 기능
- 🎛️ **파라미터 조정**: Temperature, Max Tokens 등 실시간 조정
- 📊 **모델 비교 가이드**: 각 모델의 특징과 추천 용도 안내
- 🔄 **자동 모델 전환**: 오류 발생 시 자동으로 다른 모델로 전환
- 🌐 **CJK 문자 감지**: 한국어 응답에서 중국어/일본어 한자 자동 감지 및 제거

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/strongjam/GroqAiTest.git
cd GroqAiTest
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. API 키 설정
`chat_app.py` 파일에서 본인의 Groq API 키로 변경:
```python
api_key = "your_groq_api_key_here"
```

### 4. 실행
```bash
streamlit run chat_app.py
```

## 파일 구조

- `chat_app.py`: 메인 Streamlit 애플리케이션
- `test_groq.py`: Groq API 테스트 스크립트
- `requirements.txt`: 필요한 Python 패키지 목록

## 지원 모델

### Llama 모델
- **Llama 3.3 70B**: Meta의 최신 대형 언어 모델
- **Llama 3.1 70B**: 안정적이고 강력한 대형 모델
- **Llama 3.1 8B**: 빠르고 효율적인 소형 모델
- **Llama 3.2 90B Vision**: 이미지 분석이 가능한 대형 멀티모달 모델
- **Llama 3.2 11B Vision**: 빠른 이미지 분석 모델

### 기타 모델
- **Mixtral 8x7B**: Mistral AI의 고성능 MoE 모델
- **Gemma 모델**: Google의 경량 언어 모델
- **Qwen 모델**: Alibaba의 다국어 언어 모델

## 사용법

1. 좌측 사이드바에서 모델 선택
2. Temperature와 Max Tokens 조정
3. Vision 모델 선택 시 이미지 업로드 가능
4. 채팅창에 메시지 입력

## 기술 스택

- **Streamlit**: 웹 UI 프레임워크
- **Groq API**: AI 모델 API
- **Python**: 백엔드 언어
- **PIL (Pillow)**: 이미지 처리

## 라이선스

MIT License

## 기여

이슈와 풀 리퀘스트는 언제나 환영합니다!
