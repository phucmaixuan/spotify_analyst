import pandas as pd

df_billboard = pd.read_csv("top_songs_through_year.csv")

# Chuẩn hoá dữ liệu thiếu
# Thay các ký hiệu lỗi bằng NaN
df_billboard.replace(["-", "#", " ", ""], pd.NA, inplace=True)

# Chuẩn hoá kiểu dữ liệu 
# Chuyển cột Date về dạng datetime
df_billboard["Date"] = pd.to_datetime(df_billboard["Date"], errors="coerce")

# Tạo cột Year (phục vụ phân tích)
df_billboard["Year"] = df_billboard["Date"].dt.year

# Ép kiểu số cho các cột hạng
num_cols = ["Rank", "Last Week", "Peak Position", "Weeks in Charts"]
for col in num_cols:
    df_billboard[col] = pd.to_numeric(df_billboard[col], errors="coerce")

#  Xử lý giá trị trùng
# Sắp xếp để lấy bản ghi mới nhất (nếu cùng bài, cùng nghệ sĩ)
df_billboard.sort_values(by=["Song", "Artist", "Date"], ascending=[True, True, False], inplace=True)
df_billboard.drop_duplicates(subset=["Song", "Artist"], keep="first", inplace=True)

# Kiểm tra dữ liệu
print("\nThông tin tổng quan:")
print(df_billboard.info())

print("\nSố lượng giá trị thiếu theo cột:")
print(df_billboard.isna().sum())

# Lưu ra file mới
df_billboard.to_csv("billboard_clean.csv", index=False)
