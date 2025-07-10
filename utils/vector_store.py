import streamlit as st
import sys
import os

# SQLite3 fix for ChromaDB - must be done before importing chromadb
try:
    # Try to replace sqlite3 with pysqlite3-binary for compatibility
    import pysqlite3
    sys.modules['sqlite3'] = pysqlite3
    print("✓ Using pysqlite3-binary for ChromaDB compatibility")
except ImportError:
    print("⚠️ pysqlite3-binary not found. Install with: pip install pysqlite3-binary")

# Try to import ChromaDB components with proper error handling
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from config.settings import VECTOR_STORE_PATH, EMBEDDING_MODEL
    CHROMADB_AVAILABLE = True
except Exception as e:
    st.error(f"ChromaDB components failed to import: {e}")
    CHROMADB_AVAILABLE = False

@st.cache_resource
def load_vectorstore():
    """Load vector store for context retrieval with comprehensive error handling"""
    if not CHROMADB_AVAILABLE:
        st.warning("🔧 ChromaDB not available. Vector search disabled.")
        st.info("💡 To enable vector search: pip install pysqlite3-binary chromadb")
        return None, None
    
    try:
        embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        # Attempt to initialize ChromaDB with better error handling
        vectordb = Chroma(
            persist_directory=VECTOR_STORE_PATH,
            embedding_function=embedding_model
        )
        
        # Test the connection
        vectordb._collection.count()
        
        st.success("✅ Vector store loaded successfully")
        return vectordb, embedding_model
        
    except RuntimeError as e:
        error_msg = str(e).lower()
        if "sqlite3" in error_msg or "unsupported version" in error_msg:
            st.error("🔧 SQLite Version Issue!")
            st.markdown("""
            **Quick Fix:**
            ```bash
            pip install pysqlite3-binary
            ```
            Then restart the app.
            """)
            st.info("Vector search disabled. App continues with basic functionality.")
        else:
            st.error(f"ChromaDB Runtime Error: {e}")
        return None, None
        
    except Exception as e:
        st.warning(f"⚠️ Vector store initialization failed: {e}")
        st.info("Continuing without vector search...")
        return None, None

def get_context_chunks(query, k=10):
    """Get context chunks from vector store with comprehensive fallback"""
    try:
        vectordb, _ = load_vectorstore()
        if vectordb is None:
            # Graceful fallback message
            return f"📄 Context search unavailable for query: '{query[:50]}...'\n\nVector database is not accessible. Install pysqlite3-binary to enable context search."
        
        docs_and_scores = vectordb.similarity_search_with_score(query, k=k)
        if not docs_and_scores:
            return f"No relevant context found for: '{query}'"
        
        context = "\n\n".join([doc[0].page_content for doc in docs_and_scores])
        return f"📚 Retrieved {len(docs_and_scores)} relevant context chunks:\n\n{context}"
        
    except Exception as e:
        return f"⚠️ Context search error: {str(e)}\n\nContinuing without additional context..."
