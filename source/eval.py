import json, os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

def evaluate_and_dump(model, name, X_test, y_test, outdir="artifacts"):
    os.makedirs(outdir, exist_ok=True)
    y_pred = model.predict(X_test)

    # text report
    with open(os.path.join(outdir, f"{name}_report.txt"), "w", encoding="utf-8") as f:
        f.write(classification_report(y_test, y_pred, digits=4))

    # confusion matrix
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred,
                                            display_labels=["not_trend","trend"],
                                            cmap="Blues", ax=ax)
    ax.set_title(f"{name} - Confusion Matrix")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, f"{name}_confusion_matrix.png"), dpi=160)
    plt.close(fig)

    # feature importance (nếu có)
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        order = np.argsort(importances)
        fig, ax = plt.subplots(figsize=(6, max(3, 0.25 * X_test.shape[1])))
        ax.barh(np.array(X_test.columns)[order], np.array(importances)[order])
        ax.set_title(f"{name} - Feature Importance")
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, f"{name}_feature_importance.png"), dpi=160)
        plt.close(fig)
