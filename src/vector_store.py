# src/vector_store.py

from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import numpy as np, os, pickle, faiss
from logger import get_logger

class VectorStore:
    """Hugging Face API-based embedding vector store"""

    def __init__(self):
        load_dotenv()
        self.logger = get_logger(__name__)
        self.hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        self.model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
        self.index_path = "data/faiss_index.bin"
        self.meta_path = "data/chunks_metadata.pkl"

        # Load model with token
        self.model = SentenceTransformer(self.model_name, use_auth_token=self.hf_token)
        self.logger.info(f"[OK] Loaded embedding model: {self.model_name}")

    def generate_embeddings(self, texts):
        self.logger.info("[OK] Generating embeddings...")
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return np.array(embeddings, dtype="float32")

    def build_index(self, chunks, metadata):
        embeddings = self.generate_embeddings(chunks)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        faiss.write_index(index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(metadata, f)
        self.logger.info("[OK] FAISS index built and saved")

    def load_index(self):
        if os.path.exists(self.index_path):
            index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                metadata = pickle.load(f)
            self.logger.info("[OK] FAISS index loaded successfully")
            return index, metadata
        else:
            raise FileNotFoundError("FAISS index not found.")
