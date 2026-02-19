from sentence_transformers import SentenceTransformer

# kleines, schnelles Modell (384 Dimensionen!)
# ACHTUNG: passt nicht zu vector(1536) -> wir ändern gleich die Dimension
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()
