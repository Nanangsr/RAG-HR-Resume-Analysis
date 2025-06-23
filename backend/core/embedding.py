from langchain_community.embeddings import SentenceTransformerEmbeddings
import os
import torch

embedding_model_cache = None

def get_embedding_model():
    """Load optimized embedding model with simple caching."""
    global embedding_model_cache
    if embedding_model_cache is None:
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading embedding model '{model_name}' onto device '{device}'...")
        embedding_model_cache = SentenceTransformerEmbeddings(
            model_name=model_name,
            model_kwargs={'device': device, 'trust_remote_code': True},
            encode_kwargs={'normalize_embeddings': True}
        )
        print("Embedding model loaded successfully.")
    return embedding_model_cache
