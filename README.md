# 🎵 Spotify Music Analytics - Data Engineering Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![SQL Server](https://img.shields.io/badge/SQL_Server-2019+-red.svg)
![Power BI](https://img.shields.io/badge/Power_BI-Latest-yellow.svg)
![License](https://img.shields.io/badge/License-Academic-green.svg)

**Đồ án Tổng hợp - Hệ Kĩ Thuật Dữ Liệu**

Trường Đại học Bách Khoa - ĐHQG TP.HCM

</div>

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng chính](#-tính-năng-chính)
- [Kiến trúc hệ thống](#️-kiến-trúc-hệ-thống)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Cài đặt](#-cài-đặt)
- [Sử dụng](#-sử-dụng)
- [Phân tích dữ liệu](#-phân-tích-dữ-liệu)
- [Machine Learning](#-machine-learning)
- [Dashboard](#-dashboard)
- [Thành viên nhóm](#-thành-viên-nhóm)
- [Tài liệu tham khảo](#-tài-liệu-tham-khảo)

---

## 🎯 Giới thiệu

Dự án xây dựng **hệ thống kỹ thuật dữ liệu hoàn chỉnh** để thu thập, xử lý, phân tích và dự đoán xu hướng âm nhạc từ **Spotify** - một trong những nền tảng nghe nhạc lớn nhất thế giới với hàng trăm triệu người dùng.

### 🎯 Mục tiêu

- Thu thập và tích hợp dữ liệu từ **3 nguồn** khác nhau (Spotify API, Kaggle, Billboard Charts)
- Xây dựng **Data Warehouse** theo kiến trúc Bronze-Silver-Gold
- Phân tích xu hướng âm nhạc qua **20+ năm** (2000-2024)
- Dự đoán độ phổ biến của bài hát bằng **Machine Learning**
- Trực quan hóa dữ liệu với **Power BI Dashboard**

### 📊 Quy mô dữ liệu

- **75,892** bài hát đã xử lý
- **2,000+** bài hát trending (Billboard Charts)
- **15+** đặc trưng âm nhạc (danceability, energy, valence, tempo, etc.)
- Phân tích **5 giai đoạn** (2000-2004, 2005-2009, 2010-2014, 2015-2019, 2020-2024)

---

## ✨ Tính năng chính

### 🔄 ETL Pipeline
- **Bronze Layer**: Nạp dữ liệu thô từ CSV và API
- **Silver Layer**: Làm sạch, chuẩn hóa, khử trùng lặp
- **Gold Layer**: Mô hình Star Schema với Fact/Dimension tables

### 📈 Phân tích dữ liệu
- Phân tích xu hướng âm nhạc theo thời gian
- Ma trận tương quan giữa các đặc trưng
- Top nghệ sĩ, thể loại, bài hát phổ biến
- Phân tích độ dài bài hát, tempo, năng lượng

### 🤖 Machine Learning
- **3 mô hình**: Logistic Regression, Random Forest, XGBoost
- Dự đoán bài hát trending với độ chính xác **84%** (validation)
- Multi-label classification cho thể loại nhạc
- Temporal split để tránh data leakage

### 📊 Dashboard & Visualization
- Interactive Power BI Dashboard
- Real-time insights về xu hướng âm nhạc
- Phân tích theo nghệ sĩ, thể loại, năm phát hành

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
├─────────────────┬─────────────────┬───────────────────────────┤
│  Spotify API    │  Kaggle Dataset │  Billboard Charts         │
│  (Metadata)     │  (Audio Features)│  (Trending Songs)         │
└────────┬────────┴────────┬────────┴────────┬──────────────────┘
         │                 │                 │
         v                 v                 v
┌─────────────────────────────────────────────────────────────────┐
│                    BRONZE LAYER (Raw Data)                       │
│                    - Spotify_Raw.csv                             │
│                    - songs_normalize.csv                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               v
┌─────────────────────────────────────────────────────────────────┐
│                    SILVER LAYER (Cleaned Data)                   │
│  - Safe Type Casting (TRY_CAST)                                 │
│  - Deduplication (ROW_NUMBER)                                   │
│  - Multi-valued Attributes Handling                             │
│  - Data Validation (UDF Functions)                              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               v
┌─────────────────────────────────────────────────────────────────┐
│                     GOLD LAYER (Star Schema)                     │
│                                                                  │
│         ┌─────────────┐          ┌─────────────┐               │
│         │ DimTrack    │          │ DimArtist   │               │
│         └──────┬──────┘          └──────┬──────┘               │
│                │                        │                       │
│         ┌──────┴────────────────────────┴──────┐               │
│         │         FactSongFeatures              │               │
│         │  - track_id_sk (FK)                   │               │
│         │  - artist_id_sk (FK)                  │               │
│         │  - popularity, energy, danceability   │               │
│         └──────┬────────────────────────────────┘               │
│                │                        │                       │
│         ┌──────┴──────┐          ┌──────┴──────┐               │
│         │ DimPlaylist │          │  DimAlbum   │               │
│         └─────────────┘          └─────────────┘               │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               v
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYTICS & ML LAYER                          │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  Power BI        │         │  ML Models       │             │
│  │  Dashboard       │         │  - XGBoost       │             │
│  │                  │         │  - Random Forest │             │
│  └──────────────────┘         └──────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Công nghệ sử dụng

### Database & Storage
- **Microsoft SQL Server** - Data Warehouse
- **SQL Server Management Studio (SSMS)** - Database Administration
- **T-SQL** - ETL Processing

### Data Processing
- **Python 3.8+**
  - `pandas` - Data manipulation
  - `numpy` - Numerical computing
  - `requests` - API calls
  - `spotipy` - Spotify API wrapper

### Machine Learning
- **scikit-learn** - ML algorithms & preprocessing
- **XGBoost** - Gradient boosting
- **matplotlib, seaborn** - Data visualization

### Business Intelligence
- **Power BI Desktop** - Dashboard creation
- **DAX** - Advanced calculations

### Data Sources
- **Spotify Web API** - Real-time metadata
- **Kaggle** - Historical datasets
- **Billboard Charts** - Trending songs

---

## 📦 Cài đặt

### Yêu cầu hệ thống

- Python 3.8 trở lên
- SQL Server 2019 trở lên
- Power BI Desktop (phiên bản mới nhất)
- Tối thiểu 8GB RAM
- 5GB ổ cứng trống

### Bước 1: Clone repository

```bash
git clone https://github.com/your-username/spotify-data-engineering.git
cd spotify-data-engineering
```

### Bước 2: Cài đặt Python dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
scikit-learn==1.3.0
xgboost==1.7.6
spotipy==2.23.0
requests==2.31.0
python-dotenv==1.0.0
```

### Bước 3: Cấu hình Spotify API

1. Tạo ứng dụng tại [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Lấy `Client ID` và `Client Secret`
3. Tạo file `.env`:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### Bước 4: Thiết lập SQL Server

1. Mở SSMS và kết nối đến SQL Server
2. Chạy script tạo database:

```sql
CREATE DATABASE SpotifyDataWarehouse;
GO

USE SpotifyDataWarehouse;
GO

-- Tạo schemas
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
GO
```

3. Chạy các script khởi tạo bảng từ thư mục `sql/`

---

## 🚀 Sử dụng

### 1. Thu thập dữ liệu

#### Từ Spotify API:
```bash
python scripts/01_collect_spotify_data.py
```

#### Từ Kaggle:
```bash
# Download manually từ Kaggle hoặc sử dụng Kaggle API
kaggle datasets download -d melissamonfared/spotify-tracks-attributes-and-popularity
```

### 2. ETL Pipeline

#### Bronze Layer (Nạp dữ liệu thô):
```bash
python scripts/02_load_bronze.py
```

#### Silver Layer (Làm sạch):
```sql
-- Chạy trong SSMS
EXEC silver.sp_clean_and_deduplicate;
```

#### Gold Layer (Dimensional Model):
```sql
-- Chạy trong SSMS
EXEC gold.sp_build_star_schema;
```

### 3. Phân tích dữ liệu

```bash
python scripts/03_analyze_data.py
```

Kết quả:
- Ma trận tương quan theo giai đoạn
- Biểu đồ xu hướng âm nhạc
- Phân tích thể loại, nghệ sĩ

### 4. Huấn luyện mô hình ML

```bash
python scripts/04_train_ml_models.py
```

Output:
- `model_comparison_validation.csv` - Kết quả trên tập validation
- `model_comparison_test.csv` - Kết quả trên tập test
- `model_comparison_overall.csv` - Kết quả tổng thể
- `predictions_xgboost.csv` - Dự đoán từ mô hình tốt nhất

### 5. Mở Dashboard

1. Mở file `dashboard/Spotify_Analytics.pbix` bằng Power BI Desktop
2. Refresh data sources
3. Explore interactive visualizations!

---

## 📊 Phân tích dữ liệu

### Xu hướng theo thời gian (2000-2024)

#### Giai đoạn 2000-2004
- **Đặc trưng nổi bật**: Loudness (+0.18), Instrumentalness (-0.28)
- **Xu hướng**: Nhạc Pop/Rock mạnh mẽ, có năng lượng cao
- **Số bài hát**: 4,022

#### Giai đoạn 2005-2009
- **Đặc trưng nổi bật**: Loudness (+0.15), Speechiness (-0.14)
- **Xu hướng**: YouTube ra đời, nhạc số bùng nổ
- **Số bài hát**: 6,253

#### Giai đoạn 2010-2014
- **Đặc trưng nổi bật**: Energy (-0.07), Liveness (-0.07)
- **Xu hướng**: Streaming xuất hiện, đa dạng hóa thể loại
- **Số bài hát**: 10,139

#### Giai đoạn 2015-2019
- **Đặc trưng nổi bật**: Duration_ms (-0.11), Danceability (+0.09)
- **Xu hướng**: TikTok, bài hát ngắn gọn, nhịp điệu nhanh
- **Số bài hát**: 19,762 (tăng 100% so với giai đoạn trước!)

#### Giai đoạn 2020-2024
- **Đặc trưng nổi bật**: Danceability (+0.10), Duration_ms (-0.09)
- **Xu hướng**: Cá nhân hóa, cảm xúc tích cực, video ngắn
- **Số bài hát**: 23,666

### Phát hiện chính

| Đặc trưng | Tương quan với Popularity | Ý nghĩa |
|-----------|---------------------------|---------|
| **Danceability** | +0.09 ~ +0.10 | Bài hát dễ nhảy có xu hướng phổ biến hơn |
| **Loudness** | +0.08 ~ +0.18 | Âm thanh mạnh mẽ thu hút người nghe |
| **Instrumentalness** | -0.17 ~ -0.28 | Nhạc không lời ít phổ biến hơn |
| **Duration** | -0.09 ~ -0.11 | Bài hát ngắn dễ viral hơn (đặc biệt từ 2015) |
| **Tempo** | Tăng dần | Nhịp độ trung bình tăng từ ~115 lên ~122 BPM |

---

## 🤖 Machine Learning

### Bài toán

**Phân loại nhị phân**: Dự đoán bài hát có trở thành **trending** hay không

### Đặc trưng (Features)

#### Audio Features (11 đặc trưng):
- `danceability`, `energy`, `loudness`, `speechiness`
- `acousticness`, `instrumentalness`, `liveness`, `valence`
- `tempo`, `duration_ms`, `key`

#### Genre Features (One-Hot Encoding):
- `genre_pop`, `genre_rock`, `genre_hip hop`, `genre_country`, v.v.
- Hỗ trợ **multi-label** (một bài hát có thể thuộc nhiều thể loại)

### Gán nhãn

```python
threshold = df_train_val['popularity'].quantile(0.70)  # = 44.00
is_trend = 1 if popularity >= 44 else 0
```

**Phân phối nhãn**:
- Train: 31.89% trend / 68.11% non-trend
- Validation: 31.38% trend / 68.62% non-trend
- Test: 37.86% trend / 62.14% non-trend

### Chia dữ liệu (Temporal Split)

```
Train + Validation: 2010-2017 (26%)
Test: 2018-2024 (47%)
```

Lý do: Tránh **temporal leakage**, mô phỏng dự đoán thực tế

### Kết quả mô hình

#### Validation Set

| Model | Accuracy | Precision (1) | Recall (1) | F1 (1) | Weighted F1 |
|-------|----------|---------------|------------|--------|-------------|
| **Logistic Regression** | **0.8300** | 0.79 | 0.69 | 0.74 | **0.8258** |
| Random Forest | 0.7549 | 0.77 | 0.23 | 0.36 | 0.6787 |
| XGBoost | **0.8384** | 0.78 | 0.74 | 0.76 | **0.8296** |

#### Test Set

| Model | Accuracy | Precision (1) | Recall (1) | F1 (1) | Weighted F1 |
|-------|----------|---------------|------------|--------|-------------|
| Logistic Regression | 0.7130 | 0.67 | 0.60 | 0.63 | 0.7167 |
| Random Forest | 0.6839 | 0.65 | 0.42 | 0.51 | 0.6345 |
| **XGBoost** | **0.7226** | 0.67 | 0.68 | 0.68 | **0.7211** |

### Mô hình tốt nhất: XGBoost

**Lý do**:
- Độ chính xác cao trên cả validation (83.84%) và test (72.26%)
- Cân bằng tốt giữa Precision và Recall
- Khả năng tổng quát hóa tốt (không overfitting)
- Học được mối quan hệ phi tuyến phức tạp

**Cấu hình**:
```python
XGBClassifier(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
```

---

## 📊 Dashboard

### Power BI Features
<img width="653" height="602" alt="image" src="https://github.com/user-attachments/assets/cb2bc3a6-2bed-41b9-baab-a14a40f6805e" />


#### 1. Overview Page
- Tổng quan số liệu (Total Songs, Avg Popularity, Top Genres)
- Trend line: Số bài hát qua các năm
- Top 10 nghệ sĩ phổ biến nhất
<img width="1051" height="601" alt="image" src="https://github.com/user-attachments/assets/c1072b62-44f1-4d8a-a30b-2d8bdb9ded1d" />

#### 2. Genre Analysis
- Phân bố thể loại theo giai đoạn
- Biểu đồ Sunburst: Thể loại → Nghệ sĩ → Bài hát
- Matrix: Tương quan giữa thể loại và đặc trưng âm nhạc

<img width="1033" height="591" alt="image" src="https://github.com/user-attachments/assets/1ccc65c5-5566-4315-b960-094430287731" />



#### 3. Audio Features
- Radar chart: So sánh đặc trưng âm nhạc
- Heatmap: Ma trận tương quan
- Box plot: Phân phối theo thể loại

<img width="1041" height="585" alt="image" src="https://github.com/user-attachments/assets/8f701e43-f6d4-4f18-9868-44696a5ff784" />

#### 4. Trend Prediction
- Kết quả từ ML model
- Confusion matrix
- Feature importance

<img width="1048" height="594" alt="image" src="https://github.com/user-attachments/assets/0f4f932a-615b-476a-b2ee-74bdd96fea27" />


### Interactive Filters
- **Thời gian**: Năm, giai đoạn
- **Thể loại**: Pop, Rock, Hip-Hop, v.v.
- **Nghệ sĩ**: Tìm kiếm và lọc
- **Độ phổ biến**: Slider 0-100

---

## 👥 Thành viên nhóm

| STT | Họ và Tên | MSSV | Nhiệm vụ | Email |
|-----|-----------|------|----------|-------|
| 1 | **Phan Châu Nguyên** | 2312376 | - Soạn LaTeX, khai thác dữ liệu<br>- Xây dựng Dashboard<br>- Lưu trữ dữ liệu | nguyen.phan@hcmut.edu.vn |
| 2 | **Mai Xuân Phúc** | 2312687 | - Tính khả thi của dữ liệu<br>- Phân tích dữ liệu<br>- Xây dựng mô hình ML | phuc.mai@hcmut.edu.vn |
| 3 | **Phan Phúc Thịnh** | 2313306 | - Soạn LaTeX<br>- Khai thác & phân tích dữ liệu<br>- Đánh giá hiệu năng mô hình | thinh.phan@hcmut.edu.vn |
| 4 | **Nguyễn Quang Tùng** | 2313817 | - Chuẩn hóa tên biến<br>- Xây dựng mô hình dự đoán<br>- Tiền xử lí dữ liệu | tung.nguyen@hcmut.edu.vn |

**Giảng viên hướng dẫn**: ThS. Dương Huỳnh Anh Đức

**Khoa**: Khoa học và Kỹ thuật Máy tính

**Trường**: Đại học Bách Khoa - ĐHQG TP.HCM

---

## 📚 Tài liệu tham khảo

### Papers & Research
1. Chhavi Maheshwaria. "Music Recommendation on Spotify using Deep Learning." Preprint, 2023.
2. Shuo Jiang. "Predicting Music Popularity: A Machine Learning Approach Using Spotify Data." MLSCM 2024.

### Datasets
- [Spotify Tracks Attributes and Popularity](https://www.kaggle.com/datasets/melissamonfared/spotify-tracks-attributes-and-popularity)
- [Billboard Hot 100 Dataset](https://www.kaggle.com/code/soldatovda/spotify/input)

### API Documentation
- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)

### Technical References
- [Microsoft SQL Server Documentation](https://docs.microsoft.com/en-us/sql/)
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

---

## 📄 License

Dự án này được thực hiện cho mục đích học thuật tại Trường Đại học Bách Khoa - ĐHQG TP.HCM.

---

## 🙏 Acknowledgments

- Cảm ơn **Spotify** đã cung cấp API và dữ liệu công khai
- Cảm ơn cộng đồng **Kaggle** đã chia sẻ datasets
- Cảm ơn **ThS. Dương Huỳnh Anh Đức** đã hướng dẫn nhiệt tình

---

<div align="center">

**Đồ án Tổng hợp - Hệ Kĩ Thuật Dữ Liệu**

Trường Đại học Bách Khoa - ĐHQG TP.HCM

Tháng 9/2025

</div>
