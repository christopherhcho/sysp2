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

# '/submit' 엔드포인트로 POST 요청이 들어왔을 때 처리하는 함수
@app.route('/submit', methods=['POST'])
def submit():
    # 클라이언트에서 전송된 JSON 데이터 받기
    data = request.json
    
    # JSON 데이터에서 'inputText' 키로 사용자가 입력한 텍스트를 추출, 값이 없으면 빈 문자열 반환
    input_text = data.get('inputText', '')

    # API 요청에 필요한 데이터를 사전 형태로 구성
    api_request_payload = {
        "model": "gpt-4o-mini",  # 사용할 OpenAI 모델 (gpt-4o-mini 지정)
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},  # 시스템 메시지, AI에게 역할 지시
            {"role": "user", "content": input_text}  # 사용자가 입력한 텍스트 전달
        ],
        "max_tokens": 100,  # 생성할 응답의 최대 토큰 수
        "temperature": 0.7  # 응답의 창의성 정도 (0에 가까울수록 덜 창의적, 1에 가까울수록 더 창의적)
    }

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
    app.run(debug=True, port=8070)
