import streamlit as st
from pathlib import Path
from pipeline.utils.document_tracker import DocumentTracker
from pipeline.storage.vector_store import VectorStore
from pipeline.storage.document_store import DocumentStore
from pipeline.ingestion.loader import DocumentLoader
from pipeline.ingestion.processor import DocumentProcessor
from typing import Optional

def process_uploaded_file(
    uploaded_file,
    doc_store: DocumentStore,
    vector_store: VectorStore,
    tracker: DocumentTracker
) -> bool:
    """Process a single uploaded file"""
    try:
        # Create temp directory if not exists
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / uploaded_file.name
        
        # Save uploaded file
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Initialize components
        loader = DocumentLoader(tracker, doc_store)
        processor = DocumentProcessor(vector_store)
        
        # Load documents - pass the parent directory
        documents = loader.load_documents(temp_dir.parent)
        
        if not documents:
            st.error(f"No content extracted from {uploaded_file.name}")
            return False
            
        # Process and add to vector store
        success = processor.process_documents(documents)
        
        # Cleanup
        temp_path.unlink()
        
        if success:
            st.session_state["show_processed"] = True
        
        return success
        
    except Exception as e:
        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        return False

def render_ingestion_sidebar(
    tracker: DocumentTracker,
    vector_store: VectorStore,
    doc_store: DocumentStore
):
    """Render ingestion controls in the sidebar"""
    with st.sidebar:
        st.header("📁 Document Management")
        
        # File Upload Section
        st.subheader("Upload Documents", divider="gray")
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload one or more PDF files to be processed"
        )
        
        if uploaded_files:
            with st.spinner("Processing documents..."):
                for uploaded_file in uploaded_files:
                    if process_uploaded_file(uploaded_file, doc_store, vector_store, tracker):
                        st.success(f"✅ Processed: {uploaded_file.name}")
                    else:
                        st.error(f"❌ Failed to process: {uploaded_file.name}")
        
        # Document List
        if st.session_state.get("show_processed", False):
            with st.expander("📑 Processed Documents", expanded=True):
                processed_files = tracker.get_processed_files()
                if processed_files:
                    for doc_path in processed_files:
                        st.text(Path(doc_path).name)
                else:
                    st.info("No documents processed yet")
        
        # Maintenance Section
        st.subheader("Maintenance", divider="gray")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh"):
                st.session_state.show_processed = True
                st.rerun()
        
        # Reset Option
        with st.expander("⚠️ Danger Zone"):
            st.warning("This will delete all embedded documents!")
            if st.button("Reset Vector DB", type="primary"):
                confirm = st.button("Confirm Reset")
                if confirm:
                    vector_store.reset()
                    st.success("Vector DB reset successfully")
                    st.rerun()