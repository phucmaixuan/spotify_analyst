import numpy as np
import pandas as pd

AUDIO_FEATURES = [
    "danceability","energy","valence","acousticness",
    "speechiness","instrumentalness","liveness","tempo","duration_ms"
]

def normalize_main_genre(raw: str) -> str:
    if not isinstance(raw, str): return "other"
    g = raw.lower()
    if "pop" in g or "k-pop" in g: return "pop"
    if "hip hop" in g or "hip-hop" in g or "rap" in g or "trap" in g: return "hiphop_rap"
    if "r&b" in g or "rnb" in g or "soul" in g: return "rnb_soul"
    if "rock" in g or "metal" in g or "punk" in g: return "rock"
    if "indie" in g or "alternative" in g or "alt" in g: return "indie_alt"
    if "edm" in g or "electro" in g or "dance" in g or "house" in g or "club" in g: return "electronic_dance"
    if "latin" in g or "reggaeton" in g or "reggae" in g or "bachata" in g or "salsa" in g: return "latin"
    if "country" in g: return "country"
    return "other"

# ---------- One-hot genre (không lo leakage) ----------
def build_features_onehot(train_df: pd.DataFrame, test_df: pd.DataFrame):
    tr = train_df.copy(); te = test_df.copy()
    tr["main_genre"] = tr.get("main_genre", tr.get("genre")).apply(normalize_main_genre)
    te["main_genre"] = te.get("main_genre", te.get("genre")).apply(normalize_main_genre)

    tr_dum = pd.get_dummies(tr["main_genre"], prefix="genre")
    te_dum = pd.get_dummies(te["main_genre"], prefix="genre")
    tr_dum, te_dum = tr_dum.align(te_dum, join="outer", axis=1, fill_value=0)

    X_train = pd.concat([tr[AUDIO_FEATURES], tr_dum], axis=1)
    X_test  = pd.concat([te[AUDIO_FEATURES], te_dum], axis=1)
    return X_train, X_test

# ---------- Target encoding (tránh leakage: học mapping từ TRAIN) ----------
def build_features_target(train_df: pd.DataFrame, test_df: pd.DataFrame, alpha: float = 50.0):
    tr = train_df.copy(); te = test_df.copy()
    tr["main_genre"] = tr.get("main_genre", tr.get("genre")).apply(normalize_main_genre)
    te["main_genre"] = te.get("main_genre", te.get("genre")).apply(normalize_main_genre)

    mu = tr["is_trend"].mean()
    stats = tr.groupby("main_genre")["is_trend"].agg(["mean","count"])
    enc = (stats["mean"]*stats["count"] + alpha*mu) / (stats["count"] + alpha)
    mapping = enc.to_dict(); fallback = mu

    tr_enc = tr["main_genre"].map(lambda g: mapping.get(g, fallback)).astype(float)
    te_enc = te["main_genre"].map(lambda g: mapping.get(g, fallback)).astype(float)

    X_train = pd.concat([tr[AUDIO_FEATURES], tr_enc.rename("genre_enc")], axis=1)
    X_test  = pd.concat([te[AUDIO_FEATURES], te_enc.rename("genre_enc")], axis=1)
    return X_train, X_test
