import streamlit as st
import requests

# Backend URL
FASTAPI_URL = "http://192.168.0.117:8501"

st.title("AI-Powered Data Extraction and Query System") # Title

# Upload section
st.subheader("Upload Data (URL, Image, or PDF)")
input_type = st.radio("Select Input Type", ["URL", "File"])

# URL Section
if input_type == "URL":
    url = st.text_input("Enter URL:")
    if st.button("Extract and Store Data"):
        response = requests.post(f"{FASTAPI_URL}/load", params={"url": url})
        st.success(response.json()["message"])

# file or image 
elif input_type == "File":
    file = st.file_uploader("Upload a file", type=["jpg", "png", "pdf"])
    if file and st.button("Extract and Store Data"):
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{FASTAPI_URL}/load", files=files)
        st.success(response.json()["message"])

# Text Section
st.subheader("Enter the your Prompt: ")
query = st.text_area("Enter your question:")
if st.button("Get Response"):
    response = requests.post(f"{FASTAPI_URL}/query", json={"query": query})
    st.write("AI Response:")
    st.write(response.json()["response"])