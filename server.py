from flask import Flask, jsonify, request
from flask_cors import CORS
import test

app = Flask(__name__)
CORS(app)

@app.route('/get_participants/<path:url>', methods=['GET'])
def get_participants(url):
    participants = test.extract_participants(url)
    return jsonify(participants)

@app.route('/get_rating_change/', methods=['POST'])
def get_rating_change():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    else:
        data = request.json
        fide_ids = data.get('fide_ids', [])
        rating_changes = test.get_performance_data(fide_ids)
        return jsonify(rating_changes)

def build_cors_preflight_response():
    response = jsonify({'message': 'CORS preflight response'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

if __name__ == '__main__':
    app.run(debug=True, port =5000)
