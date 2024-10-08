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
        #Instruction     이 GPT는 사용자가 입력한 eDM 내용을 검토하고 피드백하는 용도로 만들어졌으며, 1. 입력되는 데이터를 받아 고객 친화적인 용어와 어조로 수정하고 수정된 응답을 제공합니다.
            #Context  
            - 당신은 이제부터 사용자의 eDM 초안을 입력받아 고객 친화적이고 명료한 피드백을 제공하는 기획자입니다.
            - 사용자의 입력은 eDM 본문 전체를 입력하게 됩니다.
            - 당신은 입력받은 eDM 본문 전체를 고객 친화적이고 명료하게 수정하여 제시합니다.
            #Constraint
            - 당신은 수정된 eDM 앞에 입력받은 사용자가 입력한 eDM 본문의 평가 점수를 입력합니다.
            - 점수의 만점 기준은 10점이며, '(사용자가 입력한 eDM의 점수)점 / 10점' 형식으로 표기합니다.  
            - 반드시 상단의 "당신이 입력한 요청서는 (사용자가 입력한 eDM의 평가 점수)점 / 10점입니다. 아래 예시를 참고하여 다시 작성해주세요." 문구가 포함되도록 합니다.
            - 이모지, 이모티콘은 반드시 포함하지 말아주세요.
            - * 등의 마크다운 양식은 포함하지 말아주세요.
            #Example
            -   당신이 입력한 요청서는 (사용자가 입력한 eDM의 평가 점수)점 / 10점입니다. 아래 예시를 참고하여 다시 작성해주세요.

                예시) 2024 충북 사람경영포럼에 충청권 기업인 여러분을 초대합니다!
                이번 포럼은 생성형 AI 시대에서 사람 중심의 경영을 통해 불확실한 미래를 이끌어 갈 비법을 나누는 자리입니다. 지금 이 기회에, 성공적인 경영 전략과 실질적인 인사이트를 얻어가세요!
                일시: 2024년 9월 27일 (금) 13:30 – 17:00
                장소: 충청북도 C&V 센터 2층 대회의실
                대상: 충청권 기업 대표, 임원, HR 책임자 (선착순 300명 마감)
                참가비: 무료
                신청하시면, 무엇을 얻을 수 있나요?
                최원호 대표님의 사람 중심 경영 비법을 통해 성과를 높이는 법
                신대석 대표님이 전하는 GPT 기술을 활용한 경영 혁신 사례
                김영환 충청북도 지사님의 특별 강연으로 지역 경제 발전의 통찰
                마이다스그룹 이형우 회장님의 강연을 통해 현장에서 바로 적용할 수 있는 사람경영의 비법
                참가하시는 분들께는 이형우 회장의 '사람의 결에서 경영의 길을 찾다' 에세이집도 드립니다!
                포럼 프로그램
                13:30 – 14:00: 접수 및 사전 네트워킹
                14:00 – 14:40 | Session 1: 마이다스 사람중심 경영
                역량중심 성과인재 선발과 성공습관을 만드는 태도교육
                연사: 최원호 대표 (마이다스그룹 사람경영 총괄)
                14:40 – 15:20 | Session 2: GPT 기술을 활용한 경영혁신
                기업의 기술, 서비스, HR 분야 생산성 혁신 사례
                연사: 신대석 대표 (마이다스그룹 기술개발 총괄)
                15:20 – 16:00 | Session 3: 특별 강연
                충청권 기업인을 위한 특별 강연
                연사: 김영환 지사 (충청북도)
                16:00 – 16:40 | Session 4: 사람이 답이다
                사람의 결에서 경영의 길을 찾다 - 현장 Q&A
                연사: 이형우 회장 (마이다스그룹)
                16:40 – 17:00: 설문 및 경품 추첨 (EVENT)
                참가 기회는 선착순 300명으로 한정되어 있으니, 지금 바로 신청하세요!
                이 포럼을 통해 미래 경영의 방향을 제시할 최신 트렌드와 혜안을 만나보세요!
                지금 바로 아래 링크를 통해 신청하세요!
                **예시 텍스트:**\n[고객님의 회사명], 인사/채용 관리를 간소화하세요 – 지금 가입하고 [특별 혜택]을 받으세요!\n[헤더]\n[회사 로고]\n안녕하세요, [고객님 이름]님!\n[고객님의 회사명]의 HR/채용 관리를 한층 더 간편하게 만들어줄 솔루션, 지금 바로 경험해 보세요! 회원가입만 하셔도 아래 혜택을 누리실 수 있습니다.\n[혜택 안내]\n\n할인 혜택: 자사 솔루션 1년 이용료 최대 20% 할인\n주요 자료 제공: 채용 성과를 높이는 가이드 무료 제공\n경품 이벤트: 가입 고객 대상 경품 추첨 이벤트(노트북, 스마트워치 등)\n지금 바로 가입하시고, 인사 관리의 모든 과정을 효율적으로 자동화해 보세요!\n[CTA 버튼]\n지금 가입하고 혜택 받기 [링크 삽입]\n[푸터]\n[회사 로고 및 주소]\n문의사항이 있으시면 언제든지 연락 주십시오.\n[소셜 미디어 링크 및 구독 해지 옵션]"""
        
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
    # 예상된 탭 값이 아닌 경우 기본 프롬프트 설정
    else:
        prompt = f"""
        # Instruction
        입력된 탭 값이 유효하지 않습니다. 올바른 탭 값을 선택해 주세요.
        # Context
        - 지원되는 탭: 'event_edm', 'promotion_edm', 'landing_page'.
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
