import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from loguru import logger
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_faiss_index(texts):
    vectors = [model.encode(t["text"]) for t in texts]
    vectors_np = np.array(vectors).astype("float32")
    dim = vectors_np.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors_np)
    logger.info(f"Built FAISS index with {len(vectors_np)} vectors.")
    return index, vectors_np

def search_faiss(index, texts, query, k=3):
    query_vector = model.encode([query]).astype("float32")
    D, I = index.search(query_vector, k)
    results = []
    for i in I[0]:
        entry = texts[i]
        count = len(re.findall(r'\b' + re.escape(query) + r'\b', entry["text"], flags=re.IGNORECASE))
        results.append({
            "page": entry["page"],
            "count": count,
            "preview": entry["text"][:300] + '...'
        })
    return results
