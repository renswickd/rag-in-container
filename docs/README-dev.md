# Policy Assistant (Dev)

## Quickstart
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and set `GROQ_API_KEY`
4. Put PDFs under `data/policy_documents/` and metadata CSV at `data/metadata/pr_metadata.csv`
5. `python -m pipeline.ingest_pdfs`
6. `python -m apps.cli_chat`
`
## Config
See `configs/dev.yaml`.

## Flow
Ingestion → Chroma → Retrieve → Agent(tool) → Generate (with memory).
