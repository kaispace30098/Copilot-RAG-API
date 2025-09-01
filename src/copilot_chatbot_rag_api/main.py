import os
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List

# Corrected import to address the deprecation warning
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

# --- Pydantic Models for a Clear API Structure ---
class QueryRequest(BaseModel):
    """The request body for a user's query."""
    userId: str
    prompt: str

class SearchResult(BaseModel):
    """Represents a single retrieved document chunk."""
    source: str
    content: str

class SearchResponse(BaseModel):
    """The response body containing a list of search results."""
    results: List[SearchResult]

# --- API Key Security Setup ---
API_KEY = os.getenv("RAG_API_KEY", "your-secret-key-for-testing")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    """Validates the API key from the request header."""
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

# --- Initialize FastAPI App ---
app = FastAPI(
    title="FAISS Similarity Search API",
    description="An API that finds the top 3 most similar text chunks from a FAISS vector database.",
    version="1.0.0",
)

# --- Load Models and Vector Database at Server Startup ---
try:
    print("Loading models and FAISS index at startup...")

    # 1. Embedding Model (MUST match your db_builder.py)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-roberta-large-v1",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # 2. FAISS Index Path (MUST match your db_builder.py)
    index_path = "faiss_db"
    db = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # 3. The Retriever component for searching the database
    retriever = db.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 most relevant text chunks

    print("✅ Models and FAISS index loaded successfully.")

except Exception as e:
    print(f"❌ FATAL: Error loading models or index: {e}")
    retriever = None

# --- API Endpoints ---

@app.get("/")
def read_root():
    """A simple endpoint to confirm that the API is running."""
    return {"status": "Similarity Search API is online and ready"}

@app.post("/api/similarity-search", response_model=SearchResponse)
async def perform_similarity_search(request: QueryRequest, api_key: str = Depends(get_api_key)):
    """
    Receives a prompt and returns the top 3 most relevant document chunks from FAISS.
    """
    if not retriever:
        raise HTTPException(status_code=503, detail="FAISS retriever is not available.")

    print(f"Received search from user '{request.userId}': '{request.prompt}'")

    try:
        # Invoke the retriever to get the raw documents
        docs = retriever.invoke(request.prompt)
        
        # Format the documents into our SearchResult model
        results = [
            SearchResult(
                source=doc.metadata.get("source", "Unknown"),
                content=doc.page_content
            ) for doc in docs
        ]
        
        print(f"Found {len(results)} relevant chunks.")
        return SearchResponse(results=results)
        
    except Exception as e:
        print(f"Error during similarity search: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform the search.")

