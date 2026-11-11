from dataclasses import dataclass


@dataclass
class Document:
    doc_id: int
    path: str
    content: str
    file_type: str

    @property
    def file_name(self):
        from pathlib import Path
        return Path(self.path).name
