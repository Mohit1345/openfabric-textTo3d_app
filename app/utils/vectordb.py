import os
import faiss
import pickle
from datetime import datetime
from sentence_transformers import SentenceTransformer

class VectorMemoryManager:
    def __init__(self, persist_directory="/openfabric/app/outputs/faiss"):
        self.persist_directory = os.path.abspath(persist_directory)
        os.makedirs(self.persist_directory, exist_ok=True)

        self.index_path = os.path.join(self.persist_directory, "faiss.index")
        self.meta_path = os.path.join(self.persist_directory, "metadata.pkl")

        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384

        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []

        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadata = pickle.load(f)

    def embed_text(self, text):
        return self.embedding_model.encode([text])[0]

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def add_prompt(self, prompt, meta=None):
        embedding = self.embed_text(prompt).astype('float32')
        self.index.add(embedding.reshape(1, -1))

        doc_meta = meta or {}
        doc_meta['original_prompt'] = prompt
        doc_meta['timestamp'] = datetime.utcnow().isoformat()
        self.metadata.append(doc_meta)

        self.save()
        print(f"✅ Added prompt to FAISS: {prompt}")

    def search_similar(self, query, top_k=3):
        if self.index.ntotal == 0:
            return []

        query_embedding = self.embed_text(query).astype('float32').reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)

        matches = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                matches.append({
                    'prompt': self.metadata[idx]['original_prompt'],
                    'meta': self.metadata[idx],
                    'distance': float(dist)
                })

        return matches
