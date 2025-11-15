# Training script (placeholder)

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from app.config import settings
from app.core.preprocess import Preprocessor

def load_data(path: Path):
    df = pd.read_csv(
    settings.DATA_PATH,
    sep=";",
    encoding="latin1",
    engine="python",
    quoting=3,   # Ignora comillas problemáticas
    on_bad_lines="skip"   # evita filas rotas
)

    # identificar columnas
    text_col = "text" if "text" in df.columns else df.columns[0]
    label_col = None
    for c in ["airline_sentiment","sentiment","label"]:
        if c in df.columns:
            label_col = c
            break
    if label_col is None:
        raise ValueError("No se encontró columna de etiquetas")
    df = df[[text_col, label_col]].dropna()
    df["text_clean"] = df[text_col].astype(str).map(Preprocessor().clean_text)
    # map labels to positive/neutral/negative if necessary
    df["label_mapped"] = df[label_col].astype(str).str.lower().map(
        lambda x: "positive" if "pos" in x else ("negative" if "neg" in x else ("neutral" if "neu" in x else x))
    )
    return df

def train_and_save():
    path = settings.DATA_PATH
    if not path.exists():
        print("CSV no encontrado en:", path)
        return
    df = load_data(path)
    X = df["text_clean"].values
    y = df["label_mapped"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=20000)),
        ("clf", LogisticRegression(max_iter=1000))
    ])
    print("Entrenando modelo...")
    pipe.fit(X_train, y_train)
    print("Accuracy en test:", pipe.score(X_test, y_test))
    out_path = settings.MODEL_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out_path)
    print("Modelo guardado en:", out_path)

if __name__ == "__main__":
    train_and_save()
