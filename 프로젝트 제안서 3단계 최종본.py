import os
import json
import time
import urllib.request
import urllib.error
import sys

# Windows 터미널에서 한글 깨짐 방지
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stdin.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def load_history_log():
    """
    이전 마음 성장 일기를 불러와서 출력해주는 함수
    사용자가 과거 상담 결과와 변화된 점을 눈으로 보며 성장도를 확인할 수 있도록 도움.
    """
    log_filename = "mind_narae_history.txt"
    # 파일이 존재하는지 먼저 확인.
    if os.path.exists(log_filename):
        print("\n==================================================")
        print("      ★ [이전 상담 및 마음 성장 기록] ★")
        print("==================================================")
        try:
            # 파일을 읽어서 화면에 출력함.
            with open(log_filename, "r", encoding="utf-8") as f:
                records = f.read()
                if records.strip():
                    print(records)
                else:
                    print("아직 저장된 마음 성장 기록이 없습니다. 새로운 첫 발걸음을 떼어보세요!\n")
        except Exception as e:
            print(f"[안내] 이전 기록을 읽는 도중 오류가 발생했습니다: {e}")
        print("==================================================\n")
    else:
        # 파일이 없을 때는 안내 문구만 출력함.
        print("\n[안내] 저장된 이전 상담 기록이 없습니다. 오늘 첫 성장의 기록을 남겨보세요!\n")

def initialize_program():
    """
    프로그램 초기화 함수
    상담사의 정체성을 부여하고 대화 기록을 초기화함.
    """
    print("\n==================================================")
    print("      [마음나래] - AI 마음 치유 도우미")
    print("==================================================")
    print("마음나래 입니다. 오늘은 극복하고 싶은 어떤 마음이 드셨나요?")
    print("(감정, 신체적 증상, 최근의 행동 변화 등을 편하게 말씀해 주세요.)")
    print("--------------------------------------------------")
    
    # AI에게 전문적인 심리상담사 정체성을 부여하는 시스템 지침
    system_instruction = (
        "너는 친절하고 전문적인 심리상담사 '마음나래'이다. "
        "사용자가 극복하고 싶은 자신의 감정, 정신/신체 상태, 행동 등에 대해 이야기할 것이다. "
        "아래 규칙에 따라 대화와 조언을 제공하라:\n"
        "1. 사용자의 입력이 너무 짧거나 모호하면(예: '우울하다', '힘들다' 등 한두 단어), 성급하게 해결책을 주지 말고 "
        "어떤 마음의 감정이 드는지, 두통이나 불면 등의 신체 증상이 동반되는지, 또는 할 일을 미루거나 고립되는 등의 최근 행동 양상은 어떤지 구체적으로 묻는 다정한 질문을 던져라.\n"
        "2. 사용자가 충분히 구체적인 상태를 적었거나 추가 답변을 통해 정보가 다 모였다면, 마음에 공감해주며 [인지적 측면], [정서적 측면], [행동적 측면]으로 나누어 극복할 수 있는 구체적인 '단기 해결방안'을 한국어로 정성껏 추천해라.\n"
        "3. 사용자가 장기 극복 방안을 원한다고 하면, [장기 인지 방안], [장기 정서 방안], [장기 행동 방안]을 각각 하나씩 제시해라.\n"
        "4. 사용자가 선택한 장기 해결방안(인지, 정서, 행동 중 하나)에 대해 구체적인 실천 방법을 요청하면, 1단계부터 5단계까지 누구나 바로 따라 할 수 있는 마이크로 실천 계획으로 상세히 나눠 설명해라."
    )
    
    # 초기 대화 기록 설정 (시스템 instruction 추가)
    history = [{"role": "system", "content": system_instruction}]
    return history

def get_user_input(prompt_text="현재 마음 상태를 알려주세요: "):
    """
    사용자로부터 입력을 받는 단순 함수
    """
    return input(prompt_text)

def simulate_ai_response(history):
    """
    인터넷 연결이 없거나 API 키가 없는 경우 작동하는 오프라인 시뮬레이션 응답기
    사용자 대화 내용 분석에 맞춰 적절한 응답을 흉내 냄.
    """
    # 가장 최근의 사용자 입력 찾기
    last_user_message = ""
    for msg in reversed(history):
        if msg["role"] == "user":
            last_user_message = msg["content"]
            break
            
    # 1. 5단계 실천 계획 요청인지 확인
    if "실천 계획" in last_user_message or "5단계" in last_user_message:
        selected_type = "정서적 개입"
        if "인지" in last_user_message:
            selected_type = "장기 인지 방안 (감사 일기)"
        elif "행동" in last_user_message:
            selected_type = "장기 행동 방안 (가벼운 운동)"
        elif "정서" in last_user_message:
            selected_type = "장기 정서 방안 (호흡 명상)"
            
        return (
            f"선택하신 '{selected_type}' 방안을 일상에서 실천하기 위한 [5단계 실천 계획]입니다:\n\n"
            f"1단계: 매일 아침 기상 직후 혹은 저녁 취침 전 5분이라는 명확한 시간을 정해 알람을 맞춥니다.\n"
            f"2단계: 휴대폰 알림을 끄고 방해받지 않는 독립적인 공간을 확보합니다.\n"
            f"3단계: 첫날에는 단 1분이라도 가볍게 시작(한 번 호흡하기, 한 줄 쓰기 등)하여 뇌의 저항감을 낮춥니다.\n"
            f"4단계: 완료 후 달력에 스티커를 붙이거나 체크를 하며 나를 위해 노력했음을 스스로 격려합니다.\n"
            f"5단계: 만약 하루를 거르더라도 자책하지 않고 다음 날 아주 작게 다시 시작합니다."
        )

    # 2. 장기적인 측면의 해결방안을 물어본 경우
    elif "장기" in last_user_message:
        return (
            "인지, 정서, 행동의 세 가지 측면에서 추천해 드리는 [장기적인 극복 방안]입니다:\n\n"
            "[장기 인지 방안] 매일 저녁 감사한 일 3가지를 적는 '감사 일기'를 습관화하여 긍정적인 인지 필터 기르기.\n"
            "[장기 정서 방안] 매일 5분씩 깊은 호흡에 온전히 집중하는 '마음챙김 호흡'으로 감정의 편도체 다스리기.\n"
            "[장기 행동 방안] 주 3회 30분씩 가볍게 땀이 나는 강도의 산책이나 스트레칭을 통해 뇌에 도파민 활성화하기."
        )
        
    # 3. 입력이 너무 짧거나 구체화 요청 프롬프트인 경우
    elif "질문" in last_user_message or "짧습니다" in last_user_message or len(last_user_message.strip()) < 10:
        return (
            "마음 상태에 대해 말씀해 주셔서 감사합니다. 혹시 어떤 상황에서 그런 기분을 느끼시는지,\n"
            "머리가 무겁거나 가슴이 답답한 등의 '신체 반응'이 있는지, 그리고 최근 할 일을 미루는 등의\n"
            "'행동 변화'도 함께 나타나는지 조금 더 자세히 적어주실 수 있을까요?"
        )
        
    # 4. 일반적인 단기 처방전 출력
    else:
        return (
            "적어주신 마음 상태를 바탕으로 마음나래가 준비한 맞춤형 [단기 해결 처방전]입니다:\n\n"
            "[인지적 측면]\n"
            "지금 느끼는 큰 불안이나 자책은 상황이 진짜로 나빠서가 아니라, 지친 뇌의 부정적 해석(인지적 왜곡)일 수 있습니다.\n"
            "현재 드는 걱정거리를 종이에 쓴 뒤 '이 생각은 객관적으로 사실인가?' 한 발 떨어져서 의심해 보세요.\n\n"
            "[정서적 측면]\n"
            "느끼고 계신 감정을 '나쁜 감정'이라며 밀쳐내거나 자책하지 마세요.\n"
            "'내가 지금 상황에서 스트레스와 서운함을 강하게 느낄 만하구나'라고 자기 자신을 따뜻하게 안아주고 수용해 줍니다.\n"
            "[행동적 측면]\n"
            "의욕은 가만히 있으면 생기지 않고, 몸을 미세하게라도 움직여야 생깁니다.\n"
            "지금 당장 자리에서 일어나 따뜻한 물을 마시거나, 3분 동안 창밖을 내다보며 가벼운 목 스트레칭을 실천해 보세요."
        )

def request_ai_solution(history, api_key):
    """
    Gemini API를 호출하여 AI의 답변을 받아옴.
    네트워크 실패나 API 키 부재 시 시뮬레이션 모드로 작동함.
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
            # Gemini의 role은 user와 model만 허용됨.
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
        
    # JSON 데이터를 바이트 스트림으로 인코딩함.
    data_bytes = json.dumps(payload).encode('utf-8')
    
    try:
        # urllib를 사용해 API 요청을 보냄.
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=12) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
            return ai_text
            
    except urllib.error.HTTPError as e:
        # 2.5-flash 실패(예: 모델 지원 안 함 등) 시 1.5-flash 모델로 폴백함.
        try:
            fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            req_fb = urllib.request.Request(fallback_url, data=data_bytes, headers=headers, method='POST')
            with urllib.request.urlopen(req_fb, timeout=12) as response_fb:
                res_body_fb = response_fb.read().decode('utf-8')
                res_json_fb = json.loads(res_body_fb)
                ai_text = res_json_fb['candidates'][0]['content']['parts'][0]['text']
                return ai_text
        except Exception as fallback_err:
            print(f"\n[알림] API 응답 실패 (에러코드: {e.code}). 시뮬레이션 모드로 진행함.")
            return simulate_ai_response(history)
            
    except Exception as e:
        print(f"\n[알림] 네트워크 연결 장애가 발생함 ({str(e)}). 시뮬레이션 모드로 진행함.")
        return simulate_ai_response(history)

def print_solution(solution_text):
    """
    결과 처방전을 화면에 포맷팅하여 출력하는 함수
    """
    print("\n==================================================")
    print("            [마음나래의 치유 처방전]")
    print("==================================================")
    print(solution_text)
    print("==================================================")

def save_session_log(user_initial_state, solution_type, user_feedback):
    """
    상담기록을 '마음상태 + 선택한 해결방안이 어떤 종류인지'를 기준으로 파일에 저장함.
    """
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    log_filename = "mind_narae_history.txt"
    
    # 텍스트 로그 형식 정의
    log_entry = (
        f"==================================================\n"
        f"상담 시각: {current_time}\n"
        f"1. 마음 상태: {user_initial_state}\n"
        f"2. 선택한 해결방안: {solution_type}\n"
        f"3. 변화점 기록: {user_feedback}\n"
        f"==================================================\n\n"
    )
    
    try:
        # 파일에 이어쓰기(append)로 기록 저장
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"\n[기록] 귀하의 마음성장 일기가 '{log_filename}' 파일에 누적 기록되었습니다.")
    except Exception as e:
        print(f"\n[오류] 파일 기록 중 에러가 발생했습니다: {e}")

def interpret_yes_no(text):
    """
    사용자의 입력을 분석하여 긍정('yes'), 부정('no'), 혹은 모호함('error')으로 분류함.
    """
    text_clean = text.strip().lower()
    
    # 긍정을 의미하는 단어들 (예, 네, 어, 응, yes, y, 좋아, 좋아요, 원해, 원해요, ok, 오케이 등)
    positive_words = [
        "예", "네", "어", "응", "yes", "y", "좋아", "좋아요", "원해", "원해요", 
        "오케이", "ok", "원합니다", "할래", "부탁", "해줘", "좋습니다", "좋고"
    ]
    # 부정을 의미하는 단어들 (아니, 아니오, 아뇨, ㄴㄴ, no, n, 싫어, 싫어요, 안해, 안할래, 괜찮아 등)
    negative_words = [
        "아니", "아뇨", "ㄴㄴ", "no", "n", "싫어", "싫어요", "안해", "안할래", "괜찮아", 
        "필요없어", "사양", "싫습니다", "안 원해"
    ]
    
    for word in positive_words:
        if word in text_clean:
            return "yes"
            
    for word in negative_words:
        if word in text_clean:
            return "no"
            
    return "error"

def main():
    # 1. 프로그램 실행 시 이전 대화 및 변화점 기록 불러와 출력하기
    load_history_log()

    # API 키 검색 및 입력 (기존 제공되었던 키 유지)
    api_key = "AQ.Ab8RN6K7eHriKkS5T2rWyiEhZIxtZy-jBXD5xYb6q4BHFJfbRA"
    
    if api_key == "여기에_복사한_API_키를_붙여넣으세요" or not api_key:
        print("[안내] 환경 변수(GEMINI_API_KEY)가 감지되지 않았습니다.")
        api_key = input("사용하실 Gemini API Key를 입력해 주세요 (빈칸인 채로 엔터를 누르면 '시뮬레이션 모드'로 작동합니다): ").strip()
        if not api_key:
            print("[알림] API Key가 비어 있어 '오프라인 시뮬레이션 모드'로 진행합니다.\n")
            
    # 2. 프로그램 초기화
    # conversation_history: 사용자의 입력과 AI의 답변을 순서대로 누적해 기록하는 대화 저장소 (리스트 타입)
    # system_instruction: AI에게 심리상담사 역할을 부여하는 지시문 (문자열 타입)
    conversation_history = initialize_program()
    system_instruction = conversation_history[0]["content"]

    # 3. 사용자 마음상태 입력받기
    # user_input: 사용자가 입력한 정서/신체 증상 문장 전체 (문자열 타입)
    user_input = get_user_input("나의 현재 마음 상태 (감정/신체/행동 등 입력, 종료를 원하면 '종료' 입력): ")
    
    # '종료' 처리
    if user_input.strip() == "종료":
        print("\n상담을 종료합니다. 오늘 하루 수고 많으셨습니다. 늘 나를 아껴주세요.")
        return

    conversation_history.append({"role": "user", "content": user_input})

    # [MUST] 사용자의 더 구체적인 상태를 위한 질문하기 (항상 구체화 질문을 먼저 던짐)
    print("\n[마음나래]가 더 구체적인 상태 파악을 위해 질문을 준비하고 있습니다...")
    
    # 구체화용 질문을 요청하기 위한 임시 프롬프트 추가
    clarify_prompt = "사용자가 말한 마음 상태에 대해 공감해주고, 어떤 구체적인 감정이나 신체 반응(두통, 불면 등), 행동 변화(할 일 미루기 등)가 나타나는지 다정하게 추가 질문을 던져주세요."
    conversation_history.append({"role": "user", "content": clarify_prompt})
    
    # AI 또는 시뮬레이션 호출
    ai_response_text = request_ai_solution(conversation_history, api_key)
    
    # ai_raw_response: AI API가 서버로부터 보내온 날것의 응답 데이터 (시뮬레이션 시 간소화된 딕셔너리로 대처)
    ai_raw_response = {"role": "assistant", "content": ai_response_text}
    
    # Final_solution: AI 응답 중 핵심 답변만 골라낸 최종 문장
    Final_solution = ai_response_text
    
    # 구체화용 질문 출력
    print(f"\n[마음나래의 질문]\n{Final_solution}")
    print("--------------------------------------------------")
    
    # 사용자로부터 구체적인 답변 입력받기
    user_input_detail = get_user_input("질문에 대해 말씀해 주세요 (종료를 원하면 '종료' 입력): ")
    if user_input_detail.strip() == "종료":
        print("\n상담을 종료합니다. 오늘 하루 수고 많으셨습니다. 늘 나를 아껴주세요.")
        return
        
    # user_input을 기존 입력에 덧붙여서 보관
    user_input = user_input + " / " + user_input_detail
    
    # 대화 히스토리에 실제 AI 질문과 사용자 답변 누적 기록
    conversation_history[-1] = {"role": "assistant", "content": Final_solution}
    conversation_history.append({"role": "user", "content": user_input_detail})

    # [MUST] 입력받은 데이터를 통해 인지/정서/행동의 측면에서 해결방안을 단기 측면에서 추천하기
    short_term_prompt = (
        "지금까지 나눈 대화를 바탕으로, 사용자의 상태를 완화하기 위한 [단기 해결방안]을 "
        "[인지적 측면], [정서적 측면], [행동적 측면]으로 나누어 알기 쉽게 각각 제시해 주세요."
    )
    conversation_history.append({"role": "user", "content": short_term_prompt})
    
    print("\n[마음나래]가 단기 해결방안을 생각하고 있습니다...")
    ai_response_text = request_ai_solution(conversation_history, api_key)
    
    ai_raw_response = {"role": "assistant", "content": ai_response_text}
    Final_solution = ai_response_text
    
    # 단기 해결방안 출력
    print_solution(Final_solution)
    conversation_history.append({"role": "assistant", "content": Final_solution})

    # [NICE] 단기 측면의 해결방안 추천 이후 장기 측면의 해결방안을 원하는지 묻기
    # 예, 아니오 및 다양한 응답을 해석할 수 있도록 함
    selected_solution_type = "단기 해결방안"  # 최종 기록에 쓰일 종류 초기값
    
    while True:
        print("\n혹시 단기적인 방법 외에 길게 지속적으로 노력해볼 수 있는 장기적인 해결방안도 알아볼까요?")
        want_long_term = get_user_input("장기적인 해결방안을 원하십니까? (예/아니오): ")
        
        # 사용자의 다양한 긍정/부정 입력 해석
        decision = interpret_yes_no(want_long_term)
        
        if decision == "yes":
            # [NICE] 장기적인 측면의 해결방안을 원할 경우 제시하기
            long_term_prompt = (
                "사용자가 장기 해결방안을 원합니다. 인지, 정서, 행동의 측면에서 각각 하나씩 "
                "[장기 인지 방안], [장기 정서 방안], [장기 행동 방안]을 간단명료하게 제시해 주세요."
            )
            conversation_history.append({"role": "user", "content": long_term_prompt})
            
            print("\n[마음나래]가 장기 해결방안을 찾아보는 중입니다...")
            ai_response_text = request_ai_solution(conversation_history, api_key)
            
            ai_raw_response = {"role": "assistant", "content": ai_response_text}
            Final_solution = ai_response_text
            
            # 장기 해결방안 출력
            print_solution(Final_solution)
            conversation_history.append({"role": "assistant", "content": Final_solution})
            
            # [LATER] 사용자가 선택한 하나의 장기적 해결방안을 5단계로 나누어 실천 방안 제시하기
            print("\n제시된 장기 해결방안 중 가장 마음에 드는 혹은 실천해보고 싶은 방안을 골라주세요.")
            choice = get_user_input("선택해 주세요 (1. 인지 / 2. 정서 / 3. 행동): ")
            
            choice_type = "정서"  # 기본 선택 설정
            if choice in ["1", "인지"]:
                choice_type = "인지"
            elif choice in ["2", "정서"]:
                choice_type = "정서"
            elif choice in ["3", "행동"]:
                choice_type = "행동"
            else:
                if "인지" in choice:
                    choice_type = "인지"
                elif "행동" in choice:
                    choice_type = "행동"
                    
            selected_solution_type = f"장기 {choice_type} 방안"
            
            plan_prompt = (
                f"선택한 '{selected_solution_type}'에 대하여 구체적으로 일상에서 실천할 수 있는 "
                "5단계 실천 계획을 세워주세요. 각 단계별로 아주 쉽고 구체적으로 설명해 주세요."
            )
            conversation_history.append({"role": "user", "content": plan_prompt})
            
            print(f"\n[마음나래]가 '{selected_solution_type}'의 5단계 구체적인 실천 로드맵을 작성하고 있습니다...")
            ai_response_text = request_ai_solution(conversation_history, api_key)
            
            ai_raw_response = {"role": "assistant", "content": ai_response_text}
            Final_solution = ai_response_text
            
            # 5단계 실천 방안 출력
            print_solution(Final_solution)
            conversation_history.append({"role": "assistant", "content": Final_solution})
            break  # 올바른 입력을 처리했으므로 반복문 탈출
            
        elif decision == "no":
            print("\n알겠습니다. 장기 해결방안은 생략하고 다음 단계로 진행합니다.")
            break  # 반복문 탈출
            
        else:
            # 예/아니오 외 모호한 답변 시 안내 출력 후 다시 질문
            print("\n[안내] 답변이 모호하여 정확히 이해하지 못했습니다. '예' 또는 '아니오'로 대답해 주세요.")
            print("-" * 45)

    # [LATER] 성장을 눈으로 볼 수 있도록, 해결방안 사용 이후 변화점을 기록하는 질문하기
    print("\n==================================================")
    print("            [마음나래의 성장 기록 질문]")
    print("==================================================")
    user_feedback = get_user_input("Q. 처방을 받고 난 지금, 이전의 마음 상태와 비교해서 어떤 긍정적인 변화나 다짐이 생기셨나요?\n답변 입력: ")
    
    # [LATER] 사용자의 대화창 기록할 때 “마음상태 + 선택한 해결방안이 어떤 종류인지”를 기준으로 표시하기
    save_session_log(user_input, selected_solution_type, user_feedback)
    
    print("\n성장 일기가 정상적으로 저장되었습니다. 오늘 하루도 너무 애쓰셨습니다. 다음에 또 찾아주세요!")

if __name__ == "__main__":
    main()
