import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

# ==== 1. Kết nối Spotify API ====
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id="75b20bbcd32e44eaba375723e2810634",
    client_secret="d9c33160ec9a4b0abf60aecb340369db"
))

# ==== 2. Đọc file CSV, lấy 20 bài đầu ====
df = pd.read_csv("spotify_clean.csv").head(20000)
'''
# ==== 3. Hàm lấy ngày phát hành ====
def get_release_date(track_id):
    try:
        track = sp.track(track_id)
        return track["album"]["release_date"]
    except Exception as e:
        print(f"Lỗi {track_id}: {e}")
        return None

# ==== 4. Thêm cột 'date' ====
tqdm.pandas(desc="Fetching release dates (20 tracks)")
df["date"] = df["track_id"].progress_apply(get_release_date)

# ==== 5. In hoặc lưu kết quả ====
print(df[["track_name", "album_name", "date"]])
df.to_csv("spotify_test_20_with_date.csv", index=False)
print("✅ Done! Đã lưu file test có 20 bài với cột date.")
'''
release_dates = []

for i in tqdm(range(0, len(df), 50), desc="Fetching in batch (50 tracks each)"):
    batch_ids = df["track_id"].iloc[i:i+50].tolist()
    try:
        results = sp.tracks(batch_ids)
        for t in results["tracks"]:
            if t is not None:
                release_dates.append(t["album"]["release_date"])
            else:
                release_dates.append(None)
    except Exception as e:
        print(f"Lỗi tại batch {i}: {e}")
        release_dates.extend([None] * len(batch_ids))  # để giữ đúng độ dài

df["date"] = release_dates
print("✅ Thêm cột 'date' thành công!")
df.to_csv("spotify_test_20_with_date.csv", index=False)