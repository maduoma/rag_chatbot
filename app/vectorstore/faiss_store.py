import faiss
import numpy as np
import os
import pickle

_faiss_index = None
_chunks_db = []

EMBED_DIM = 384  # all-MiniLM-L6-v2

INDEX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/faiss_index'))
INDEX_PATH = os.path.join(INDEX_DIR, 'index.faiss')
CHUNKS_PATH = os.path.join(INDEX_DIR, 'chunks_db.pkl')

def save_faiss_store():
    global _faiss_index, _chunks_db
    if _faiss_index is not None:
        if not os.path.exists(INDEX_DIR):
            os.makedirs(INDEX_DIR)
        faiss.write_index(_faiss_index, INDEX_PATH)
        with open(CHUNKS_PATH, 'wb') as f:
            pickle.dump(_chunks_db, f)

def load_faiss_store():
    global _faiss_index, _chunks_db
    if os.path.exists(INDEX_PATH):
        _faiss_index = faiss.read_index(INDEX_PATH)
    else:
        _faiss_index = faiss.IndexFlatL2(EMBED_DIM)
    if os.path.exists(CHUNKS_PATH):
        with open(CHUNKS_PATH, 'rb') as f:
            _chunks_db = pickle.load(f)
    else:
        _chunks_db = []

# Load at module import
load_faiss_store()

def get_faiss_store():
    global _faiss_index
    if _faiss_index is None:
        _faiss_index = faiss.IndexFlatL2(EMBED_DIM)
    return _faiss_index

def add_to_faiss(chunks: list, embeddings: list):
    global _chunks_db
    index = get_faiss_store()
    vecs = np.array(embeddings).astype('float32')
    index.add(vecs)
    _chunks_db.extend(chunks)
    save_faiss_store()

def retrieve_chunks(query: str, top_k: int = 3) -> list:
    from app.vectorstore.embeddings import embed_chunks
    index = get_faiss_store()
    if index.ntotal == 0:
        return []
    query_vec = np.array(embed_chunks([query])).astype('float32')
    D, I = index.search(query_vec, top_k)
    return [_chunks_db[i] for i in I[0] if i < len(_chunks_db)]
