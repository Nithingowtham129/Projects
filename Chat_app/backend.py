import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File
from extraction.extract_text import extract_text_from_url, extract_text_from_pdf, extract_text_from_image
from database.milvus_handler import store_in_milvus, search_milvus, generate_embedding

# Configure the Gemini API to access the AI model
genai.configure(api_key="SET_YOUR_API_KEY") # modify with your own

app = FastAPI()

#loading data from the user
@app.post("/load")
async def load_data(url: str = None, file: UploadFile = None):
    if url:
        text = extract_text_from_url(url)
    elif file:
        file_extension = file.filename.split(".")[-1]
        if file_extension in ["jpg", "png"]:
            text = extract_text_from_image(file.file)
        elif file_extension == "pdf":
            text = extract_text_from_pdf(file.file)
    else:
        return {"error": "No valid input provided"}

    store_in_milvus(text)
    return {"message": "Data loaded successfully"}

# generating response for the information from the 
@app.post("/query")
async def query_data(query: str):
    query_embedding = generate_embedding(query)
    search_results = search_milvus(query_embedding)
    retrieved_texts = [hit.entity.text for hit in search_results[0]]

    prompt = f"Based on the following information: {retrieved_texts}, answer the query: {query}"

    # Use Gemini API to generate responses
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return {"response": response.text.strip()}