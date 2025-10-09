import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

LOG_ROOT = Path("logs")
SESSION_PREFIX = "session-"
KEEP_SESSIONS = 5
PROCESSED_DOCS_DIR = "processed_docs"

def _slug_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def _list_sessions(log_root: Path) -> list[Path]:
    if not log_root.exists():
        return []
    return sorted(
        [p for p in log_root.iterdir() if p.is_dir() and p.name.startswith(SESSION_PREFIX)],
        key=lambda p: p.stat().st_mtime,
        reverse=True, 
    )

def _copy_document(src_path: Path, dest_dir: Path) -> Path:
    """Copy a document to the processed_docs directory while preserving metadata"""
    dest_path = dest_dir / src_path.name
    shutil.copy(src_path, dest_path)  # copy2 preserves metadata
    return dest_path

def purge_old_sessions(log_root: Path = LOG_ROOT, keep: int = KEEP_SESSIONS) -> None:
    """
    Keep only the N most recent sessions, remove others including their processed_docs
    """
    sessions = _list_sessions(log_root)
    if len(sessions) <= keep:
        return
    
    for old in sessions[keep:]:
        try:
            shutil.rmtree(old)
        except Exception as e:
            print(f"[WARN] Failed to remove old session at {old}: {e}")

def init_logger(
    name: str = "policy",
    session_id: Optional[str] = None,
    level: int = logging.INFO,
    propagate: bool = False,
) -> Tuple[logging.Logger, Path]:
    """
    Create a session-scoped logger and file under logs/<session-id>/
    Also creates a processed_docs directory for document tracking
    """
    # 1) Ensure logs root exists & purge old sessions
    _ensure_dir(LOG_ROOT)
    purge_old_sessions(LOG_ROOT, KEEP_SESSIONS)

    # 2) Build session id and path
    session_id = session_id or f"{SESSION_PREFIX}{_slug_timestamp()}"
    session_path = LOG_ROOT / session_id
    _ensure_dir(session_path)

    log_file = session_path / "app.log"

    # 3) Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = propagate  # don’t double-log to root

    # Avoid duplicate handlers if called multiple times (e.g., in notebooks/reloads)
    _remove_existing_handlers(logger)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Small header to mark new session starts
    logger.info("────────────────────────────────────────────────────────")
    logger.info("Logging initialized")
    logger.info(f"Session ID: {session_id}")
    logger.info(f"Log file  : {log_file.resolve()}")
    logger.info("────────────────────────────────────────────────────────")

    return logger, session_path

def _remove_existing_handlers(logger: logging.Logger) -> None:
    for h in list(logger.handlers):
        logger.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass
