# classification_hit
The project is trying to predicting a song or a track will be a hit or not based on the "popularity" that measure by sound featues


# Run train.py: chỉnh songs_normalize ra ngoài thành con của file classification_hit
# đảm bảo bạn đang ở thư mục D:\classification_hit (nơi có .venv)
# và đang ở trong môi trường ảo (.venv) — dòng prompt có (.venv)
(.venv) PS D:\classification_hit> pip install pandas scikit-learn xgboost matplotlib
 py -m source.train --data ./songs_normalize.csv --genre_mode target
 
