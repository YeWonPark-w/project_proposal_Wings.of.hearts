import os
import json
import time
import requests
import sys

# Windows 터미널에서 한글 깨짐 방지
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stdin.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def initialize_program():
    """
    프로그램 초기화 함수.
    상담사의 정체성을 부여하고 대화 역사를 초기화합니다.
    """
    print("\n==================================================")
    print("      [마음나래] - AI 마음 치유 도우미")
    print("==================================================")
    print("마음나래 입니다. 오늘은 극복하고 싶은 어떤 마음이 드셨나요?")
    print("(감정, 신체적 증상, 최근의 행동 변화 등을 편하게 말씀해 주세요.)")
    print("--------------------------------------------------")
    
    # AI에게 전문적인 CBT 심리상담사 정체성을 부여하는 시스템 지침
    system_instruction = (
        "너는 친절하고 전문적인 심리상담사 '마음나래'이다. "
        "사용자가 극복하고 싶은 자신의 감정, 정신/신체 상태, 행동 등에 대해 이야기할 것이다. "
        "아래 규칙에 따라 대화와 조언을 제어하라:\n"
        "1. 사용자의 입력이 너무 짧거나 모호하면(예: '우울하다', '힘들다' 등 한두 단어), 성급하게 해결책을 주지 말고 "
        "어떤 마음의 감정이 드는지, 두통이나 불면 등의 신체 증상이 동반되는지, 또는 할 일을 미루거나 고립되는 등의 최근 행동 양상은 어떤지 구체적으로 묻는 다정한 질문을 던져라.\n"
        "2. 사용자가 충분히 구체적인 상태를 적었거나 추가 답변을 통해 정보가 다 모였다면, 마음에 공감해주며 [인지적 측면], [정서적 측면], [행동적 측면]으로 나누어 극복할 수 있는 구체적인 '단기 해결방안'을 한국어로 정성껏 추천해라. "
        "이때, 단기 해결방안 출력의 가장 마지막 줄에는 반드시 정확히 '[SHORT_DONE]' 이라는 키워드만 한 줄 추가해라. (프로그램 제어를 위해 필수)\n"
        "3. 사용자가 장기 극복 방안이나 지속적인 관리법을 원한다는 요청을 하면, [장기 인지 방안], [장기 정서 방안], [장기 행동 방안]을 각각 하나씩 제시하고, 가장 마지막 줄에 반드시 '[LONG_DONE]' 이라는 키워드만 한 줄 추가해라. (프로그램 제어를 위해 필수)\n"
        "4. 사용자가 선택한 장기 해결방안(인지, 정서, 행동 중 하나)에 대해 구체적인 실천 방법을 요청하면, 1단계부터 5단계까지 누구나 바로 따라 할 수 있는 마이크로 실천 계획으로 상세히 나눠 설명해라. "
        "가장 마지막 줄에는 반드시 '[PLAN_DONE]' 이라는 키워드만 한 줄 추가해라. (프로그램 제어를 위해 필수)"
    )
    
    # 초기 대화 기록 설정
    history = [{"role": "system", "content": system_instruction}]
    return history

def get_user_input(prompt_text="요즘 사용자님의 마음은 어떤가요?: "):
    """
    사용자로부터 입력을 받는 단순 함수. 
    """
    return input(prompt_text)
# 함수는 공장이고, return은 완성품을 공장 밖으로 내보내는 것

def simulate_ai_response(history):
    """
    인터넷 연결이 없거나 API 키가 없는 경우 작동하는 오프라인 시뮬레이션 응답기.
    사용자 대화 단계(대화 내용 분석)에 맞춰 적절한 응답을 흉내 냅니다.
    """
    # 가장 최근의 사용자 입력 찾기
    last_user_message = ""
    for msg in reversed(history):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break
            
    # 사용자 메시지 수 계산 (대화 단계 유추용)
    user_count = len([msg for msg in history if msg["role"] == "user"])
    
    # 1. 장기 극복 방안 중 특정 카테고리를 골랐을 때 (5단계 실천방안 제공)
    if "실천" in last_user_message or any(opt in last_user_message for opt in ["인지", "정서", "행동"]) and user_count >= 3:
        selected_type = "정서적 명상"
        if "인지" in last_user_message:
            selected_type = "인지적 감사 일기"
        elif "행동" in last_user_message:
            selected_type = "행동적 가벼운 운동"
            
        return (
            f"선택하신 '{selected_type}' 방안을 실천하기 위한 [5단계 실천 계획]입니다:\n\n"
            f"1단계: 매일 아침 기상 직후 혹은 저녁 취침 전 5분이라는 명확한 시간을 정해 알람을 맞춥니다.\n"
            f"2단계: 휴대폰 알림을 끄고 방해받지 않는 독립적인 공간을 확보합니다.\n"
            f"3단계: 첫날에는 단 1분이라도 가볍게 시작(한 번 호흡하기, 한 줄 쓰기 등)하여 뇌의 저항감을 낮춥니다.\n"
            f"4단계: 완료 후 달력에 스티커를 붙이거나 체크를 하며 나를 위해 노력했음을 스스로 격려합니다.\n"
            f"5단계: 만약 하루를 거르더라도 자책하지 않고 다음 날 아주 작게 다시 시작합니다.\n\n"
            f"[PLAN_DONE]"
        )
        # f는 문자열 안에 변수를 넣게 해주기 위해 사용함


    # 2. 장기적인 측면의 해결방안을 물어본 경우
    elif "장기적" in last_user_message or "장기" in last_user_message:
        return (
            "인지, 정서, 행동의 세 가지 측면에서 추천해 드리는 [장기적인 극복 방안]입니다:\n\n"
            "[장기 인지 방안] 매일 저녁 감사한 일 3가지를 적는 '감사 일기'를 습관화하여 긍정적인 인지 필터 기르기.\n"
            "[장기 정서 방안] 매일 5분씩 깊은 호흡에 온전히 집중하는 '마음챙김 호흡'으로 감정의 편도체 다스리기.\n"
            "[장기 행동 방안] 주 3회 30분씩 가볍게 땀이 나는 강도의 산책이나 스트레칭을 통해 뇌에 도파민 활성화하기.\n\n"
            "[LONG_DONE]"
        )
        
    # 3. 마음상태 초기 진단 단계
    else:
        # 10글자 이하이거나 모호한 핵심 단어가 없을 때 구체화 질문
        if len(last_user_message.strip()) < 10:
            return (
                "적어주신 내용만으로는 마음 상태를 깊이 들여다보기 조금 어렵습니다.\n"
                "혹시 어떤 상황에서 그런 기분을 느끼시는지, 머리가 무겁거나 가슴이 답답한 등의 '신체 반응'이 있는지,\n"
                "그리고 최근 무기력하게 누워만 있거나 회피하는 등의 '행동 변화'도 있는지 조금 더 자세히 적어주시면 큰 도움이 됩니다."
            )
        else:
            # 상태가 구체적일 때 단기 처방전 출력
            return (
                "적어주신 마음 상태를 바탕으로 마음나래가 준비한 맞춤형 [단기 해결 처방전]입니다:\n\n"
                "[인지적 측면]\n"
                "지금 느끼는 큰 불안이나 자책은 상황이 진짜로 나빠서가 아니라, 지친 뇌의 부정적 해석(인지적 왜곡)일 수 있습니다.\n"
                "현재 드는 걱정거리를 종이에 쓴 뒤 '이 생각은 객관적으로 사실인가?' 한 발 떨어져서 의심해 보세요.\n\n"
                "[정서적 측면]\n"
                "느끼고 계신 감정을 '나쁜 감정'이라며 밀쳐내거나 자책하지 마세요.\n"
                "'내가 지금 상황에서 스트레스와 서운함을 강하게 느낄 만하구나'라고 자기 자신을 따뜻하게 안아주고 수용해 줍니다.\n\n"
                "[행동적 측면]\n"
                "의욕은 가만히 있으면 생기지 않고, 몸을 미세하게라도 움직여야 생깁니다.\n"
                "지금 당장 자리에서 일어나 따뜻한 물을 마시거나, 3분 동안 창밖을 내다보며 가벼운 목 스트레칭을 실천해 보세요.\n\n"
                "[SHORT_DONE]"
            )

def request_ai_solution(history, api_key):
    """
    Gemini API를 호출하여 AI의 답변을 받아옵니다.
    네트워크 실패나 API 키 부재 시 시뮬레이션 모드로 작동합니다.
    """
    if not api_key:
        return simulate_ai_response(history)
        
    # Gemini API 호출 주소 및 설정
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # Streamlit이나 OpenAI 형태의 대화 리스트를 Gemini API 규격으로 변환
    gemini_contents = []
    system_instruction_text = ""
    
    for message in history:
        role = message["role"]
        content = message["content"]
        if role == "system":
            system_instruction_text = content
        else:
            # Gemini의 role은 user와 model만 허용됩니다.
            gemini_role = "user" if role == "user" else "model"
            gemini_contents.append({
                "role": gemini_role,
                "parts": [{"text": content}]
            })
            
    payload = {
        "contents": gemini_contents
    }
    
    # 시스템 instruction 추가
    if system_instruction_text:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction_text}]
        }
        
    try:
        # API 요청 보내기
        response = requests.post(url, headers=headers, json=payload, timeout=12)
        if response.status_code == 200:
            res_json = response.json()
            ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
            return ai_text
        else:
            # 2.5-flash 실패 시 1.5-flash 모델로 폴백
            fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            response_fb = requests.post(fallback_url, headers=headers, json=payload, timeout=12)
            if response_fb.status_code == 200:
                res_json = response_fb.json()
                ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
                return ai_text
            else:
                print(f"\n[알림] API 응답 실패 (코드: {response.status_code}). 시뮬레이션 모드로 진행합니다.")
                return simulate_ai_response(history)
    except Exception as e:
        print(f"\n[알림] 네트워크 연결 장애가 발생했습니다 ({str(e)}). 시뮬레이션 모드로 진행합니다.")
        return simulate_ai_response(history)

def print_solution(solution_text):
    """
    결과 처방전을 화면에 예쁘게 포맷팅하여 출력하는 함수.
    """
    print("\n==================================================")
    print("            [마음나래의 치유 처방전]")
    print("==================================================")
    print(solution_text)
    print("==================================================")

def save_session_log(user_initial_state, solution_type, user_feedback):
    """
    상담기록을 '마음상태 + 선택한 해결방안이 어떤 종류인지'를 포함하여 파일에 저장합니다.
    """
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    log_filename = "mind_narae_history.txt"
    
    # 텍스트 로그 형식 정의
    log_entry = (
        f"==================================================\n"
        f"상담 시각: {current_time}\n"
        f"마음 상태 (초기 호소): {user_initial_state}\n"
        f"해결방안 종류: [{solution_type}]적 개입\n"
        f"치유 시도 후 변화점: {user_feedback}\n"
        f"==================================================\n\n"
    )
    
    try:
        # 파일에 이어쓰기(append)로 기록 저장
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"\n[기록] 귀하의 마음성장 일기가 '{log_filename}' 파일에 누적 기록되었습니다.")
    except Exception as e:
        print(f"\n[오류] 파일 기록 중 에러가 발생했습니다: {e}")

# ==================================================
# [새로 추가된 기능] 사용자의 입력을 분석하여 긍정적인 의미인지 판별하는 함수
# ==================================================
def is_affirmative(text):
    """
    사용자의 입력에 '예', '네', 'yes', '받고 싶어' 등 긍정적 의미를 갖는 단어가 포함되어 있는지 확인합니다.
    사용자가 다양한 말투로 긍정 의사를 표현해도 정상 작동하도록 돕습니다.
    """
    # 공백 제거 및 영어 소문자 변환
    text_clean = text.strip().lower()
    
    # 긍정을 나타내는 주요 단어 리스트
    positive_words = [
        "예", "네", "어", "응", "yes", "y", "받고", "원해", "좋아", 
        "오케이", "ok", "원합니다", "하겠습", "할래", "부탁", "해줘"
    ]
    
    # 리스트의 단어 중 하나라도 사용자의 답변에 들어있다면 긍정(True)으로 판단합니다.
    for word in positive_words:
        if word in text_clean:
            return True
            
    # 그 외에는 부정(False)으로 판단합니다.
    return False

def main():
    # 0. API 키 탐색 및 입력
    # 발급받으신 API 키가 있다면 아래 큰따옴표("") 안에 붙여넣어 주세요.
    # (예시: api_key = "AIzaSyABC123...")
    api_key = "AQ.Ab8RN6KgwyDWmi5IzGwcVcZWrO5sStO4xsLRMtDQ4ltz2jE1fw"
    
    # 만약 키를 붙여넣지 않고 그대로 실행하면 터미널에서 묻거나 시뮬레이션 모드로 작동합니다.
    if api_key == "여기에_복사한_API_키를_붙여넣으세요" or not api_key:
        print("[안내] 환경 변수(GEMINI_API_KEY)가 감지되지 않았습니다.")
        api_key = input("사용하실 Gemini API Key를 입력해 주세요 (빈칸인 채로 엔터를 누르면 '시뮬레이션 모드'로 작동합니다): ").strip()
        if not api_key:
            print("[알림] API Key가 비어 있어 '오프라인 시뮬레이션 모드'로 진행합니다.\n")
            
    # 1. 초기화 (시스템 프롬프트 생성 및 인사말)
    conversation_history = initialize_program()
    
    # 사용자의 첫 증상 진술 기록을 남겨두기 위한 변수
    user_initial_state = ""
    
    # --- 단기 처방전 및 장기 처방전 제공 흐름 ---
    user_text = get_user_input("나의 현재 마음 상태 (감정/신체/행동 등 입력, 종료를 원하면 '종료' 입력): ")
    
    # '종료' 처리
    if user_text.strip() == "종료":
        print("\n상담을 종료합니다. 오늘 하루 수고 많으셨습니다. 늘 나를 아껴주세요.")
        return

    user_initial_state = user_text
    conversation_history.append({"role": "user", "content": user_text})

    while True:
        print("\nAI 상담사가 답변을 분석하는 중입니다...")
        ai_answer = request_ai_solution(conversation_history, api_key)
        
        if "[SHORT_DONE]" in ai_answer:
            # 단기 처방전 출력
            clean_answer = ai_answer.replace("[SHORT_DONE]", "").strip()
            print_solution(clean_answer)
            break
        else:
            # 상태가 모호하여 추가 질문을 던진 경우
            print(f"\n[마음나래]: {ai_answer}")
            user_text = get_user_input("\n나의 답변 (종료를 원하면 '종료' 입력): ")
            if user_text.strip() == "종료":
                print("\n상담을 종료합니다. 오늘 하루 수고 많으셨습니다. 늘 나를 아껴주세요.")
                return
            conversation_history.append({"role": "user", "content": user_text})

    # 사용자가 원한다면 장기 처방전 제공
    want_long_term = get_user_input("\n더 장기적으로 마음을 관리할 수 있는 [장기 처방전]도 받아보시겠습니까? (예/아니오): ")
    if is_affirmative(want_long_term):
        long_term_prompt = (
            "이 상태를 극복하기 위한 장기적인 해결방안을 [장기 인지 방안], [장기 정서 방안], [장기 행동 방안]의 세 가지 측면에서 각각 하나씩 제시해 주세요. "
            "마지막 줄에는 반드시 정확히 '[LONG_DONE]' 이라는 키워드만 한 줄 추가해 주세요."
        )
        conversation_history.append({"role": "user", "content": long_term_prompt})
        
        print("\nAI 상담사에게 장기 처방전을 요청하는 중입니다...")
        ai_answer = request_ai_solution(conversation_history, api_key)
        
        # [LONG_DONE] 태그 확인 및 출력
        clean_answer = ai_answer.replace("[LONG_DONE]", "").strip()
        print_solution(clean_answer)
        
        print("\n장기 극복 가이드를 제공해 드렸습니다. 오늘 하루 수고 많으셨습니다. 늘 나를 아껴주세요.")
    else:
        print("\n오늘 하루 수고 많으셨습니다. 늘 나를 아껴주세요.")

if __name__ == "__main__":
    main()
