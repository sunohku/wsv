import pandas as pd
from supabase import create_client, Client

# --- 1. Supabaseの接続設定 ---
SUPABASE_URL = "https://wkrwvgqicurgmcsitsum.supabase.co"
# 新しいPublishable key（または必要に応じてお手元の正しいキー）を設定
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indrcnd2Z3FpY3VyZ21jc2l0c3VtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4OTAzMDM4OCwiZXhwIjoyMTA0NjA2Mzg4fQ.Mo9wOX3Hm3OHH9y4PFOdwy7objpAoF6XzQHr1Co7vXM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. 完成版エクセルファイルの読み込み（検証済みの header=2 を確実に指定） ---
excel_path = "downloads_自治会データ統合_緯度経度付き完全版2.xlsx"
df = pd.read_excel(excel_path, header=2)

# --- 3. Supabaseのテーブル定義と完全に一致させたデータ変換 ---
records = []
for _, row in df.iterrows():
    # 名前が空（NaN）または空白の行は完全にスキップする安全策
    name_val = row.get('名前')
    if pd.isna(name_val) or str(name_val).strip() == '' or str(name_val).startswith('nan'):
        continue
        
    record = {
        "ban": str(row.get('班', '')) if pd.notna(row.get('班')) else "",
        "position": str(row.get('役職', '')) if pd.notna(row.get('役職')) else "",
        "name": str(name_val).strip(),
        "landline": str(row.get('黒電話', '')) if pd.notna(row.get('黒電話')) else "",
        "mobile": str(row.get('スマホ', '')) if pd.notna(row.get('スマホ')) else "",
        "koshihikari": int(row.get('コシヒカリ', 0)) if pd.notna(row.get('コシヒカリ')) else 0,
        "tentakaku": int(row.get('てんたかく', 0)) if pd.notna(row.get('てんたかく')) else 0,
        "algis": int(row.get('アルギット', 0)) if pd.notna(row.get('アルギット')) else 0,
        "fufufu": int(row.get('富富富', 0)) if pd.notna(row.get('富富富')) else 0,
        "point_x": float(row.get('POINT_X')) if pd.notna(row.get('POINT_X')) else None,
        "point_y": float(row.get('POINT_Y')) if pd.notna(row.get('POINT_Y')) else None,
        "latitude": float(row.get('緯度')) if pd.notna(row.get('緯度')) else None,
        "longitude": float(row.get('経度')) if pd.notna(row.get('経度')) else None,
        "abbreviation": str(row.get('略称', '')) if pd.notna(row.get('略称')) else ""
    }
    records.append(record)

print(f"📌 抽出された有効なレコード数: {len(records)} 件")

# --- 4. Supabaseへ一括インサート（登録）実行 ---
try:
    if len(records) > 0:
        response = supabase.table("neighborhood_data").insert(records).execute()
        print("✨ Supabaseへのデータ登録が完全に成功しました！", response)
    else:
        print("⚠️ 登録対象となる有効なデータが見つかりませんでした。")
except Exception as e:
    print("❌ エラーが発生しました:", e)