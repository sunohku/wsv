from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# 根元（http://localhost:8080/）にアクセスされたら map.html を返す
@app.route('/')
def index():
    return send_from_directory('.', 'map.html')

# 【追加】GeoJSONファイルを求められたら安全に返す窓口
@app.route('/品目_4326.geojson')
def get_geojson():
    return send_from_directory('.', '品目_4326.geojson')

# スマホの地図から「保存」が送られてきたときに受け取る窓口
@app.route('/save', methods=['POST'])
def save_geojson():
    try:
        new_data = request.json
        file_path = '品目_4326.geojson'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
            
        return jsonify({"status": "success", "message": "保存に成功しました！"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)