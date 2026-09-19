import pandas as pd
from pyproj import Transformer

# 1. Excelファイルの読み込み（すべてのシートを取得）
file_path = "Book4.xlsx"
excel_file = pd.ExcelFile(file_path)
print("検出されたシート:", excel_file.sheet_names)

# 各シートをデータフレームとして読み込み
sheets = {s: pd.read_excel(file_path, sheet_name=s) for s in excel_file.sheet_names}

# 2. 「名前」列を基準に全シートを外部結合（outer join）でマージ
# ※シート内の名前列の列名が共通（例: '名前' または '名称' など）であることをご確認ください
merged_df = None
for name, df in sheets.items():
    if merged_df is None:
        merged_df = df
    else:
        # 重複する列名がある場合は区別するための接尾辞を付与
        merged_df = pd.merge(merged_df, df, on="名前", how="outer", suffixes=("", f"_{name}"))

# 3. 座標系の処理（平面直角座標系 第7系 JGD2000 -> 緯度・経度への変換例）
# 第7系のEPSGコードは 'EPSG:2449' です。
# POINT_X（北距）、POINT_Y（東距）が存在する場合、WGS84の緯度・経度に変換して列を追加します。
if 'POINT_X' in merged_df.columns and 'POINT_Y' in merged_df.columns:
    # EPSG:2449 (JGD2000 / Plane rectangular coordinate system VII) から EPSG:4326 (WGS84 緯度経度) へ変換
    # always_xy=True により、transform(経度/東距, 緯度/北距) の順序で指定します
    transformer = Transformer.from_crs("EPSG:2449", "EPSG:4326", always_xy=True)
    
    # 欠損値を除外して一括変換
    valid_mask = merged_df['POINT_X'].notna() & merged_df['POINT_Y'].notna()
    
    if valid_mask.any():
        # 第7系は Yが東距(East)、Xが北距(North)
        lons, lats = transformer.transform(
            merged_df.loc[valid_mask, 'POINT_Y'].values, 
            merged_df.loc[valid_mask, 'POINT_X'].values
        )
        merged_df.loc[valid_mask, 'Lon_WGS84'] = lons
        merged_df.loc[valid_mask, 'Lat_WGS84'] = lats

# 4. 編集可能なExcelファイルとして出力
output_filename = "merged_output.xlsx"
merged_df.to_excel(output_filename, index=False)
print(f"マージ完了！ '{output_filename}' として保存されました。")