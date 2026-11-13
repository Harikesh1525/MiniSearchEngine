
import unittest
import tempfile
from pathlib import Path

from reportlab.pdfgen import canvas
from docx import Document as WordDocument

from document_handler.document import Document
from document_handler.document_reader import DocumentReader
from document_handler.document_manager import DocumentManager


class TestDocumentReader(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)
        self.reader = DocumentReader()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_txt_reading(self):
        path = self.folder / "sample.txt"
        path.write_text("Python is a programming language.")

        content = self.reader.read(path)

        self.assertEqual(
            content,
            "Python is a programming language."
        )

    def test_pdf_reading(self):
        path = self.folder / "sample.pdf"

        pdf = canvas.Canvas(str(path))
        pdf.drawString(100, 750, "Sample PDF document")
        pdf.save()

        content = self.reader.read(path)

        self.assertIn("Sample PDF document", content)

    def test_docx_reading(self):
        path = self.folder / "sample.docx"

        doc = WordDocument()
        doc.add_paragraph("Sample DOCX document")
        doc.save(path)

        content = self.reader.read(path)

        self.assertIn("Sample DOCX document", content)

    def test_docx_table_extraction(self):
        path = self.folder / "table.docx"

        doc = WordDocument()
        table = doc.add_table(rows=2, cols=2)

        table.cell(0, 0).text = "Name"
        table.cell(0, 1).text = "Age"
        table.cell(1, 0).text = "Murali"
        table.cell(1, 1).text = "25"

        doc.save(path)

        content = self.reader.read(path)

        self.assertIn("Name", content)
        self.assertIn("Age", content)
        self.assertIn("Murali", content)
        self.assertIn("25", content)

    def test_empty_txt(self):
        path = self.folder / "empty.txt"
        path.write_text("")

        content = self.reader.read(path)

        self.assertEqual(content, "")

    def test_unsupported_file(self):
        path = self.folder / "image.png"
        path.write_text("Not a supported document")

        with self.assertRaises(ValueError):
            self.reader.read(path)

    def test_uppercase_txt_extension(self):
        path = self.folder / "SAMPLE.TXT"
        path.write_text("Testing uppercase extension")

        content = self.reader.read(path)

        self.assertEqual(
            content,
            "Testing uppercase extension"
        )


class TestDocumentManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)
        self.manager = DocumentManager(self.folder)

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_pdf(self, path):
        pdf = canvas.Canvas(str(path))
        pdf.drawString(100, 750, "Manager PDF document")
        pdf.save()

    def test_directory_scanning(self):
        (self.folder / "a.txt").write_text("Text document")

        nested = self.folder / "nested"
        nested.mkdir()

        self.create_pdf(nested / "b.pdf")

        docx = WordDocument()
        docx.add_paragraph("Word document")
        docx.save(nested / "c.docx")

        (self.folder / "image.png").write_text("Ignore this")

        documents = self.manager.load_documents()

        self.assertEqual(len(documents), 3)

        self.assertEqual(
            [doc.doc_id for doc in documents],
            [1, 2, 3]
        )

        self.assertEqual(
            [doc.file_name for doc in documents],
            ["a.txt", "b.pdf", "c.docx"]
        )

        self.assertTrue(
            all(isinstance(doc, Document) for doc in documents)
        )

    def test_empty_directory(self):
        documents = self.manager.load_documents()

        self.assertEqual(documents, [])
        self.assertEqual(self.manager.get_errors(), [])

    def test_missing_directory(self):
        missing = self.folder / "missing"

        manager = DocumentManager(missing)

        with self.assertRaises(FileNotFoundError):
            manager.load_documents()

    def test_corrupted_files(self):
        (self.folder / "broken.pdf").write_text(
            "This is not a valid PDF"
        )

        (self.folder / "broken.docx").write_text(
            "This is not a valid DOCX"
        )

        documents = self.manager.load_documents()

        self.assertEqual(documents, [])
        self.assertEqual(len(self.manager.get_errors()), 2)


if __name__ == "__main__":
    unittest.main()
