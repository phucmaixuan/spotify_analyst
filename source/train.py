# from xgboost import XGBClassifier
# from sklearn.metrics import classification_report

# def split_by_time(df, features, target, split_year=2018):
#     # Chia theo thời gian
#     train_df = df[df['year'] < split_year]
#     test_df = df[df['year'] >= split_year]

#     X_train = train_df[features]
#     y_train = train_df[target]
#     X_test = test_df[features]
#     y_test = test_df[target]

#     return X_train, X_test, y_train, y_test

# def train_model(X_train, y_train):
#     model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
#     model.fit(X_train, y_train)
#     return model


import os, json, argparse
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from .genre import AUDIO_FEATURES, build_features_target, build_features_onehot
from .eval import evaluate_and_dump

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except Exception:
    HAS_XGB = False

def temporal_split(df: pd.DataFrame, split_year: int):
    return df[df["year"] < split_year].copy(), df[df["year"] >= split_year].copy()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=str, default="dataset/songs_normalize.csv")
    ap.add_argument("--split_year", type=int, default=2018)
    ap.add_argument("--genre_mode", choices=["target","onehot"], default="target")
    ap.add_argument("--alpha", type=float, default=50.0, help="smoothing for target encoding")
    ap.add_argument("--outdir", type=str, default="artifacts")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # 1) load + label
    df = pd.read_csv(args.data)
    df["is_trend"] = (df["popularity"] >= 70).astype(int)
    df = df[AUDIO_FEATURES + ["genre","year","is_trend"]].dropna()

    # 2) split theo thời gian
    train_df, test_df = temporal_split(df, args.split_year)
    y_train, y_test = train_df["is_trend"], test_df["is_trend"]

    # 3) build features (genre xử lý ở module features/genre.py)
    if args.genre_mode == "target":
        X_train, X_test = build_features_target(train_df, test_df, alpha=args.alpha)
    else:
        X_train, X_test = build_features_onehot(train_df, test_df)

    # 4) train 3 models
    # Logistic
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    lr.fit(X_train, y_train)
    evaluate_and_dump(lr, "LogisticRegression", X_test, y_test, args.outdir)

    # RandomForest
    rf = RandomForestClassifier(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    evaluate_and_dump(rf, "RandomForest", X_test, y_test, args.outdir)

    # XGBoost
    if HAS_XGB:
        xgb = XGBClassifier(
            n_estimators=400, learning_rate=0.05, max_depth=6,
            subsample=0.8, colsample_bytree=0.8, random_state=42,
            objective="binary:logistic", eval_metric="logloss", n_jobs=-1
        )
        xgb.fit(X_train, y_train)
        evaluate_and_dump(xgb, "XGBoost", X_test, y_test, args.outdir)

        # lưu xác suất dự đoán để lọc top trend
        proba = xgb.predict_proba(X_test)[:,1]
        out = X_test.copy()
        out["true_is_trend"] = y_test.values
        out["pred_prob_trend"] = proba
        out["pred_label"] = (proba >= 0.5).astype(int)
        out.to_csv(os.path.join(args.outdir, "XGBoost_prediction_results.csv"), index=False)

    # 5) lưu config tối thiểu
    with open(os.path.join(args.outdir, "run_config.json"), "w", encoding="utf-8") as f:
        json.dump({
            "data": args.data,
            "split_year": args.split_year,
            "genre_mode": args.genre_mode,
            "alpha": args.alpha,
            "features": AUDIO_FEATURES
        }, f, indent=2)

    print("✅ Done. Artifacts in:", os.path.abspath(args.outdir))

if __name__ == "__main__":
    main()
