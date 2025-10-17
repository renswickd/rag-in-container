from pathlib import Path
import shutil
from datetime import datetime

class DocumentStore:
    def __init__(self, archive_root: Path):
        self.archive_root = archive_root
        self.archive_root.mkdir(parents=True, exist_ok=True)

    def archive_document(self, source_path: Path) -> Path:
        """Archive a document with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source_path.stem}_{timestamp}{source_path.suffix}"
        dest_path = self.archive_root / filename
        
        shutil.copy2(source_path, dest_path)
        return dest_path

    def get_archived_documents(self) -> List[Path]:
        """Get list of archived documents"""
        return sorted(self.archive_root.glob("*.pdf"))