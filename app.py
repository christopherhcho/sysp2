from flask import Flask, render_template, request
import logging

app = Flask(__name__)

# 기본 페이지 라우팅
@app.route('/')
def home():
    return render_template('index.html')

# POST 요청을 처리하는 엔드포인트
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # 클라이언트에서 전송된 JSON 데이터 받기
    input_text = data.get('inputText', '')  # 입력된 텍스트 추출
    print(f"서버에 입력된 텍스트: {input_text}")  # 서버 콘솔에 로그 출력
    return {'message': '연결됐습니다.'}, 200  # 응답

if __name__ == '__main__':
    # 서버 실행
    app.run(debug=True, port=8070)
