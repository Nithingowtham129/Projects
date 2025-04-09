from fastapi import FastAPI, UploadFile, File, Request
from data_extraction import extract_text_from_url, extract_text_from_pdf, extract_text_from_image
from pydantic import BaseModel
from db import add_to_chroma, query_chroma
import google.generativeai as genai

app = FastAPI()

model = genai.GenerativeModel("gemini-1.5-pro-latest")

genai.configure(api_key="Your_API_Key_Here")

class QueryInput(BaseModel):
    query: str

@app.post("/load")
async def load_data(url: str = None, file: UploadFile = None):
    if url:
        text = extract_text_from_url(url)
        source = url
        
    elif File:
        file_extension = file.filename.split(".")[-1].lower()
        source = file.filename
        if file_extension in ["jpg", "jpeg", "png"]:
            text = extract_text_from_image(file.file) # extract text from image
        elif file_extension == "pdf":
            text = extract_text_from_pdf(file.file) # extract text from pdf
        else:
            return {"error": "Unsupported file type"} # check if the file is supported
    else:
        return {"error": "No input provided"}

    add_to_chroma(text, source) # Store the text in ChromaDB
    return {"message": f"Data from {source} added to ChromaDB successfully."} #return the success message

@app.post("/query")
async def query_data(input: QueryInput):
    matched_chunks = query_chroma(input.query) # Query ChromaDB for relevant text chunks
    
    if not matched_chunks:
        return {"message": "No relevant content found in the database."}
    
    # Combine all matched documents (text chunks)
    context = "\n\n".join(chunk for chunk, _ in matched_chunks)

    response = model.generate_content(f"your memory:\n{context}\nAnswer the question:\n{input.query}")

    # Extract unique sources from metadata
    sources = list({meta["source"] for _, meta in matched_chunks if "source" in meta})

    return {"message": response.text, "sources": sources}