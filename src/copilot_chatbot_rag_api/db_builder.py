# src/db_builder.py

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

folder_path = "landingai_output"  # Assumes this folder is in the root
texts = []
metadatas = []

# Load embedding model with normalization
print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-roberta-large-v1",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True} )

# Iterate through all .txt files in the folder
print(f"Reading pre-chunked files from '{folder_path}'...")
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):  
        file_path = os.path.join(folder_path, file_name)

        # Read file content
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Append content and metadata
        texts.append(content)
        metadatas.append({
            "source": file_name,
            "type": "text"
        })

print(f"Processed {len(texts)} pre-chunked text files.")

# Initialize FAISS database
print("Building FAISS index...")
vector_db = FAISS.from_texts(
    texts=texts,
    metadatas=metadatas,
    embedding=embeddings
)

# Save the FAISS database
vector_db.save_local("faiss_db")
print("FAISS index built and saved successfully!")