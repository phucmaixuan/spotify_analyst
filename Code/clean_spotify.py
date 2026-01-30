import pandas as pd
# Đọc file
df_spotify = pd.read_csv("spotify.csv")
# Thông tin tổng quan
print("=== Tổng quan dữ liệu ===")
print(df_spotify.info())
print("\nKích thước dữ liệu:", df_spotify.shape)
# Kiểm tra giá trị thiếu (missing values)
print("\n=== Số lượng giá trị thiếu trên mỗi cột ===")
print(df_spotify.isna().sum())
# Tính tỉ lệ thiếu
missing_ratio = (df_spotify.isna().sum() / len(df_spotify)) * 100
print("\n=== Tỉ lệ thiếu (%) ===")
print(missing_ratio[missing_ratio > 0])
# Kiểm tra dữ liệu trùng
duplicates = df_spotify.duplicated(subset=["track_id"]).sum()
print(f"\nSố bản ghi trùng track_id: {duplicates}")
# Kiểm tra kiểu dữ liệu
print("\n=== Kiểu dữ liệu từng cột ===")
print(df_spotify.dtypes)
# Làm sạch cơ bản
# - Loại bỏ bản ghi thiếu track_name hoặc artists
df_spotify.dropna(subset=["track_name", "artists"], inplace=True)
# - Loại bỏ bản ghi trùng
df_spotify.drop_duplicates(subset=["track_name","artists"], inplace=True)
# - Chuyển kiểu dữ liệu phù hợp
df_spotify["explicit"] = df_spotify["explicit"].astype(bool)
audio_features = [
    "popularity", "duration_ms", "danceability", "energy", "key", "loudness",
    "mode", "speechiness", "acousticness", "instrumentalness",
    "liveness", "valence", "tempo", "time_signature"
]
df_spotify[audio_features] = df_spotify[audio_features].apply(pd.to_numeric, errors="coerce")
# - Thay NaN trong cột không quan trọng (album_name, track_genre) bằng "Unknown"
df_spotify["album_name"].fillna("Unknown", inplace=True)
df_spotify["track_genre"].fillna("Unknown", inplace=True)
# Xuất kết quả sau làm sạch
print("\n=== Sau khi làm sạch ===")
print("Kích thước mới:", df_spotify.shape)
print("Giá trị thiếu sau xử lý:")
print(df_spotify.isna().sum().sum(), "giá trị thiếu còn lại.")
# xuất file làm sạch thành 'spotify_clean.csv'
df_spotify.to_csv("spotify_clean.csv", index=False)