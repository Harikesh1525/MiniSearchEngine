
import os
from pathlib import Path

from .document import Document
from .document_reader import DocumentReader


class DocumentManager:

    def __init__(self, directory):
        self.directory = Path(directory)
        self.reader = DocumentReader()
        self.documents = []
        self.errors = []

    def load_documents(self):

        if not self.directory.exists():
            raise FileNotFoundError(
                f"Directory not found: {self.directory}"
            )

        if not self.directory.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {self.directory}"
            )

        self.documents = []
        self.errors = []

        file_paths = []

        def handle_directory_error(error):
            self.errors.append({
                "path": error.filename or str(self.directory),
                "error": str(error)
            })

        for root, directories, files in os.walk(
            self.directory,
            onerror=handle_directory_error
        ):

            directories.sort()
            files.sort()

            for filename in files:

                file_path = Path(root) / filename

                if file_path.suffix.lower() in (
                    DocumentReader.SUPPORTED_EXTENSIONS
                ):
                    file_paths.append(file_path)

        file_paths.sort(
            key=lambda path: path.relative_to(
                self.directory
            ).as_posix().casefold()
        )

        for file_path in file_paths:

            try:
                content = self.reader.read(file_path)

                document = Document(
                    doc_id=len(self.documents) + 1,
                    path=str(file_path.resolve()),
                    content=content,
                    file_type=file_path.suffix.lower()
                )

                self.documents.append(document)

            except Exception as error:

                self.errors.append({
                    "path": str(file_path),
                    "error": f"{type(error).__name__}: {error}"
                })

        return self.documents

    def get_documents(self):
        return self.documents

    def get_errors(self):
        return self.errors
