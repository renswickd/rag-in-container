# Architecture Overview

## Components

### Frontend Layer
- Streamlit-based UI
- Component-based architecture
- Session state management
- CSS styling system

### Pipeline Layer
- Document ingestion
- PDF processing
- Vector storage
- Document archival

### Graph Layer
- RAG implementation
- Custom tools
- LLM integration
- State management

## Data Flow

1. Document Ingestion:
   ```
   Upload → Process → Archive → Vector Store
   ```

2. Query Processing:
   ```
   Query → Retrieve → Agent → Generate → Response
   ```

3. Metadata Management:
   ```
   Query → Tool → Metadata Lookup → Response
   ```