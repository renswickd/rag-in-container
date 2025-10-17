# Configuration Guide

## Environment Variables

```bash
DATABASE_URL=your_database_url
CHROMA_DB_PATH=path_to_your_chroma_db
PDF_DIRECTORY=data/policy_documents/
METADATA_FILE=data/policy_records_metadata.csv
GROQ_API_KEY=your_groq_api_key
LOG_LEVEL=info
```

## Application Config (app_config.yaml)

### Storage Settings
- Document registry location
- Archive directory
- Temporary storage
- Metadata CSV location

### Vector Store Settings
- Persistence directory
- Collection name
- Embedding model
- Retrieval parameters

### Processing Settings
- Chunk size
- Chunk overlap
- Session management