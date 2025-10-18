import os
from pathlib import Path
import yaml
from typing import Dict, Any

def load_config(config_path: str = "configs/app_config.yaml") -> Dict[str, Any]:
    """Load application configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Override with environment variables if set
        if os.getenv("CHROMA_DIR"):
            config["vector_store"]["persist_directory"] = os.getenv("CHROMA_DIR")
            
        if os.getenv("EMBED_MODEL"):
            config["vector_store"]["embedding_model"] = os.getenv("EMBED_MODEL")
            
        return config
        
    except Exception as e:
        raise RuntimeError(f"Failed to load config from {config_path}: {str(e)}")
