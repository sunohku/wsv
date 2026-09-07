import json
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Firebaseの初期化
if not firebase_admin._apps:
  cred = credentials.Certificate("serviceAccountKey.json")
  firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. GeoJSONファイルの読み込み
geojson_path = "品目5_4326.geojson"
print(f"{geojson_path} を読み込んでいます...")

with open(geojson_path, "r", encoding="utf-8") as f:
  geojson_data = json.load(f)

# 3. Firestoreへのデータ登録
collection_ref = db.collection("farms")
features = geojson_data.get("features", [])
print(
    f"合計 {len(features)} 件のデータを検出しました。インポートを開始します..."
)

for i, feature in enumerate(features):
  doc_id = f"feature_{i+1}"

  # Firestoreのネスト制限を回避するため、geometryをJSON文字列（テキスト）として安全に格納します
  geometry_data = feature.get("geometry", {})
  properties_data = feature.get("properties", {})

  safe_feature = {
      "type": feature.get("type", "Feature"),
      "properties": properties_data,
      "geometry_json": json.dumps(geometry_data),
  }

  collection_ref.document(doc_id).set(safe_feature)
  print(f"[{i+1}/{len(features)}] 登録完了: {doc_id}")

print("すべてのGeoJSONデータのインポートが完了しました！")