import streamlit as st
import requests

#Fast API URL
FASTAPI_URL = "http://127.0.0.1:8501"
st.title("🤖 AI-Powered Data Extraction and Query System")

# Upload section
st.subheader("📤 Upload Data (URL or File)")
input_type = st.radio("Select Input Type", ["URL", "File"])

# Input area should always be visible
url = None
file = None

if input_type == "URL":
    url = st.text_input("Enter URL:")

elif input_type == "File":
    file = st.file_uploader("Upload a file", type=["jpg", "png", "pdf"])

# Buttons for triggering actions
if st.button("Extract and Store Data"):
    if input_type == "URL" and url:
        response = requests.post(f"{FASTAPI_URL}/load", params={"url": url})
        st.success(response.json()["message"])

    elif input_type == "File" and file:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{FASTAPI_URL}/load", files=files)
        st.success(response.json()["message"])
    else:
        st.warning("Please provide a valid input before submitting.")

# Query Section
st.subheader("🔍 Ask a Question")
query = st.text_area("Enter your question:")
if st.button("Get Response"):
    with st.spinner("Generating response..."):
        response = requests.post(f"{FASTAPI_URL}/query", json={"query": query})
        st.markdown("### 💬 AI Response:")
        st.write(response.json()["message"])
        sources = response.json().get("sources")
        if sources:
            st.markdown("### 📚 Sources:")
            st.write(", ".join(sources))