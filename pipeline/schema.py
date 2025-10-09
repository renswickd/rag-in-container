from dataclasses import dataclass

@dataclass
class DocMeta:
    source: str
    title: str | None = None
    section: str | None = None
    # version: str | None = None
    effective_date: str | None = None
