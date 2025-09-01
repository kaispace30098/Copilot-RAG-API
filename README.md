# Copilot RAG API

This project provides a backend API designed to be used as an **Action in Microsoft Copilot Studio**.  
It implements a **Retrieval-Augmented Generation (RAG)** pattern using a local **FAISS vector database** to perform similarity searches on a given knowledge base.  

The API is built with **FastAPI** and is designed to be containerized with **Docker** for easy deployment to cloud services like **Azure App Service**.

---

## ✨ Features
- **FastAPI Backend**: A robust and fast web framework for building APIs.  
- **FAISS Vector Search**: Utilizes a powerful local vector database for efficient similarity searches.  
- **Sentence Transformers**: Uses state-of-the-art models to create high-quality text embeddings.  
- **Dockerized**: Comes with a Dockerfile for easy, consistent, and scalable deployment.  
- **Secure Endpoint**: Includes API key authentication, ready for production use.  
- **Clear API Structure**: Uses Pydantic models for well-defined request and response schemas.  

---

## 📦 Prerequisites
- Python **3.12** (recommended)  
- **Poetry** for local dependency management  
- **Docker Desktop** for building and running the container  
- An **Azure account** (for cloud deployment)  

---

## ⚙️ Project Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kaispace30098/Copilot-RAG-API.git
cd Copilot-RAG-API
```

### 2. Install Dependencies
This project uses **Poetry** to manage dependencies.
```bash
poetry install
```

### 3. Prepare Your Knowledge Base
Place all your pre-chunked `.txt` files into the `landingai_output_F1` directory (or create it if it doesn't exist).

### 4. Build the FAISS Index
Run the builder script to convert your text files into a vector database.  
This will create a `faiss_db` folder.
```bash
poetry run python src/db_builder.py
```

---

## 🚀 Running the API

### A) Running Locally (for Development)
Activate the Poetry environment and run the **Uvicorn server**:
```bash
# Start the server on port 8080
poetry run uvicorn copilot_chatbot_rag_api.main:app --reload --port 8080
```

Access the interactive API docs at:  
👉 http://localhost:8080/docs

---

### B) Running with Docker (Recommended)
This method simulates the **production environment**.

#### 1. Build the Docker Image
```bash
docker build -t rag-api .
```

#### 2. Run the Docker Container
```bash
docker run -d -p 8080:8080 -e RAG_API_KEY="your-secret-key" --name rag-api-container rag-api
```

The API will be accessible at:  
👉 http://localhost:8080/docs

---

## 🔑 API Endpoint Details

- **URL:** `/api/similarity-search`  
- **Method:** `POST`  
- **Authentication:** Requires API key in header  

### Headers
```
X-API-Key: your-secret-key
```

### Request Body
```json
{
  "userId": "some_user_id",
  "prompt": "Your question to search for"
}
```

### Success Response (200 OK)
```json
{
  "results": [
    {
      "source": "filename_of_chunk.txt",
      "content": "The text content of the relevant chunk."
    }
  ]
}
```

---

## ☁️ Deployment to Azure

1. **Push to Container Registry**  
   Build and push your Docker image to **Azure Container Registry (ACR)**.

2. **Create App Service**  
   Create a new **Azure App Service** (Web App for Containers).

3. **Configure App Service**  
   - Point the App Service to your image in ACR.  
   - Set environment variables (`RAG_API_KEY`) in the configuration.

4. **Register in Copilot Studio**  
   Use the **public URL** from App Service to register this API as a new **Action**.

---

## 📖 License
MIT License – feel free to use and modify.
