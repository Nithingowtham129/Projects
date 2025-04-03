from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
from sentence_transformers import SentenceTransformer

connections.connect("default", host="localhost", port = "19530")

model = SentenceTransformer("all-MiniLM-L6-v2") # sentence transformer model

# fields describing the data 
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
]

schema = CollectionSchema(fields, description="Text embeddings storage")

collection = Collection("text_collection", schema)


# function to generate embedding for a given text
def generate_embedding(text):
    return model.encode(text).tolist()

# function to store a text in milvus collection
def store_in_milvus(text):
    embedding = generate_embedding(text)
    collection.insert([[text], [embedding]])

# function to search for similar texts in milvus collection
def search_milvus(query_embedding):
    return collection.search([query_embedding], "embedding", top_k=3)