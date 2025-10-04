## RAG Policy Assistant

The RAG Policy Assistant is a Retrieval-Augmented Generation (RAG) application designed to answer user queries based on knowledge extracted from PDF documents and associated metadata. This application utilizes a knowledge graph and embeddings stored in Chroma DB to provide accurate and relevant responses.

### Project Structure

```
policy-assistant/
├─ apps/
│  ├─ cli_chat.py                 # Local CLI entrypoint (reads .env, runs chat loop with thread_id)
│  └─ api/
│     └─ main.py                  # (Optional) FastAPI app for dev testing
│
├─ graphs/
│  ├─ policy_graph.py             # Graph wiring: retrieve → agent → generate (+ memory)
│  └─ nodes/
│     ├─ retrieve.py              # Retrieve node (Chroma retriever)
│     ├─ agent.py                 # ReAct agent node (LangGraph prebuilt + tool bindings)
│     └─ generate.py              # Final response node (uses retrieved context + metadata)
│
├─ tools/
│  ├─ metadata_tool.py            # @tool lookup_policy_metadata (reads CSV)
│  └─ __init__.py
│
├─ pipeline/
│  ├─ ingest_pdfs.py              # Ingestion: load PDFs, chunk, embed, persist to Chroma
│  ├─ hygiene.py                  # Vector hygiene (dedupe, re-embed changed, manifests)
│  └─ schema.py                   # Metadata schema helpers (title, section, version, etc.)
│
├─ data/
│  ├─ pdfs/                       # Source policy PDFs (dev)
│  ├─ metadata/
│  │  └─ pr_metadata.csv          # Policy metadata (dev)
│
├─ chroma_db/                     # Persisted Chroma collection (dev)
│
├─ configs/
│  ├─ dev.yaml                    # Single source of truth: k, models, chunking, guardrails toggles
│  └─ logging.yaml                # Optional structured logging config
│
├─ tests/
|  ├─ test_ingest_pdfs.py          # UNIT - ingestion pipeline
│
├─ docs/
│  ├─ README-dev.md               # How to run locally (env, commands, flow)
│  ├─ ingestion.md                # Chunking, schema, hygiene runbook
│
├─ .env.example                   # GROQ_API_KEY=... 
├─ .env                           # Local secrets (gitignored)
├─ .gitignore
├─ requirements.txt               # Python dependencies
├─ setup.py                       # Package setup
└─ README.md                      # Project overview

```

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd rag-policy-assistant
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in the `.env` file as needed.

### Usage

To run the application, execute the following command:
```
python src/main.py
```

### Testing

To run the unit tests, use:
```
pytest tests/
```

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.# rag-in-container
