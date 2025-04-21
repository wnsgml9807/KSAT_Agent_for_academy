import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import logging
import os
import uuid
import requests
import json
import re
import time

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="KSAT 국어 출제용 AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 UI 구성
with st.sidebar:
    st.title("수능 독서 출제용 Agent")
    st.write("Version 0.2.0")

    st.info(
        """
        **제작자:** 권준희
        wnsgml9807@naver.com
        """
    )

    # 세션 초기화 버튼
    if st.button("🔄️ 세션 초기화"):
        # 세션 ID를 새로 생성
        st.session_state.session_id = f"session_{uuid.uuid4()}"
        logger.info(f"세션 ID 재생성: {st.session_state.session_id}")
        
        # Streamlit 세션 상태 초기화
        keys_to_clear = list(st.session_state.keys())
        for key in keys_to_clear:
            if key != "session_id":  # session_id는 방금 새로 설정했으므로 삭제하지 않음
                del st.session_state[key]
                
        st.success("세션이 초기화되었습니다. 페이지를 새로고침합니다.")
        time.sleep(1)
        st.rerun()


# --- 백엔드 URL 설정 ---
try:
    # Streamlit Cloud 환경변수 또는 로컬 환경변수
    FASTAPI_SERVER_URL = st.secrets.get("FASTAPI_SERVER_URL") or os.environ.get("FASTAPI_SERVER_URL")
    if not FASTAPI_SERVER_URL:
        FASTAPI_SERVER_URL = "http://127.0.0.1:8000"
except Exception:
    FASTAPI_SERVER_URL = "http://127.0.0.1:8000"

logger.info(f"백엔드 서버: {FASTAPI_SERVER_URL}")

# --- 세션 상태 초기화 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    logger.info("세션 상태에 'messages' 초기화")

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{uuid.uuid4()}"
    logger.info(f"새 세션 ID 생성: {st.session_state.session_id}")

# --- 저장된 메시지 표시 함수 ---
def render_message(message):
    """저장된 메시지를 타입에 따라 적절하게 렌더링하는 함수"""
    role = message.get("role", "unknown")
    content = message.get("content", "")
    
    # 사용자 메시지 표시
    if role == "user":
        with st.chat_message("user"):
            st.markdown(content)
        return
    
    # 어시스턴트 메시지 표시
    if role == "assistant":
        with st.container(border=False):
            # 플레이스홀더 50개 미리 생성 (스트리밍 로직과 일치)
            placeholders = [st.empty() for _ in range(50)]
            current_idx = 0
            
            # 문자열인 경우 처리
            if isinstance(content, str):
                try:
                    # JSON 파싱 시도
                    msg_data = json.loads(content)
                except (json.JSONDecodeError, TypeError):
                    # JSON 아닌 경우 그대로 표시 (에러 메시지 등)
                    st.markdown(content)
                    return
            else:
                # 이미 딕셔너리인 경우
                msg_data = content
            
            # messages 키가 있는 경우 (새 형식)
            if isinstance(msg_data, dict) and "messages" in msg_data:
                for item in msg_data["messages"]:
                    item_type = item.get("type", "")
                    
                    if item_type == "text":
                        # 텍스트 메시지는 border=True 컨테이너에 표시
                        with placeholders[current_idx].container(border=True):
                            st.markdown(item["content"])
                        current_idx += 1
                        
                    elif item_type == "tool":
                        # 도구 실행 결과
                        tool_name = item.get("name", "도구 실행 결과")
                        if tool_name in ["handoff_for_agent", "handoff_for_supervisor"]:
                            # 핸드오프는 border=False 컨테이너에 표시
                            with placeholders[current_idx].container(border=False):
                                st.markdown(item["content"])
                        else:
                            # 다른 도구들은 익스팬더에 표시, expanded=False로 일치
                            with placeholders[current_idx].expander(f"🛠️ {tool_name} 도구를 사용합니다.", expanded=False):
                                st.code(item["content"])
                        current_idx += 1
                        
                    elif item_type == "agent_change":
                        # 에이전트 전환은 success 메시지로 표시
                        with placeholders[current_idx].container(border=False):
                            st.success(f"{item.get('agent', 'unknown')} 에이전트에게 통제권을 전달합니다.")
                        current_idx += 1
            else:
                # 기존 형식 또는 에러 메시지는 그대로 표시
                st.markdown(str(content))

# --- 저장된 메시지 표시 ---
for message in st.session_state.messages:
    render_message(message)

# --- 사용자 입력 처리 ---
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 표시
    render_message({"role": "user", "content": prompt})

    # 어시스턴트 응답 처리 시작
    with st.container(border=False):   
        # 플레이스홀더 30개 미리 생성
        placeholders = [st.empty() for _ in range(50)]
        
        # 현재 사용할 플레이스홀더 인덱스
        current_idx = 0
        
        # 메시지 저장용 객체
        message_data = {
            "messages": []
        }
        
        # 현재 텍스트 누적
        current_text = ""
        
        logger.info(f"백엔드 요청 전송 - 세션 ID: {st.session_state.session_id}, 프롬프트: {prompt[:50]}...")
        
        try:
            response = requests.post(
                f"{FASTAPI_SERVER_URL}/chat/stream",
                json={"prompt": prompt, "session_id": st.session_state.session_id},
                stream=True,
                timeout=1200
            )
            response.raise_for_status()
            logger.info("백엔드 스트림 연결 성공")
            
            current_agent = "supervisor"
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data: "):
                    continue
                try:
                    # 'data: ' 접두사 제거 및 JSON 파싱
                    payload = json.loads(line[6:])
                    msg_type = payload.get("type", "message")
                    text = payload.get("text", "")
                    agent = payload.get("response_agent", "unknown")
                    
                    if agent != current_agent:
                        # 현재 텍스트 저장 (있을 경우)
                        if current_text:
                            with placeholders[current_idx].container(border=True):
                                st.write(current_text)
                            message_data["messages"].append({
                                "type": "text",
                                "content": current_text
                            })
                            current_idx += 1
                            current_text = ""
                        
                        # 에이전트 전환 표시
                        with placeholders[current_idx].container(border=False):
                            st.success(f"{agent} 에이전트에게 통제권을 전달합니다.")
                        message_data["messages"].append({
                            "type": "agent_change",
                            "agent": agent
                        })
                        current_agent = agent
                        current_idx += 1
                    
                    # 메시지 타입별 처리
                    if msg_type == "message":
                        # 일반 텍스트는 현재 플레이스홀더에 스트리밍
                        current_text += text
                        with placeholders[current_idx].container(border=True):
                            st.markdown(current_text)
                        
                    elif msg_type == "tool":
                        # 현재 텍스트 저장 (있을 경우)
                        if current_text:
                            with placeholders[current_idx].container(border=True):
                                st.markdown(current_text)
                            message_data["messages"].append({
                                "type": "text",
                                "content": current_text
                            })
                            current_idx += 1
                            current_text = ""
                        
                        # 도구 실행 결과를 새 플레이스홀더에 익스팬더로 표시
                        tool_name = payload.get("tool_name")
                        with placeholders[current_idx].expander(f"🛠️ {tool_name} 도구를 사용합니다.", expanded=False):
                                st.code(text)
                        
                        # 도구 실행 결과 저장
                        message_data["messages"].append({
                            "type": "tool",
                            "name": tool_name,
                            "content": text
                        })
                        current_idx += 1
                    
                    elif msg_type == "end":
                        # 최종 텍스트 저장
                        if current_text:
                            with placeholders[current_idx].container(border=True):
                                st.markdown(current_text)
                            message_data["messages"].append({
                                "type": "text",
                                "content": current_text
                            })
                        continue
                                        
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON 파싱 실패, 데이터 무시: {line[6:]} (오류: {str(e)})")
                    with placeholders[current_idx].container(border=False):
                        st.error(f"JSON 파싱 오류: {str(e)}")
                    current_idx += 1
                    continue
                except Exception as e:
                    logger.error(f"메시지 처리 중 오류 발생: {str(e)}", exc_info=True)
                    with placeholders[current_idx].container(border=False):
                        st.error(f"메시지 처리 오류: {str(e)}")
                    current_idx += 1
                    continue
            
            # 완성된 어시스턴트 응답을 JSON 형태로 세션 상태에 저장
            st.session_state.messages.append({"role": "assistant", "content": message_data})
            logger.info("어시스턴트 응답 저장 완료")
            
        except requests.exceptions.RequestException as e:
            error_msg = f"백엔드 연결 오류: {e}"
            logger.error(error_msg, exc_info=True)
            with placeholders[current_idx].container():
                st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        except Exception as e:
            error_msg = f"응답 처리 중 오류 발생: {e}"
            logger.error(error_msg, exc_info=True)
            with placeholders[current_idx].container():
                st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
