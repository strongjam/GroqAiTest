import streamlit as st
from groq import Groq
import time
import re
import base64
from PIL import Image
from io import BytesIO
import requests

# 페이지 설정
st.set_page_config(page_title="Groq Playground", page_icon="🎮", layout="wide")

# API 키 설정
api_key = "your_groq_api_key_here"

# Groq 클라이언트 생성
client = Groq(api_key=api_key)

# API에서 사용 가능한 모델 목록 가져오기
@st.cache_data(ttl=3600)  # 1시간 캐싱
def get_available_models():
    """Groq API에서 사용 가능한 모델 목록 가져오기"""
    # 기본 모델 목록 (항상 표시)
    default_models = {
        "Llama 3.3 70B": "llama-3.3-70b-versatile",
        "Llama 3.1 70B": "llama-3.1-70b-versatile",
        "Llama 3.1 8B": "llama-3.1-8b-instant",
        "Mixtral 8x7B": "mixtral-8x7b-32768",
        "Llama 3.2 90B Vision": "llama-3.2-90b-vision-preview",
        "Llama 3.2 11B Vision": "llama-3.2-11b-vision-preview",
    }

    try:
        url = "https://api.groq.com/openai/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            models_data = response.json()
            api_models = {}

            for model in models_data.get("data", []):
                model_id = model.get("id", "")

                # TTS, Whisper, Guard 모델 제외 (채팅 API 미지원)
                skip_keywords = ["tts", "whisper", "guard", "safeguard"]
                if any(keyword in model_id.lower() for keyword in skip_keywords):
                    continue

                # 사용자 친화적인 이름 생성
                if "llama-3.3-70b" in model_id:
                    display_name = "Llama 3.3 70B"
                elif "llama-3.1-70b" in model_id:
                    display_name = "Llama 3.1 70B"
                elif "llama-3.1-8b" in model_id:
                    display_name = "Llama 3.1 8B"
                elif "mixtral-8x7b" in model_id:
                    display_name = "Mixtral 8x7B"
                elif "llama-3.2-90b-vision" in model_id:
                    display_name = "Llama 3.2 90B Vision"
                elif "llama-3.2-11b-vision" in model_id:
                    display_name = "Llama 3.2 11B Vision"
                elif "llama-4-maverick" in model_id:
                    display_name = "Llama 4 Maverick 17B"
                elif "llama-4-scout" in model_id:
                    display_name = "Llama 4 Scout 17B"
                elif "kimi-k2" in model_id:
                    display_name = "Kimi K2"
                elif "compound-mini" in model_id:
                    display_name = "Groq Compound Mini"
                elif "compound" in model_id and "mini" not in model_id:
                    display_name = "Groq Compound"
                elif "gpt-oss-120b" in model_id:
                    display_name = "GPT-OSS 120B"
                elif "gpt-oss-20b" in model_id:
                    display_name = "GPT-OSS 20B"
                elif "qwen3-32b" in model_id:
                    display_name = "Qwen 3 32B"
                elif "allam-2-7b" in model_id:
                    display_name = "Allam 2 7B"
                else:
                    # 기본 이름 생성
                    display_name = model_id.replace("/", " - ").replace("-", " ").title()

                api_models[display_name] = model_id

            # 기본 모델과 API 모델 병합 (API 모델이 우선)
            merged_models = {**default_models, **api_models}
            return merged_models
        else:
            return default_models
    except Exception as e:
        return default_models

# 사용 가능한 모델 목록
AVAILABLE_MODELS = get_available_models()

# 모델별 아이콘 (동적으로 생성)
def get_model_icon(model_name):
    """모델 이름에 따라 아이콘 반환"""
    if "Tts" in model_name or "TTS" in model_name:
        return "🔊"
    elif "Vision" in model_name:
        return "👁️"
    elif "Llama 4" in model_name:
        return "🦙✨"
    elif "Llama" in model_name:
        return "🦙"
    elif "Mixtral" in model_name:
        return "🌀"
    elif "Gemma" in model_name:
        return "💎"
    elif "Qwen" in model_name:
        return "🐉"
    elif "Kimi" in model_name:
        return "🌙"
    elif "Compound" in model_name:
        return "⚡"
    elif "GPT-OSS" in model_name:
        return "🔓"
    elif "Allam" in model_name:
        return "🌍"
    else:
        return "🤖"

# TTS 모델인지 확인하는 함수
def is_tts_model(model_name):
    """모델이 TTS 모델인지 확인"""
    return "tts" in model_name.lower()

# 기본 모델 아이콘 (캐싱용)
MODEL_ICONS = {model: get_model_icon(model) for model in AVAILABLE_MODELS.keys()}

# 모델별 설명 (기본 정보)
DEFAULT_MODEL_DESCRIPTIONS = {
    "Llama 3.3 70B": {
        "description": "Meta의 최신 대형 언어 모델",
        "strengths": "고품질 응답, 복잡한 추론, 창의적 작업",
        "best_for": "전문적인 질문, 긴 대화, 복잡한 문제 해결",
        "speed": "보통",
        "quality": "⭐⭐⭐⭐⭐"
    },
    "Llama 3.1 70B": {
        "description": "안정적이고 강력한 대형 모델",
        "strengths": "균형잡힌 성능, 신뢰성 높은 응답",
        "best_for": "일반적인 질문, 분석, 요약",
        "speed": "보통",
        "quality": "⭐⭐⭐⭐⭐"
    },
    "Llama 3.1 8B": {
        "description": "빠르고 효율적인 소형 모델",
        "strengths": "빠른 응답 속도, 낮은 지연시간",
        "best_for": "간단한 질문, 빠른 대화, 실시간 응답",
        "speed": "매우 빠름 ⚡",
        "quality": "⭐⭐⭐⭐"
    },
    "Mixtral 8x7B": {
        "description": "Mistral AI의 고성능 MoE 모델",
        "strengths": "다양한 작업 처리, 멀티태스킹",
        "best_for": "코딩, 기술 문서, 다국어 지원",
        "speed": "빠름",
        "quality": "⭐⭐⭐⭐⭐"
    },
    "Llama 3.2 90B Vision": {
        "description": "비전 기능이 있는 대형 멀티모달 모델",
        "strengths": "이미지 이해, 시각적 추론",
        "best_for": "이미지 분석, 시각적 질문 답변",
        "speed": "보통",
        "quality": "⭐⭐⭐⭐⭐"
    },
    "Llama 3.2 11B Vision": {
        "description": "빠른 비전 처리가 가능한 모델",
        "strengths": "빠른 이미지 처리, 효율적인 비전 작업",
        "best_for": "빠른 이미지 분석, 실시간 비전 작업",
        "speed": "빠름",
        "quality": "⭐⭐⭐⭐"
    }
}

def get_model_description(model_name):
    """모델 이름에 따라 설명 생성"""
    # 기본 설명이 있으면 반환
    if model_name in DEFAULT_MODEL_DESCRIPTIONS:
        return DEFAULT_MODEL_DESCRIPTIONS[model_name]

    # 동적으로 설명 생성
    model_lower = model_name.lower()

    # TTS 모델
    if "tts" in model_lower:
        return {
            "description": "텍스트를 음성으로 변환하는 TTS 모델",
            "strengths": "자연스러운 음성 생성, 다양한 목소리",
            "best_for": "텍스트 음성 변환, 오디오 생성",
            "speed": "빠름",
            "quality": "⭐⭐⭐⭐"
        }

    # Vision 모델
    elif "vision" in model_lower:
        return {
            "description": "멀티모달 비전 모델",
            "strengths": "이미지 이해, 시각적 분석",
            "best_for": "이미지 분석, 시각적 질문 답변",
            "speed": "보통",
            "quality": "⭐⭐⭐⭐"
        }

    # Llama 4 모델
    elif "llama 4" in model_lower or "llama-4" in model_lower:
        if "maverick" in model_lower:
            return {
                "description": "Meta의 Llama 4 Maverick 모델",
                "strengths": "최신 아키텍처, 향상된 추론 능력",
                "best_for": "복잡한 문제 해결, 전문적인 대화",
                "speed": "빠름",
                "quality": "⭐⭐⭐⭐⭐"
            }
        elif "scout" in model_lower:
            return {
                "description": "Meta의 Llama 4 Scout 모델",
                "strengths": "빠른 탐색, 효율적인 처리",
                "best_for": "빠른 질문 답변, 일반 대화",
                "speed": "매우 빠름 ⚡",
                "quality": "⭐⭐⭐⭐"
            }
    # Llama 모델
    elif "llama" in model_lower:
        if "70b" in model_lower or "90b" in model_lower:
            return {
                "description": "Meta의 대형 언어 모델",
                "strengths": "고품질 응답, 복잡한 추론",
                "best_for": "전문적인 질문, 복잡한 작업",
                "speed": "보통",
                "quality": "⭐⭐⭐⭐⭐"
            }
        else:
            return {
                "description": "Meta의 효율적인 언어 모델",
                "strengths": "빠른 응답, 효율적인 처리",
                "best_for": "일반적인 질문, 빠른 대화",
                "speed": "빠름",
                "quality": "⭐⭐⭐⭐"
            }

    # Mixtral 모델
    elif "mixtral" in model_lower:
        return {
            "description": "Mistral AI의 MoE 모델",
            "strengths": "다양한 작업, 코딩 지원",
            "best_for": "코딩, 기술 문서, 복잡한 작업",
            "speed": "빠름",
            "quality": "⭐⭐⭐⭐⭐"
        }

    # Gemma 모델
    elif "gemma" in model_lower:
        return {
            "description": "Google의 경량 언어 모델",
            "strengths": "효율적인 처리, 빠른 응답",
            "best_for": "일반 대화, 빠른 작업",
            "speed": "매우 빠름 ⚡",
            "quality": "⭐⭐⭐⭐"
        }

    # Qwen 모델
    elif "qwen" in model_lower:
        return {
            "description": "Alibaba의 다국어 언어 모델",
            "strengths": "다국어 지원, 다양한 작업",
            "best_for": "다국어 처리, 일반 작업",
            "speed": "보통",
            "quality": "⭐⭐⭐⭐"
        }

    # Kimi 모델
    elif "kimi" in model_lower:
        return {
            "description": "Moonshot AI의 장문맥 언어 모델",
            "strengths": "긴 문맥 이해, 복잡한 대화",
            "best_for": "긴 문서 분석, 복잡한 추론",
            "speed": "보통",
            "quality": "⭐⭐⭐⭐⭐"
        }

    # Groq Compound 모델
    elif "compound" in model_lower:
        return {
            "description": "Groq의 최적화된 언어 모델",
            "strengths": "초고속 추론, 효율적인 처리",
            "best_for": "빠른 응답, 실시간 대화",
            "speed": "초고속 ⚡⚡",
            "quality": "⭐⭐⭐⭐⭐"
        }

    # GPT-OSS 모델
    elif "gpt-oss" in model_lower:
        return {
            "description": "오픈소스 GPT 스타일 모델",
            "strengths": "강력한 언어 이해, 범용 작업",
            "best_for": "일반 대화, 다양한 작업",
            "speed": "보통",
            "quality": "⭐⭐⭐⭐⭐"
        }

    # Allam 모델
    elif "allam" in model_lower:
        return {
            "description": "IBM의 다국어 언어 모델",
            "strengths": "아랍어 지원, 다국어 처리",
            "best_for": "다국어 작업, 문화적 이해",
            "speed": "빠름",
            "quality": "⭐⭐⭐⭐"
        }

    # 기타 모델
    else:
        return {
            "description": "언어 모델",
            "strengths": "다양한 작업 처리",
            "best_for": "일반적인 질문, 대화",
            "speed": "보통",
            "quality": "⭐⭐⭐"
        }

# 모델 설명 딕셔너리 생성
MODEL_DESCRIPTIONS = {model: get_model_description(model) for model in AVAILABLE_MODELS.keys()}

# 중국어/일본어 한자 감지 및 제거 함수
def detect_and_clean_cjk(text):
    """중국어/일본어 한자를 감지하고 경고 표시"""
    cjk_pattern = re.compile(r'[\u4E00-\u9FFF\u3400-\u4DBF]')
    found_cjk = cjk_pattern.findall(text)

    if found_cjk:
        unique_chars = list(set(found_cjk))
        st.warning(f"⚠️ 응답에 중국어/일본어 한자가 포함되어 있습니다: {', '.join(unique_chars)}")
        cleaned_text = cjk_pattern.sub('?', text)
        return cleaned_text, True

    return text, False

# 이미지를 base64로 인코딩
def encode_image(image):
    """PIL Image를 base64 문자열로 변환"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Llama 3.3 70B"

if "disabled_models" not in st.session_state:
    st.session_state.disabled_models = set()

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 1024

# 제목
st.title("🎮 Groq Playground")
st.caption("AI 모델 테스트 및 실험 환경")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")

    st.subheader("🤖 모델 설정")

    # 단일 모델 선택
    available_models = [m for m in AVAILABLE_MODELS.keys() if m not in st.session_state.disabled_models]

    # 현재 선택된 모델이 비활성화되었으면 자동으로 첫 번째 사용 가능한 모델로 변경
    if available_models and st.session_state.selected_model not in available_models:
        st.session_state.selected_model = available_models[0]
        st.warning(f"⚠️ 이전에 선택한 모델이 비활성화되어 '{available_models[0]}'로 자동 전환되었습니다.")

    if available_models:
        selected_model = st.selectbox(
            "모델 선택",
            available_models,
            index=available_models.index(st.session_state.selected_model) if st.session_state.selected_model in available_models else 0,
            key="single_model_select"
        )
        st.session_state.selected_model = selected_model

        # 선택된 모델 정보 표시
        if selected_model in MODEL_DESCRIPTIONS:
            model_info = MODEL_DESCRIPTIONS[selected_model]
            with st.expander("ℹ️ 모델 정보", expanded=False):
                st.markdown(f"**{model_info['description']}**")
                st.markdown(f"**품질:** {model_info['quality']}")
                st.markdown(f"**속도:** {model_info['speed']}")
                st.markdown(f"**강점:** {model_info['strengths']}")
                st.markdown(f"**추천 용도:** {model_info['best_for']}")
    else:
        st.error("사용 가능한 모델이 없습니다!")

    st.markdown("---")

    # 온도 설정
    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state.temperature,
        step=0.1,
        help="낮을수록 일관성 있고, 높을수록 창의적인 응답"
    )

    # 최대 토큰
    st.session_state.max_tokens = st.slider(
        "Max Tokens",
        min_value=256,
        max_value=4096,
        value=st.session_state.max_tokens,
        step=256,
        help="응답의 최대 길이"
    )

    st.markdown("---")

    # 대화 초기화 버튼
    if st.button("🔄 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.subheader("📊 통계")
    st.metric("메시지 수", len(st.session_state.messages))
    st.metric("현재 모델", st.session_state.selected_model)
    st.metric("Temperature", f"{st.session_state.temperature:.1f}")

    # 모델 비교 가이드 (동적 생성)
    with st.expander("📋 모델 비교 가이드"):
        st.markdown("### 📚 전체 모델 목록")

        # 모든 모델을 카테고리별로 분류
        vision_models = []
        llama_large_models = []
        llama_small_models = []
        mixtral_models = []
        gemma_models = []
        qwen_models = []
        other_models = []

        for model_name in AVAILABLE_MODELS.keys():
            if "Vision" in model_name:
                vision_models.append(model_name)
            elif "Llama" in model_name:
                if "70b" in model_name.lower() or "90b" in model_name.lower() or "3.3" in model_name:
                    llama_large_models.append(model_name)
                else:
                    llama_small_models.append(model_name)
            elif "Mixtral" in model_name:
                mixtral_models.append(model_name)
            elif "Gemma" in model_name:
                gemma_models.append(model_name)
            elif "Qwen" in model_name:
                qwen_models.append(model_name)
            else:
                other_models.append(model_name)

        # 카테고리별 출력
        if llama_large_models:
            st.markdown("#### 🦙 Llama 대형 모델 (70B+)")
            for model in llama_large_models:
                desc = MODEL_DESCRIPTIONS.get(model, {})
                icon = get_model_icon(model)
                st.markdown(f"**{icon} {model}**")
                st.markdown(f"- {desc.get('description', '')}")
                st.markdown(f"- 품질: {desc.get('quality', '')} | 속도: {desc.get('speed', '')}")
                st.markdown(f"- 추천: {desc.get('best_for', '')}")
                st.markdown("")

        if llama_small_models:
            st.markdown("#### 🦙 Llama 소형/중형 모델")
            for model in llama_small_models:
                desc = MODEL_DESCRIPTIONS.get(model, {})
                icon = get_model_icon(model)
                st.markdown(f"**{icon} {model}**")
                st.markdown(f"- {desc.get('description', '')}")
                st.markdown(f"- 품질: {desc.get('quality', '')} | 속도: {desc.get('speed', '')}")
                st.markdown(f"- 추천: {desc.get('best_for', '')}")
                st.markdown("")

        if mixtral_models:
            st.markdown("#### 🌀 Mixtral 모델")
            for model in mixtral_models:
                desc = MODEL_DESCRIPTIONS.get(model, {})
                icon = get_model_icon(model)
                st.markdown(f"**{icon} {model}**")
                st.markdown(f"- {desc.get('description', '')}")
                st.markdown(f"- 품질: {desc.get('quality', '')} | 속도: {desc.get('speed', '')}")
                st.markdown(f"- 추천: {desc.get('best_for', '')}")
                st.markdown("")

        if vision_models:
            st.markdown("#### 👁️ Vision 모델 (이미지 분석)")
            for model in vision_models:
                desc = MODEL_DESCRIPTIONS.get(model, {})
                icon = get_model_icon(model)
                st.markdown(f"**{icon} {model}**")
                st.markdown(f"- {desc.get('description', '')}")
                st.markdown(f"- 품질: {desc.get('quality', '')} | 속도: {desc.get('speed', '')}")
                st.markdown(f"- 추천: {desc.get('best_for', '')}")
                st.markdown("")

        if gemma_models:
            st.markdown("#### 💎 Gemma 모델")
            for model in gemma_models:
                desc = MODEL_DESCRIPTIONS.get(model, {})
                icon = get_model_icon(model)
                st.markdown(f"**{icon} {model}**")
                st.markdown(f"- {desc.get('description', '')}")
                st.markdown(f"- 품질: {desc.get('quality', '')} | 속도: {desc.get('speed', '')}")
                st.markdown(f"- 추천: {desc.get('best_for', '')}")
                st.markdown("")

        if qwen_models:
            st.markdown("#### 🐉 Qwen 모델")
            for model in qwen_models:
                desc = MODEL_DESCRIPTIONS.get(model, {})
                icon = get_model_icon(model)
                st.markdown(f"**{icon} {model}**")
                st.markdown(f"- {desc.get('description', '')}")
                st.markdown(f"- 품질: {desc.get('quality', '')} | 속도: {desc.get('speed', '')}")
                st.markdown(f"- 추천: {desc.get('best_for', '')}")
                st.markdown("")

        if other_models:
            st.markdown("#### 🤖 기타 모델")
            for model in other_models:
                desc = MODEL_DESCRIPTIONS.get(model, {})
                icon = get_model_icon(model)
                st.markdown(f"**{icon} {model}**")
                st.markdown(f"- {desc.get('description', '')}")
                st.markdown(f"- 품질: {desc.get('quality', '')} | 속도: {desc.get('speed', '')}")
                st.markdown(f"- 추천: {desc.get('best_for', '')}")
                st.markdown("")

        # 통계 정보
        st.markdown("---")
        st.markdown(f"**전체 모델 수:** {len(AVAILABLE_MODELS)}개")

        # 빠른 선택 가이드
        st.markdown("---")
        st.markdown("### 🎯 빠른 선택 가이드")

        # 용도별 추천
        fast_models = []
        quality_models = []
        coding_models = []

        for model_name in AVAILABLE_MODELS.keys():
            desc = MODEL_DESCRIPTIONS.get(model_name, {})
            speed = desc.get("speed", "")
            quality = desc.get("quality", "")

            if "빠름" in speed or "⚡" in speed:
                fast_models.append(model_name)
            if quality == "⭐⭐⭐⭐⭐":
                quality_models.append(model_name)
            if "Mixtral" in model_name or ("Llama" in model_name and ("70b" in model_name.lower() or "90b" in model_name.lower())):
                coding_models.append(model_name)

        if fast_models:
            st.markdown("**⚡ 속도 중요:** " + ", ".join(fast_models[:3]))
        if quality_models:
            st.markdown("**⭐ 품질 중요:** " + ", ".join(quality_models[:3]))
        if coding_models:
            st.markdown("**💻 코딩 작업:** " + ", ".join(coding_models[:3]))
        if vision_models:
            st.markdown("**🖼️ 이미지 분석:** " + ", ".join(vision_models[:2]))

    # 비활성화된 모델 정보
    if st.session_state.disabled_models:
        st.markdown("---")
        st.subheader("⚠️ 비활성화된 모델")
        for model in st.session_state.disabled_models:
            st.text(f"• {model}")

        if st.button("🔓 비활성화 모델 초기화", use_container_width=True):
            st.session_state.disabled_models = set()
            st.success("비활성화된 모델이 초기화되었습니다!")
            st.rerun()

    # 캐시 및 전체 초기화 버튼
    st.markdown("---")
    if st.button("🔄 캐시 및 모델 목록 새로고침", use_container_width=True):
        # 캐시 클리어
        st.cache_data.clear()
        # 비활성화 목록 초기화
        st.session_state.disabled_models = set()
        st.success("캐시가 클리어되고 모델 목록이 새로고침됩니다!")
        st.rerun()

# 메인 영역 - 채팅 인터페이스
st.markdown("---")

# 이미지 업로드 영역 - Vision 모델일 때만 표시
uploaded_file = None
if "Vision" in st.session_state.selected_model:
    uploaded_file = st.file_uploader(
        "📎 이미지 업로드 (선택사항)",
        type=["png", "jpg", "jpeg", "webp"],
        help="Vision 모델과 함께 이미지를 분석할 수 있습니다"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", width=300)

# 이전 메시지 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            if message.get("image"):
                st.image(message["image"], width=300)
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        icon = MODEL_ICONS.get(message.get("model_name"), "🤖")
        with st.chat_message("assistant", avatar=icon):
            if message.get("model_name"):
                st.markdown(f"**{message['model_name']}**")

            if message.get("content"):
                content = message["content"]
                cleaned_content, has_cjk = detect_and_clean_cjk(content)

                if has_cjk or message.get("has_cjk"):
                    st.warning("⚠️ 중국어/일본어 한자 포함")
                    st.markdown(cleaned_content)
                else:
                    st.markdown(content)

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 이미지가 있는 경우 함께 저장
    user_message = {"role": "user", "content": prompt}
    if uploaded_file:
        image = Image.open(uploaded_file)
        user_message["image"] = image

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        if uploaded_file:
            st.image(image, width=300)
        st.markdown(prompt)

    # 일반 채팅
    model_name = st.session_state.selected_model
    model_id = AVAILABLE_MODELS[model_name]
    icon = MODEL_ICONS.get(model_name, "🤖")

    with st.chat_message("assistant", avatar=icon):
        st.markdown(f"**{model_name}**")

        with st.spinner("생각 중..."):
            try:
                system_prompt = f"""You are {model_name} model.

CRITICAL RULES:
- ONLY use Korean (한국어) OR English
- NEVER use Chinese (汉字), Japanese (日本語), or other languages
- For Korean: Use ONLY Hangul (한글), NO Hanja (한자)
- Match the user's language (Korean question → Korean answer)"""

                # 이미지가 있고 Vision 모델인 경우
                is_vision_model = "Vision" in model_name

                if uploaded_file and is_vision_model:
                    # Vision 모델용 메시지 구성
                    image_base64 = encode_image(image)
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ]
                elif uploaded_file and not is_vision_model:
                    # Vision 모델이 아닌데 이미지가 업로드된 경우
                    st.warning("⚠️ 현재 모델은 이미지를 처리할 수 없습니다. Vision 모델을 선택해주세요.")
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt + " (참고: 이미지가 업로드되었지만 현재 모델은 이미지를 처리할 수 없습니다)"}
                    ]
                else:
                    # 텍스트만 있는 경우
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]

                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model=model_id,
                    temperature=st.session_state.temperature,
                    max_tokens=st.session_state.max_tokens,
                )

                response = chat_completion.choices[0].message.content
                cleaned_response, has_cjk = detect_and_clean_cjk(response)

                if has_cjk:
                    st.error("⚠️ 한자 감지됨")
                    st.markdown(cleaned_response)
                else:
                    st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "model_name": model_name,
                    "content": response,
                    "has_cjk": has_cjk
                })

            except Exception as e:
                error_msg = str(e)
                needs_rerun = False

                if "decommissioned" in error_msg:
                    st.error(f"⚠️ {model_name}는 지원 중단되었습니다.")
                    st.session_state.disabled_models.add(model_name)
                    needs_rerun = True
                elif "rate_limit" in error_msg.lower():
                    st.error(f"⚠️ 토큰 제한에 도달했습니다.")
                    st.session_state.disabled_models.add(model_name)
                    needs_rerun = True
                elif "model_terms_required" in error_msg or "terms acceptance" in error_msg.lower():
                    st.error(f"⚠️ {model_name}는 약관 동의가 필요합니다.")
                    st.info("ℹ️ Groq Console에서 약관에 동의하면 사용할 수 있습니다.")
                    st.session_state.disabled_models.add(model_name)
                    needs_rerun = True
                elif "does not support chat completions" in error_msg:
                    st.error(f"⚠️ {model_name}는 채팅을 지원하지 않는 모델입니다 (TTS/Audio 전용).")
                    st.session_state.disabled_models.add(model_name)
                    needs_rerun = True
                else:
                    st.error(f"오류: {error_msg}")

                # 모델이 비활성화되었으면 자동으로 다른 모델로 전환
                if needs_rerun:
                    available_models = [m for m in AVAILABLE_MODELS.keys() if m not in st.session_state.disabled_models]
                    if available_models:
                        st.session_state.selected_model = available_models[0]
                        st.info(f"ℹ️ 자동으로 '{available_models[0]}' 모델로 전환됩니다.")
                        # 마지막 메시지 제거 (오류 메시지는 저장하지 않음)
                        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                            st.session_state.messages.pop()
                        time.sleep(2)
                        st.rerun()
