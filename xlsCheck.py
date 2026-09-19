import pandas as pd

# ファイルの読み込み確認
excel_path = "downloads_自治会データ統合_緯度経度付き完全版2.xlsx"
xls = pd.ExcelFile(excel_path)
print("【シート名一覧】", xls.sheet_names)

df = pd.read_excel(excel_path)
print("\n【実際の列名一覧（カラム）】")
print(df.columns.tolist())

print("\n【先頭3行のデータ（確認用）】")
print(df.head(3))