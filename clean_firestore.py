import firebase_admin
from firebase_admin import credentials, firestore

# Firebaseの初期化（お手元の認証ファイル名を指定してください）
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def clean_farm_properties():
    print("Firestoreのデータクレンジングを開始します...")
    
    # 削除したいキーのリスト
    target_keys_to_remove = ["下水", "幅員", "数値1桁", "歩道", "舗装", "融雪"]
    
    docs = db.collection("farms").stream()
    count = 0
    updated_count = 0
    
    for doc in docs:
        doc_id = doc.id
        data = doc.to_dict()
        properties = data.get("properties", {})
        
        modified = False
        # properties 内から対象のキーを削除
        for key in target_keys_to_remove:
            if key in properties:
                del properties[key]
                modified = True
                
        # もしルート階層に直接キーがあればそれも削除対象にする
        for key in target_keys_to_remove:
            if key in data:
                del data[key]
                modified = True

        # 変更があった場合のみFirestoreを更新
        if modified:
            db.collection("farms").document(doc_id).set(data)
            print(f" -> クレンジング実行: {doc_id}")
            updated_count += 1
            
        count += 1
        
    print(f"全 {count} 件中、{updated_count} 件のドキュメントをクレンジングしました！")

if __name__ == "__main__":
    clean_farm_properties()