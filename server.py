from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# 根元（http://localhost:8080/）にアクセスされたら map.html を返す
@app.route('/')
def index():
    return send_from_directory('.', 'map.html')

# 【追加】任意のHTMLファイルや静的ファイルを直接URLで開けるようにする汎用窓口
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

# GeoJSONファイルを求められたら安全に返す窓口
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

# 作業日誌からCSVファイル名の保存要求を受け取る窓口
@app.route('/save-log', methods=['POST'])
def save_log():
    try:
        data = request.json
        file_name = data.get('fileName')
        content = data.get('content')
        
        if not file_name or not content:
            return jsonify({"status": "error", "message": "データが不正です。"}), 400
            
        # サーバーと同じフォルダにCSVファイルを書き込む
        file_path = os.path.join('.', file_name)
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(content)
            
        return jsonify({"status": "success", "message": "ログの保存に成功しました！"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)