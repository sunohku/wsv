import json
import firebase_admin
from firebase_admin import credentials, firestore
from supabase import create_client

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

SUPABASE_URL = "https://wkrwvqgicurgmcsitsum.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_enXIXvGovfpaS6QoceRYyA_6VDBUPag"
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def migrate():
    print("Firebaseからデータを取得開始...")
    docs = db.collection("farms").stream()
    count = 0
    
    for doc in docs:
        doc_id = doc.id
        print(f"処理中のドキュメント: {doc_id}")
        data = doc.to_dict()
        
        geometry_json = data.get("geometry_json")
        if isinstance(geometry_json, dict):
            geometry_json = json.dumps(geometry_json)
            
        properties = data.get("properties", {})
        
        row_data = {
            "id": doc_id,
            "geometry_json": geometry_json,
            "properties": properties
        }
        
        # Supabaseへの書き込み
        supabase.table("farms").upsert(row_data).execute()
        count += 1
        print(f" -> 移行完了: {doc_id}")
        
    print(f"全 {count} 件のデータ移行が完了しました！")

if __name__ == "__main__":
    migrate()