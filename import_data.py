import time
import pandas as pd
import requests
from supabase import create_client

# ★ご自身のSupabaseプロジェクトのURLとキーに書き換えてください
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-service-role-or-anon-key"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 国土地理院のジオコーディングAPIを使って住所から緯度経度を取得する関数
def get_latlon(address):
    url = f"https://msearch.gsi.go.jp/address-search/AddressSearch?q={address}"
    try:
        res = requests.get(url)
        data = res.json()
        if data and len(data) > 0:
            lon, lat = data[0]["geometry"]["coordinates"]
            return lat, lon
    except Exception as e:
        print(f"Error for {address}: {e}")
    return None, None

# Excelファイルの読み込み（Sheet2を指定）
excel_path = "米配達先.xlsx"
df = pd.read_excel(excel_path, sheet_name="Sheet2")

# 各行のデータを処理
for index, row in df.iterrows():
    no = int(row["No"])
    name = str(row["氏名"]).strip()
    address = str(row["住所"]).strip()
    phone = str(row["電話番号"]) if pd.notna(row["電話番号"]) else None
    
    # 住所に「富山県」を補うと検索ヒット率が上がります
    search_address = f"富山県{address}" if not address.startswith("富山県") else address
    lat, lon = get_latlon(search_address)
    
    print(f"[{no}] {name} ({search_address}) -> 緯度: {lat}, 経度: {lon}")
    
    record = {
        "no": no,
        "name": name,
        "address": address,
        "phone": phone,
        "latitude": lat,
        "longitude": lon
    }
    
    try:
        supabase.table("delivery_locations").insert(record).execute()
    except Exception as e:
        print(f"Insert error: {e}")
        
    time.sleep(0.4) # APIに配慮して少しウェイト

print("すべてのデータの処理とSupabaseへの登録が完了しました！")