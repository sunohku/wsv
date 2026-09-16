import json
import firebase_admin
from firebase_admin import credentials, firestore

# Firebaseの初期化
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def generate_sql():
    print("Firebaseからデータを取得してSQLを生成しています...")
    docs = db.collection("farms").stream()
    
    sql_lines = []
    count = 0
    
    for doc in docs:
        doc_id = doc.id
        data = doc.to_dict()
        
        # ジオメトリデータの処理
        geometry_json = data.get("geometry_json")
        if isinstance(geometry_json, dict):
            geometry_json = json.dumps(geometry_json)
            
        properties = data.get("properties", {})
        
        # SQLの文字列として安全に埋め込めるようにシングルクォートをエスケープ
        escaped_id = doc_id.replace("'", "''")
        
        if geometry_json:
            # geometry_json 自体をエスケープ
            geo_val = f"'{str(geometry_json).replace("'", "''")}'"
        else:
            geo_val = "NULL"
            
        # properties（jsonb型）をJSON文字列に変換
        props_str = json.dumps(properties, ensure_ascii=False).replace("'", "''")
        
        # PostgreSQLのUPSERT（重複時は上書き）構文のINSERT文を作成
        sql = (
            f"INSERT INTO farms (id, geometry_json, properties) "
            f"VALUES ('{escaped_id}', {geo_val}, '{props_str}'::jsonb) "
            f"ON CONFLICT (id) DO UPDATE SET "
            f"geometry_json = EXCLUDED.geometry_json, "
            f"properties = EXCLUDED.properties;"
        )
        sql_lines.append(sql)
        count += 1
        
    # insert_data.sql という名前でファイルに保存
    with open("insert_data.sql", "w", encoding="utf-8") as f:
        f.write("\n".join(sql_lines))
        
    print(f"\n完了！全 {count} 件分のデータを 'insert_data.sql' に書き出しました。")

if __name__ == "__main__":
    generate_sql()