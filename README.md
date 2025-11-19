# Policy Assistant

A RAG-based policy assistant that helps users find and understand company policies through natural language queries.

## Features

- 📚 Interactive chat interface for policy queries
- 🔍 Semantic search across policy documents
- 📄 PDF document ingestion and processing
- 💾 Vector store for efficient retrieval
- 🏷️ Metadata tracking and lookup
- 📊 Document management and version tracking

## Project Structure

```
rag-policy-assistant/
├── configs/
│   └── app_config.yaml      # Application configuration
├── frontend/
│   ├── components/          # UI components
│   ├── static/             
│   │   └── css/            # Styling
│   └── utils/              # Frontend utilities
├── pipeline/
│   ├── ingestion/          # Document processing
│   ├── storage/            # Vector and document stores
│   └── utils/              # Pipeline utilities
├── graphs/
│   ├── nodes/              # Graph nodes
│   └── tools/              # Custom tools
├── common/                 # Shared utilities
├── data/                  # Data storage
│   ├── archived_docs/     # Archived documents
│   └── metadata/          # Policy metadata
└── docs/                  # Documentation
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Create necessary directories:
```bash
mkdir -p data/{archived_docs,metadata}
mkdir -p chroma_db
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Upload policy documents:
   - Use the sidebar upload function
   - Supports PDF files
   - Documents are automatically processed and indexed

3. Query policies:
   - Ask questions in natural language
   - View source references
   - Access policy metadata

## Configuration

Key settings in `configs/app_config.yaml`:
- Vector store parameters
- Document processing settings
- LLM configuration
- Storage paths

## Development

### Adding New Features

1. Frontend:
   - Add components in `frontend/components/`
   - Update styles in `frontend/static/css/`

2. Pipeline:
   - Document processing in `pipeline/ingestion/`
   - Storage handling in `pipeline/storage/`

3. Graph:
   - Add nodes in `graphs/nodes/`
   - Create tools in `graphs/tools/`

### Testing

```bash
pytest tests/
```

## License

MIT
