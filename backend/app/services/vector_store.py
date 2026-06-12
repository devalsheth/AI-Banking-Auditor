import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import settings

_model = None
_index = None
_documents = []

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model

def build_index(documents: list[dict]):
    global _index, _documents
    _documents = documents
    texts = [d['text'] for d in documents]
    embeddings = get_model().encode(texts, convert_to_numpy=True)
    dimension = embeddings.shape[1]
    _index = faiss.IndexFlatL2(dimension)
    _index.add(np.array(embeddings, dtype='float32'))

def search_context(query: str, top_k: int = 5):
    if _index is None or not _documents:
        return []
    embedding = get_model().encode([query], convert_to_numpy=True)
    distances, indices = _index.search(np.array(embedding, dtype='float32'), top_k)
    results = []
    for idx, distance in zip(indices[0], distances[0]):
        if idx < len(_documents):
            item = dict(_documents[idx])
            item['distance'] = float(distance)
            results.append(item)
    return results
