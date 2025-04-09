import uuid
import chromadb
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load sentence transformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_store")
collection = chroma_client.get_or_create_collection("my_collection")

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # size of each chunk
    chunk_overlap=50,  # overlap between chunks
    separators=["\n\n", "\n", ".", " ", ""] # separators for splitting text
)

# Function to add text to ChromaDB
def add_to_chroma(text, source="unknown"):
    chunks = text_splitter.split_text(text) # Split text into chunks

    for chunk in chunks:
        doc_id = str(uuid.uuid4()) # Generate a unique ID for each chunk
        embedding = embedding_model.encode(chunk).tolist() # Generate embedding for the chunk

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"source": source}],
            ids=[doc_id]
        )

# Function to query ChromaDB
def query_chroma(query_text, n_results=1):
    query_embedding = embedding_model.encode(query_text).tolist() # Generate embedding for the query

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    ) # Get results from ChromaDB
    
    # Return list of (document, metadata) pairs
    if results["documents"]:
        return list(zip(results["documents"][0], results["metadatas"][0]))
    return []
