import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from app.core.config import settings
from app.core.logging import logger
from app.services.embedding_service import embedding_service

class VectorService:
    def __init__(self):
        self.client: Optional[QdrantClient] = None
        self.collection_name = settings.QDRANT_COLLECTION
        self.dim = settings.EMBEDDING_DIM
        self._connected = False

    def connect(self):
        """Initializes connection to Qdrant server or local embedded storage."""
        if self._connected and self.client:
            return

        # 1. Try URL connection if configured
        if settings.QDRANT_URL:
            try:
                logger.info(f"Connecting to Qdrant at {settings.QDRANT_URL}...")
                client = QdrantClient(
                    url=settings.QDRANT_URL,
                    api_key=settings.QDRANT_API_KEY,
                    timeout=3.0
                )
                client.get_collections()
                self.client = client
                self._connected = True
                logger.info("Connected to Qdrant server successfully.")
                self.ensure_collection()
                return
            except Exception as e:
                logger.warning(f"Could not connect to Qdrant server ({e}). Falling back to local embedded Qdrant.")

        # 2. Local embedded Qdrant disk storage
        try:
            storage_path = os.path.join(os.getcwd(), "qdrant_storage")
            os.makedirs(storage_path, exist_ok=True)
            self.client = QdrantClient(path=storage_path)
            self._connected = True
            logger.info(f"Connected to local embedded Qdrant storage at {storage_path}.")
            self.ensure_collection()
        except Exception as e:
            logger.warning(f"Local storage Qdrant failed ({e}), falling back to in-memory Qdrant.")
            self.client = QdrantClient(":memory:")
            self._connected = True
            self.ensure_collection()

    def ensure_collection(self):
        """Creates the product vector collection if it does not exist."""
        if not self.client:
            return
            
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if not exists:
                logger.info(f"Creating Qdrant collection '{self.collection_name}'...")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=self.dim,
                        distance=qmodels.Distance.COSINE
                    )
                )
                # Create payload indexes for fast filtering
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="category",
                    field_schema=qmodels.PayloadSchemaType.KEYWORD
                )
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="price",
                    field_schema=qmodels.PayloadSchemaType.FLOAT
                )
                logger.info(f"Qdrant collection '{self.collection_name}' created.")
        except Exception as e:
            logger.error(f"Error ensuring Qdrant collection: {e}")

    def index_products(self, products: List[Dict[str, Any]]):
        """Indexes a list of products into Qdrant."""
        self.connect()
        if not self.client or not products:
            return 0

        texts = []
        for p in products:
            specs = " ".join(p.get("specs", []))
            tags = " ".join(p.get("tags", []))
            text = f"{p.get('title', '')} {p.get('brand', '')} {p.get('category', '')} {p.get('subcategory', '')} {specs} {tags} {p.get('description', '')}"
            texts.append(text)

        embeddings = embedding_service.get_embeddings(texts)
        points = []
        
        for idx, (p, emb) in enumerate(zip(products, embeddings)):
            # Deterministic integer or UUID point ID from string
            point_id = idx + 1
            payload = {
                "product_id": p["id"],
                "title": p.get("title") or p.get("name"),
                "category": p.get("category"),
                "subcategory": p.get("subcategory"),
                "brand": p.get("brand"),
                "price": float(p.get("price", 0)),
                "rating": float(p.get("rating", 4.5)),
                "availability": p.get("availability", "in_stock"),
                "tags": p.get("tags", [])
            }
            points.append(
                qmodels.PointStruct(
                    id=point_id,
                    vector=emb,
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        logger.info(f"Indexed {len(points)} products into Qdrant collection '{self.collection_name}'.")
        return len(points)

    def search(
        self,
        query: str,
        limit: int = 10,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Semantic vector search with optional payload filters."""
        self.connect()
        if not self.client:
            return []

        query_vector = embedding_service.get_embedding(query)
        
        # Build Qdrant payload filters
        must_conditions = []
        if category:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="category",
                    match=qmodels.MatchValue(value=category)
                )
            )
        if min_price is not None:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="price",
                    range=qmodels.Range(gte=min_price)
                )
            )
        if max_price is not None:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="price",
                    range=qmodels.Range(lte=max_price)
                )
            )

        query_filter = qmodels.Filter(must=must_conditions) if must_conditions else None

        try:
            hits = []
            if hasattr(self.client, "query_points"):
                response = self.client.query_points(
                    collection_name=self.collection_name,
                    query=query_vector,
                    query_filter=query_filter,
                    limit=limit
                )
                hits = getattr(response, "points", response)
            elif hasattr(self.client, "search"):
                hits = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    query_filter=query_filter,
                    limit=limit
                )
            
            results = []
            for hit in hits:
                results.append({
                    "product_id": hit.payload.get("product_id"),
                    "score": float(hit.score) if hasattr(hit, "score") else 0.9,
                    "payload": hit.payload
                })
            return results
        except Exception as e:
            logger.error(f"Qdrant search error: {e}")
            return []

vector_service = VectorService()
