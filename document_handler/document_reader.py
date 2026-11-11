
from pathlib import Path
from pypdf import PdfReader
from docx import Document as WordDocument


class DocumentReader:

    SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}

    def read(self, file_path):
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported file format")

        if extension == ".txt":
            return self.read_txt(path)

        elif extension == ".pdf":
            return self.read_pdf(path)

        elif extension == ".docx":
            return self.read_docx(path)

    def read_txt(self, path):
        with open(path, "r", encoding="utf-8-sig") as file:
            return file.read()

    def read_pdf(self, path):
        pdf = PdfReader(str(path))

        content = []

        for page in pdf.pages:
            text = page.extract_text()
            if text:
                content.append(text)

        return "\n".join(content)

    def read_docx(self, path):
        doc = WordDocument(str(path))

        content = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                content.append(paragraph.text)

        for table in doc.tables:
            for row in table.rows:
                row_text = [
                    cell.text.strip() for cell in row.cells
                ]
                content.append("\t".join(row_text))

        return "\n".join(content)
