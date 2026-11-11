
import unittest

from document_handler.document import Document
from text_processing.text_processor import TextProcessor


class TestTextProcessor(unittest.TestCase):

    def setUp(self):
        # Create a fresh TextProcessor object for every test
        self.processor = TextProcessor()

    def test_normalize(self):
        text = "Python IS Great! Hello_World."
        expected = "python is great hello world"

        self.assertEqual(self.processor.normalize(text), expected)

    def test_normalize_empty_text(self):
        self.assertEqual(self.processor.normalize(""), "")

    def test_normalize_extra_spaces(self):
        text = "   Python     is    easy   "
        expected = "python is easy"

        self.assertEqual(self.processor.normalize(text), expected)

    def test_tokenize(self):
        text = "Python is a programming language!"
        expected = ["python", "is", "a", "programming", "language"]

        self.assertEqual(self.processor.tokenize(text), expected)

    def test_tokenize_repeated_words(self):
        text = "Python python PYTHON"
        expected = ["python", "python", "python"]

        self.assertEqual(self.processor.tokenize(text), expected)

    def test_tokenize_numbers(self):
        text = "Python 123 programming 45.6"
        expected = ["python", "123", "programming", "45", "6"]

        self.assertEqual(self.processor.tokenize(text), expected)

    def test_tokenize_empty_text(self):
        self.assertEqual(self.processor.tokenize(""), [])

    def test_process_documents(self):
        documents = [
            Document(1, "doc1.txt", "Python is powerful.", ".txt"),
            Document(2, "doc2.txt", "Java is also useful.", ".txt"),
            Document(5, "doc3.txt", "Machine Learning uses Python.", ".txt")
        ]

        expected = {
            1: ["python", "is", "powerful"],
            2: ["java", "is", "also", "useful"],
            5: ["machine", "learning", "uses", "python"]
        }

        self.assertEqual(
            self.processor.process_documents(documents),
            expected
        )

    def test_process_empty_document(self):
        documents = [
            Document(10, "empty.txt", "", ".txt"),
            Document(20, "normal.txt", "Hello World!", ".txt")
        ]

        expected = {
            10: [],
            20: ["hello", "world"]
        }

        self.assertEqual(
            self.processor.process_documents(documents),
            expected
        )

    def test_process_empty_list(self):
        self.assertEqual(self.processor.process_documents([]), {})


if __name__ == "__main__":
    unittest.main()
