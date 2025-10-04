from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from common.config import load_config

def load_pdfs(pdf_dir: Path):
    docs = []
    for p in sorted(pdf_dir.glob("*.pdf")):
        loader = PyPDFLoader(str(p))
        file_docs = loader.load()
        for d in file_docs:
            d.metadata.setdefault("source", p.name)
        docs.extend(file_docs)
    return docs

def main():
    cfg = load_config()
    pdf_dir = Path(cfg["ingestion"]["pdf_dir"])
    persist_dir = cfg["vector_store"]["persist_directory"]
    collection_name = cfg["vector_store"]["collection_name"]
    chunk_size = cfg["ingestion"]["chunk_size"]
    chunk_overlap = cfg["ingestion"]["chunk_overlap"]
    separators = cfg["ingestion"]["separators"]

    pdf_dir.mkdir(parents=True, exist_ok=True)
    Path(persist_dir).mkdir(parents=True, exist_ok=True)

    print(f"[INGEST] Loading PDFs from: {pdf_dir.resolve()}")
    docs = load_pdfs(pdf_dir)
    if not docs:
        print("[INGEST] No PDFs found. Drop files into the folder and rerun.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )
    chunks = splitter.split_documents(docs)
    print(f"[INGEST] Split into {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name=cfg["embedding"]["model_name"])

    vectordb = Chroma(
        persist_directory=persist_dir,
        collection_name=collection_name,
        embedding_function=embeddings,
    )
    vectordb.add_documents(chunks)

    print(f"[INGEST] Persisted to Chroma at: {Path(persist_dir).resolve()}")

if __name__ == "__main__":
    main()

