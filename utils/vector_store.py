import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config.settings import VECTOR_STORE_PATH, EMBEDDING_MODEL

@st.cache_resource
def load_vectorstore():
    """Load vector store for context retrieval"""
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embedding_model
    )
    return vectordb, embedding_model

def get_context_chunks(query, k=10):
    """Get context chunks from vector store"""
    vectordb, _ = load_vectorstore()
    docs_and_scores = vectordb.similarity_search_with_score(query, k=k)
    return "\n\n".join([doc[0].page_content for doc in docs_and_scores])