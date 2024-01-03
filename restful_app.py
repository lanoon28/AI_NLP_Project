from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS Error 대응
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    return response

@app.route('/api/data', methods=['GET'])
    # JSON 형태의 데이터 생성
def get_data():
    data = {
        'avg_esti' : '70',
        'detail_info' : 'detail_info_sentence',
        '202301': '10',
        '202302': '20',
        '202303': '80',
        '202304': '30',
        '202305': '40',
        '202306': '50'
    }

    print("data : ", data)
    print("type : ", type(data))
    print(jsonify(data))
    print("j type : ", type(jsonify(data)))

    # JSON 데이터를 응답으로 전송
    return jsonify(data)


# # GET 요청을 처리하는 엔드포인트
# @app.route('/api/data', methods=['GET'])
# def get_data():
#     # JSON 형태의 데이터 생성
#     data = {
#         'key1': 'value1',
#         'key2': 'value2',
#         'key3': 'value3'
#     }

#     print(data)
#     print(jsonify(data))

#     # JSON 데이터를 응답으로 전송
#     return jsonify(data)

if __name__ == '__main__':
    # 서버 실행
    app.run(debug=True)

