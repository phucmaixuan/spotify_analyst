import pandas as pd
from src.preprocess import clean_genre, create_target
from src.train import split_by_time, train_model

def main():
    print("Bắt đầu quy trình...")
    # 1. Tải dữ liệu
    df = pd.read_csv('data/songs_normalize.csv')

    # 2. Tiền xử lý
    df = clean_genre(df)
    df = create_target(df, threshold=80)

    # (... Gọi các hàm xử lý feature, encode, scale ...)

    # 3. Chia dữ liệu
    features_list = ['danceability', 'energy', ...] # Danh sách các cột feature
    target_name = 'is_hit'
    X_train, X_test, y_train, y_test = split_by_time(df, features_list, target_name)

    # 4. Huấn luyện
    model = train_model(X_train, y_train)

    # 5. Đánh giá
    # (Gọi hàm đánh giá...)

    print("Hoàn thành!")

if __name__ == "__main__":
    main()