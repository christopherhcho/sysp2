from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드하여 Python 환경 변수로 설정
load_dotenv()

# 환경 변수에서 OpenAI API 키를 가져오기 (.env 파일에 저장된 API 키를 사용)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트를 초기화 (API 키를 통해 인증)
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# 기본 경로('/')로 접근 시 호출되는 함수 (index.html 페이지를 반환)
@app.route('/')
def home():
    return render_template('index.html')  # templates 폴더에 있는 index.html 파일을 반환

# GPT 프롬프트 설정
def generate_prompt(tab, input_text):
    if tab == 'event_edm':
        prompt = f"""
        # Instruction
        이 GPT는 사용자가 입력한 eDM 내용을 검토하고 피드백하는 용도로 만들어졌습니다.
        # Context
        - 사용자의 입력은 행사 eDM 본문 전체를 입력하게 됩니다.
        - 당신은 입력받은 행사 eDM 본문 전체를 고객 친화적이고 명료하게 수정하여 제시합니다.
        # Constraint
        - 사용자가 입력한 행사 eDM의 점수를 매기고 '(x/10점)' 형식으로 표기해 주세요.
        - 반드시 상단에 "당신이 입력한 요청서는 x/10점입니다. 아래 예시를 참고하여 다시 작성해주세요." 문구가 포함되도록 합니다.
        - 이모티콘, 이모지를 포함하지 말아주세요.
        - 마크다운 양식을 사용하지 마세요.
        # Example
        예시) 2024 충북 사람경영포럼에 충청권 기업인 여러분을 초대합니다! ..."""
        
    elif tab == 'promotion_edm':
        prompt = f"""
        # Instruction
        이 GPT는 사용자가 입력한 프로모션 eDM 내용을 검토하고 피드백하는 용도로 만들어졌습니다.
        # Context
        - 사용자의 입력은 프로모션 eDM 본문 전체를 입력하게 됩니다.
        - 당신은 입력받은 프로모션 eDM 본문 전체를 고객 친화적이고 명료하게 수정하여 제시합니다.
        # Constraint
        - 사용자가 입력한 프로모션 eDM의 점수를 매기고 '(x/10점)' 형식으로 표기해 주세요.
        - 반드시 상단에 "당신이 입력한 요청서는 x/10점입니다. 아래 예시를 참고하여 다시 작성해주세요." 문구가 포함되도록 합니다.
        - 이모티콘, 이모지를 포함하지 말아주세요.
        - 마크다운 양식을 사용하지 마세요.
        """
    
    elif tab == 'landing_page':
        prompt = f"""
        # Instruction
        이 GPT는 사용자가 입력한 랜딩 페이지 내용을 검토하고 피드백하는 용도로 만들어졌습니다.
        # Context
        - 사용자의 입력은 랜딩 페이지 본문 전체를 입력하게 됩니다.
        - 당신은 입력받은 랜딩 페이지 본문 전체를 고객 친화적이고 명료하게 수정하여 제시합니다.
        # Constraint
        - 사용자가 입력한 랜딩 페이지의 점수를 매기고 '(x/10점)' 형식으로 표기해 주세요.
        - 반드시 상단에 "당신이 입력한 요청서는 x/10점입니다. 아래 예시를 참고하여 다시 작성해주세요." 문구가 포함되도록 합니다.
        - 이모티콘, 이모지를 포함하지 말아주세요.
        - 마크다운 양식을 사용하지 마세요.
        """

    return {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text}
        ],
        "temperature": 0.8
    }

# '/submit' 엔드포인트로 POST 요청이 들어왔을 때 처리하는 함수
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    
    tab = data.get('tab')  # 사용자가 선택한 탭 (event_edm, promotion_edm, landing_page)
    input_text = data.get('inputText', '')  # 사용자가 입력한 텍스트

    # API 요청에 필요한 데이터를 사전 형태로 구성
    api_request_payload = generate_prompt(tab, input_text)

    # API 요청 전에 데이터 로그를 출력하여 전송될 데이터를 확인
    print("OpenAI API Request Payload:", api_request_payload)

    try:
        # OpenAI API에 요청을 보내고 응답을 받음
        response = client.chat.completions.create(**api_request_payload)

        # 응답에서 생성된 메시지 추출 (첫 번째 응답의 메시지를 가져옴)
        completion = response.choices[0].message.content

        # 클라이언트에게 JSON 형태로 응답을 반환 (200: 성공적인 요청 처리)
        return jsonify({'message': completion}), 200

    except Exception as e:
        # API 요청 중 오류가 발생할 경우 오류 메시지를 콘솔에 출력
        print("Error during API request:", str(e))
        # 클라이언트에게 오류 메시지를 JSON 형태로 반환 (500: 서버 내부 오류)
        return jsonify({'error': str(e)}), 500

# 애플리케이션을 실행할 때, Flask 서버를 시작 (디버그 모드에서 8070 포트로 실행)
if __name__ == '__main__':
    app.run(debug=False, port=8070, host='0.0.0.0')
