import json
from pathlib import Path
from typing import Dict, List
from dataclasses import asdict
from datetime import datetime
from pipeline.hygiene import file_sha256
from pipeline.schema import DocMeta
from common.logger_util import init_logger

class DocumentTracker:
    def __init__(self, track_file: str = "data/document_registry.json"):
        self.track_file = Path(track_file)
        self.registry: Dict[str, dict] = self._load_registry()
        self.logger = init_logger()[0]

    def _load_registry(self) -> Dict[str, dict]:
        """Load existing document registry or create new one"""
        if self.track_file.exists():
            with self.track_file.open('r') as f:
                try:
                    registry = json.load(f)
                    if not isinstance(registry, dict) or not registry:
                        # self.logger.warning("Invalid document registry")
                        return {}
                    return registry
                except json.JSONDecodeError:
                    # self.logger.warning("Invalid JSON in document registry")
                    return {}

    def _save_registry(self) -> None:
        """Save registry to disk"""
        self.track_file.parent.mkdir(parents=True, exist_ok=True)
        with self.track_file.open('w') as f:
            json.dump(self.registry, f, indent=2)

    def get_document_state(self, file_path: Path) -> tuple[bool, str]:
        """
        Check if a document has been processed before
        Returns: (is_processed, status_message)
        """
        file_hash = file_sha256(file_path)
        
        # Check if exact file was processed
        if file_hash in self.registry:
            return True, "File already processed"
            
        # Check if different version of same policy exists
        file_name = file_path.stem 
        for entry in self.registry.values():
            if entry['title'] == file_name:
                return True, "Different version exists"
                
        return False, "New document"

    def register_document(self, file_path: Path, metadata: DocMeta) -> None:
        """
        Register a new document in the tracking system
        """
        file_hash = file_sha256(file_path)
        
        # Convert metadata to dict and add processing info
        doc_info = asdict(metadata)
        doc_info.update({
            "processed_at": datetime.now().isoformat(),
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size
        })
        
        self.registry[file_hash] = doc_info
        self._save_registry()

    def get_unprocessed_files(self, directory: Path) -> List[Path]:
        """
        Return list of PDF files that haven't been processed yet
        """
        unprocessed = []
        for pdf_path in directory.glob("*.pdf"):
            is_processed, _ = self.get_document_state(pdf_path)
            if not is_processed:
                unprocessed.append(pdf_path)
        return unprocessed

    def get_processed_files(self) -> List[str]:
        """Return list of all processed files"""
        return [entry['file_path'] for entry in self.registry.values()]

    def get_document_metadata(self, file_path: Path) -> Dict:
        """Get metadata for a specific document if it exists"""
        file_hash = file_sha256(file_path)
        return self.registry.get(file_hash, {})