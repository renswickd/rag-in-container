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
from common.logger_util import init_logger

def load_pdfs(pdf_dir: Path, tracker: DocumentTracker) -> List:
    """Load only unprocessed PDFs"""
    docs = []
    unprocessed_files = tracker.get_unprocessed_files(pdf_dir)
    
    for p in sorted(unprocessed_files):
        print(f"Processing new file: {p.name}")
        loader = PyPDFLoader(str(p))
        file_docs = loader.load()
        
        # Create metadata
        meta = DocMeta(
            source=p.name,
            title=p.stem,
            # version="1.0", 
            effective_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Register document
        tracker.register_document(p, meta)
        
        # Add metadata to documents
        for d in file_docs:
            d.metadata.update(asdict(meta))
        docs.extend(file_docs)
        
    return docs

def main():
    logger, _ = init_logger()
    cfg = load_config()
    pdf_dir = Path(cfg["ingestion"]["pdf_dir"])
    persist_dir = cfg["vector_store"]["persist_directory"]
    collection_name = cfg["vector_store"]["collection_name"]
    
    # Initialize document tracker
    tracker = DocumentTracker()
    
    print(f"[INGEST] Loading PDFs from: {pdf_dir.resolve()}")
    docs = load_pdfs(pdf_dir, tracker)
    
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

if __name__ == "__main__":
    main()

