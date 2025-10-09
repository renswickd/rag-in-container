from pathlib import Path
from typing import List
from datetime import datetime
from dataclasses import asdict
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from common.config import load_config
from pipeline.document_tracker import DocumentTracker
from pipeline.schema import DocMeta
from common.logger_util import init_logger #, track_processed_document
import sys
from typing import List

def load_pdfs(pdf_dir: Path, tracker: DocumentTracker, session_path: Path, logger) -> List:

    docs = []
    unprocessed_files = tracker.get_unprocessed_files(pdf_dir)
    
    for p in sorted(unprocessed_files):
        try:
            logger.info(f"Processing new file: {p.name}")
            loader = PyPDFLoader(str(p))
            file_docs = loader.load()
            
            # Create metadata
            meta = DocMeta(
                source=p.name,
                title=p.stem,
                effective_date=datetime.now().strftime("%Y-%m-%d")
            )
            
            # # Save copy to session's processed_docs directory
            # archived_path = track_processed_document(session_path, p)
            # logger.info(f"Archived copy at: {archived_path}")
            
            # Register document
            tracker.register_document(p, meta)
            
            # Add metadata to documents
            for d in file_docs:
                d.metadata.update(asdict(meta))
            docs.extend(file_docs)
            
        except Exception as e:
            logger.error(f"Failed to process {p.name}: {e}")
            continue
        
    return docs

def reset_vectordb(persist_dir: str, collection_name: str, embed_model: str, force: bool = False, logger = None) -> bool:
    """Reset vector database and associated document tracker """
    warning_message = """
    ⚠️  WARNING: You are about to reset the vector database!
    This will permanently delete all embedded documents and their metadata.
    This action cannot be undone.
    """
    
    if logger:
        logger.warning(warning_message)
    print(warning_message)
    
    # User confirmation unless force=True
    if not force:
        confirmation = input("\nType 'RESET' to confirm or anything else to cancel: ").strip()
        if confirmation != "RESET":
            print("Reset cancelled.")
            if logger:
                logger.info("Vector database reset cancelled by user")
            return False
    
    try:
        # Initialize empty embeddings for connection
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(
            persist_directory=persist_dir,
            collection_name=collection_name,
            embedding_function=embeddings
        )
        
        # Get current document count for logging
        initial_count = db._collection.count()
        
        # Delete collection
        db._client.delete_collection(collection_name)
        
        # Recreate empty collection
        db = Chroma(
            persist_directory=persist_dir,
            collection_name=collection_name,
            embedding_function=embeddings
        )
        
        success_msg = f"Successfully reset vector database. Removed {initial_count} documents."
        if logger:
            logger.warning(success_msg)
        print(success_msg)
        
        return True
        
    except Exception as e:
        error_msg = f"Failed to reset vector database: {str(e)}"
        if logger:
            logger.error(error_msg)
        print(f"Error: {error_msg}")
        return False

def main():
    logger, session_path = init_logger()
    
    cfg = load_config()
    pdf_dir = Path(cfg["ingestion"]["pdf_dir"])
    persist_dir = cfg["vector_store"]["persist_directory"]
    collection_name = cfg["vector_store"]["collection_name"]
    embed_model = HuggingFaceEmbeddings(model_name=cfg["embedding"]["model_name"])
    
    # Check for --reset flag
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        logger.warning("Reset flag detected - attempting to reset vector database")
        reset_vectordb(persist_dir, collection_name, embed_model,force=False, logger=logger)
            # return
        
    # Initialize document tracker
    tracker = DocumentTracker()
    
    logger.info(f"[INGEST] Loading PDFs from: {pdf_dir.resolve()}")
    docs = load_pdfs(pdf_dir, tracker, session_path, logger)
    
    if not docs:
        logger.info("[INGEST] No new PDFs to process.")
        return
    
    logger.info(f"[INGEST] Processing {len(docs)} new documents")
    logger.info(f"[INGEST] Processed files: {tracker.get_processed_files()}")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg["ingestion"]["chunk_size"],
        chunk_overlap=cfg["ingestion"]["chunk_overlap"],
        separators=cfg["ingestion"]["separators"],
    )
    chunks = splitter.split_documents(docs)
    print(f"[INGEST] Split into {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name=cfg["embedding"]["model_name"])
    vectordb = Chroma(
        persist_directory=persist_dir,
        collection_name=collection_name,
        embedding_function=embeddings,
    )
    
    # Add new chunks to existing collection
    vectordb.add_documents(chunks)
    logger.info(f"[INGEST] Added new chunks to Chroma at: {Path(persist_dir).resolve()}")
    
    # draft - print ingestion summary
    print("\nIngestion Summary:")
    print(f"- Total files processed: {len(tracker.get_processed_files())}")
    print(f"- New files in this run: {len(docs)}")
    print(f"- New chunks added: {len(chunks)}")
    print(f"- Processed files archived at: {session_path/'processed_docs'}")

if __name__ == "__main__":
    main()

