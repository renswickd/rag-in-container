# filepath: /rag-policy-assistant/rag-policy-assistant/src/config/settings.py

class Config:
    DATABASE_URL = "your_database_url_here"
    CHROMA_DB_PATH = "path_to_your_chroma_db"
    PDF_DIRECTORY = "data/policy_documents/"
    METADATA_FILE = "data/policy_records_metadata.csv"
    API_KEY = "your_api_key_here"
    LOG_LEVEL = "INFO"