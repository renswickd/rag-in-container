from pathlib import Path
import json
from typing import List, Dict
from datetime import datetime

class DocumentTracker:
    def __init__(self, registry_file: str = "data/document_registry.json"):
        self.registry_file = Path(registry_file)
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load existing document registry or create new one"""
        if self.registry_file.exists():
            with self.registry_file.open('r') as f:
                return json.load(f)
        return {}

    def _save_registry(self) -> None:
        """Save registry to disk"""
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        with self.registry_file.open('w') as f:
            json.dump(self.registry, f, indent=2)

    def register_document(self, original_path: Path, archived_path: Path) -> None:
        """Register a processed document"""
        doc_info = {
            "original_path": str(original_path),
            "archived_path": str(archived_path),
            "processed_at": datetime.now().isoformat(),
            "file_size": original_path.stat().st_size
        }
        self.registry[str(original_path)] = doc_info
        self._save_registry()

    def get_processed_files(self) -> List[str]:
        """Get list of processed file paths"""
        return list(self.registry.keys())

    def get_unprocessed_files(self, directory: Path) -> List[Path]:
        """Get list of unprocessed PDF files in directory"""
        all_pdfs = set(p for p in directory.glob("*.pdf"))
        processed = set(Path(p) for p in self.registry.keys())
        return sorted(all_pdfs - processed)