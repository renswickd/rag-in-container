from pathlib import Path
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config(path: str = "configs/dev.yaml") -> dict:
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    
    cfg["vector_store"]["persist_directory"] = os.getenv(
        "CHROMA_DIR", cfg["vector_store"]["persist_directory"]
    )
    cfg["embedding"]["model_name"] = os.getenv("EMBED_MODEL", cfg["embedding"]["model_name"])
    return cfg
