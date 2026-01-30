
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------
# 1️⃣ Load & Clean Data
# --------------------------
df = pd.read_csv("songs_normalize.csv")

# Chuẩn hoá dữ liệu cơ bản
df['artist'] = df['artist'].astype(str).str.strip()
df['year'] = df['year'].astype(int)

# 🔹 Lọc dữ liệu: chỉ giữ các năm 2000–2020 (loại biên thiếu dữ liệu)
df = df[(df['year'] > 2000) & (df['year'] < 2020)].copy()

# Hàm chia giai đoạn 5 năm
def year_bin(y):
    return f"{(y // 5) * 5}-{(y // 5) * 5 + 4}"

df['period'] = df['year'].apply(year_bin)

sns.set(style="whitegrid", font_scale=1.1)

# ===============================================================
# Xu hướng audio feature của các bài hát qua năm các năm (Biểu đồ đường)
# ===============================================================
feature_cols = ['danceability', 'energy', 'acousticness', 'valence','speechiness' ,'acousticness', 'instrumentalness' ,'liveness']
yearly_avg = df.groupby('year')[feature_cols].mean().reset_index()

plt.figure(figsize=(10,6))
for col in feature_cols:
    plt.plot(yearly_avg['year'], yearly_avg[col], marker='o', label=col.capitalize())

plt.title("Xu hướng các audio feature trung bình qua các năm (2000–2020)", fontsize=14)
plt.xlabel("Năm")
plt.ylabel("Giá trị trung bình")
plt.legend(title="Feature")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
# ===============================================================
# Xu hướng nhịp độ các bài hát xu hướng trung bình qua năm (Biểu đồ đường)
# ===============================================================
feature_cols = ['tempo']
yearly_avg = df.groupby('year')[feature_cols].mean().reset_index()

plt.figure(figsize=(10,6))
for col in feature_cols:
    plt.plot(yearly_avg['year'], yearly_avg[col], marker='o', label=col.capitalize())

plt.title("Nhịp độ trung bình qua các năm (2000–2020)", fontsize=14)
plt.xlabel("Năm")
plt.ylabel("Giá trị trung bình")
plt.legend(title="Feature")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ===============================================================
# Nghệ sĩ nổi bật mỗi giai đoạn 5 năm (Biểu đồ thanh ngang)
# ===============================================================
artist_period_counts = (
    df.groupby(['period', 'artist'])
    .size()
    .reset_index(name='count')
)

# Lấy top 3 nghệ sĩ mỗi giai đoạn
top3_each_period = (
    artist_period_counts.groupby('period', group_keys=False)
    .apply(lambda x: x.nlargest(3, 'count'))
    .reset_index(drop=True)
)

plt.figure(figsize=(9,5))
sns.barplot(
    data=top3_each_period,
    x='count',
    y='artist',
    hue='period',
    palette='Set2'
)
plt.title("Top 3 nghệ sĩ có nhiều bài nhất mỗi giai đoạn 5 năm (2001–2019)", fontsize=14)
plt.xlabel("Số bài hát trong top")
plt.ylabel("Nghệ sĩ")
plt.legend(title="Giai đoạn", bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

# ===============================================================
# 4️⃣ Độ phổ biến trung bình theo năm (Bar Plot)
# ===============================================================
plt.figure(figsize=(10,6))

popularity_by_year = df.groupby('year')['popularity'].mean().reset_index()

sns.barplot(
    data=popularity_by_year,
    x='year',
    y='popularity',
    palette='pastel'
)

plt.title("Độ phổ biến trung bình của bài hát theo năm (2000–2020)", fontsize=14)
plt.xlabel("Năm")
plt.ylabel("Popularity trung bình")
plt.tight_layout()
plt.show()

# ===============================================================
# Phân bố thể loại nhạc qua các giai đoạn (Biểu đồ cột)
# ===============================================================
# Lấy thể loại chính (chỉ phần đầu tiên trong chuỗi)
df['main_genre'] = df['genre'].str.split(',').str[0].str.strip()

genre_period = (
    df.groupby(['period', 'main_genre'])
    .size()
    .reset_index(name='count')
)

plt.figure(figsize=(10,6))
sns.barplot(
    data=genre_period,
    x='period',
    y='count',
    hue='main_genre',
    palette='tab10'
)
plt.title("Phân bố thể loại nhạc qua các giai đoạn 5 năm (2000–2020)", fontsize=14)
plt.xlabel("Giai đoạn")
plt.ylabel("Số lượng bài trong top")
plt.legend(title="Thể loại", bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

# ===============================================================
# Độ dài trung bình bài hát theo năm (Biểu đồ đường, đơn vị: phút)
# ===============================================================

# Chuyển duration từ milliseconds → phút
df['duration_min'] = df['duration_ms'] / 60000  # 1 phút = 60000 ms

# Tính trung bình theo năm
duration_by_year = df.groupby('year')['duration_min'].mean().reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(
    data=duration_by_year,
    x='year',
    y='duration_min',
    marker='o',
    color='coral'
)

plt.title("Độ dài trung bình bài hát theo năm (2000–2020)", fontsize=14)
plt.xlabel("Năm")
plt.ylabel("Thời lượng trung bình (phút)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()