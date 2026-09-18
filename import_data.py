import time
import pandas as pd
import requests
from supabase import create_client

# c.html から分かった正しいプロジェクトURLを設定
SUPABASE_URL = "https://wkrwvgqicurgmcsitsum.supabase.co"
# SupabaseのAPIキー（設定画面の anon public または service_role キー）
SUPABASE_KEY = "sb_publishable_enXIXvGovfpaS6QoceRYyA_6VDBUPag"

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

print("データ登録を開始します...")

# 各行のデータを処理
for index, row in df.iterrows():
    no = int(row["No"])
    name = str(row["氏名"]).strip()
    address = str(row["住所"]).strip()
    phone = str(row["電話番号"]) if pd.notna(row["電話番号"]) else None
    
    # 住所に「富山県」を補う
    search_address = f"富山県{address}" if not address.startswith("富山県") else address
    lat, lon = get_latlon(search_address)
    
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
        print(f"[{no}] {name} -> 登録成功！ (緯度: {lat}, 経度: {lon})")
    except Exception as e:
        print(f"[{no}] {name} -> Insert error: {e}")
        
    time.sleep(0.3)

print("すべての処理が完了しました！")