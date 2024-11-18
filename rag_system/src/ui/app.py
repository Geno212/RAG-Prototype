import streamlit as st
import requests
from typing import Dict, Any

# Set API endpoint URL
API_BASE_URL = "http://127.0.0.1:8000"

# Streamlit UI layout
st.title("RAG System UI")
st.markdown("A simple interface for interacting with the Retrieval-Augmented Generation system.")

# Upload document section
st.header("Upload Document")
uploaded_file = st.file_uploader("Choose a file to upload", type=["pdf", "txt", "docx", "doc"])
collection_name = st.text_input("Collection Name", value="default_collection")

if st.button("Upload Document") and uploaded_file:
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post(
            f"{API_BASE_URL}/upload",
            files=files,
            params={"collection_name": collection_name}
        )
        if response.status_code == 200:
            st.success("Document uploaded and processed successfully.")
        else:
            st.error(f"Failed to upload document: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Query section
st.header("Ask a Question")
question = st.text_input("Your Question")
query_collection_name = st.text_input("Query Collection Name", value="default_collection")

if st.button("Submit Question"):
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question, "collection_name": query_collection_name}
        )
        if response.status_code == 200:
            data: Dict[str, Any] = response.json()
            st.subheader("Answer")
            st.write(data["answer"])
            st.subheader("Context")
            for context in data["context"]:
                st.text_area("Context Snippet", context, height=100)
            st.subheader("Processing Time")
            st.write(f"{data['processing_time']:.2f} seconds")
        else:
            st.error(f"Failed to get answer: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# List collections section
st.header("Available Collections")
if st.button("List Collections"):
    try:
        response = requests.get(f"{API_BASE_URL}/collections")
        if response.status_code == 200:
            collections = response.json().get("collections", [])
            if collections:
                st.write("Available Collections:")
                st.write(", ".join(collections))
            else:
                st.write("No collections found.")
        else:
            st.error(f"Failed to fetch collections: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
