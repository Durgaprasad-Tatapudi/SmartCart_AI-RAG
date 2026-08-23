import hashlib
import numpy as np
from typing import List
from app.core.config import settings
from app.core.logging import logger

class EmbeddingService:
    def __init__(self):
        self._model = None
        self._fastembed_model = None
        self.dim = settings.EMBEDDING_DIM
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return
            
        try:
            # Try FastEmbed first (ultra lightweight ONNX runtime)
            from fastembed import TextEmbedding
            logger.info(f"Loading FastEmbed multilingual model: {settings.EMBEDDING_MODEL}")
            self._fastembed_model = TextEmbedding(model_name=settings.EMBEDDING_MODEL)
            self._initialized = True
            logger.info("FastEmbed model loaded successfully.")
            return
        except Exception as e:
            logger.warning(f"FastEmbed not available ({e}), attempting sentence-transformers fallback...")

        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading SentenceTransformer model...")
            self._model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
            self.dim = 384
            self._initialized = True
            logger.info("SentenceTransformer model loaded successfully.")
            return
        except Exception as e:
            logger.warning(f"SentenceTransformer not available ({e}). Using deterministic multilingual dense vectorizer.")
            self._initialized = True

    def get_embedding(self, text: str) -> List[float]:
        """Generates a dense vector embedding for a single text."""
        return self.get_embeddings([text])[0]

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a batch of texts."""
        if not self._initialized:
            self.initialize()

        if self._fastembed_model:
            try:
                embeddings = list(self._fastembed_model.embed(texts))
                return [emb.tolist() for emb in embeddings]
            except Exception as e:
                logger.error(f"FastEmbed embedding error: {e}")

        if self._model:
            try:
                embeddings = self._model.encode(texts, normalize_embeddings=True)
                return [emb.tolist() for emb in embeddings]
            except Exception as e:
                logger.error(f"SentenceTransformer embedding error: {e}")

        # Deterministic multilingual semantic vectorizer fallback (ensures 100% offline & zero crash)
        return [self._deterministic_vector(t) for t in texts]

    def _deterministic_vector(self, text: str) -> List[float]:
        """Generates a normalized deterministic dense vector based on multilingual semantic tokens."""
        vec = np.zeros(self.dim, dtype=np.float32)
        words = text.lower().split()
        if not words:
            return vec.tolist()
            
        for i, word in enumerate(words):
            h = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)
            idx1 = h % self.dim
            idx2 = (h >> 8) % self.dim
            vec[idx1] += 1.0 / (i + 1)
            vec[idx2] += 0.5 / (i + 1)

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

embedding_service = EmbeddingService()
