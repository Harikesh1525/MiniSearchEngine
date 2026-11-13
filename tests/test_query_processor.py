import unittest

from document_handler.document import Document
from inverted_index.inverted_index import InvertedIndex
from query_processing.query_processor import QueryProcessor


class TestQueryProcessor(unittest.TestCase):

    def setUp(self):

        self.processor = QueryProcessor()

        self.documents = [
            Document(
                doc_id=1,
                path="documents/doc1.txt",
                content="Python Python programming",
                file_type=".txt"
            ),

            Document(
                doc_id=2,
                path="documents/doc2.txt",
                content="Python programming language",
                file_type=".txt"
            ),

            Document(
                doc_id=3,
                path="documents/doc3.txt",
                content="Programming fundamentals",
                file_type=".txt"
            )
        ]

        processed_documents = {
            1: ["python", "python", "programming"],
            2: ["python", "programming", "language"],
            3: ["programming", "fundamentals"]
        }

        self.index = InvertedIndex()
        self.index.build_index(processed_documents)

    # Test normal query processing
    def test_process_query(self):

        result = self.processor.process_query(
            "Python Programming!"
        )

        self.assertEqual(
            result,
            ["python", "programming"]
        )

    # Test empty query
    def test_empty_query(self):

        result = self.processor.search(
            "",
            self.index,
            self.documents
        )

        self.assertEqual(result, [])

    # Test prefix search
    def test_prefix_search(self):

        result = self.processor.search(
            "pyth",
            self.index,
            self.documents
        )

        self.assertEqual(
            {item["doc_id"] for item in result},
            {1, 2}
        )

    # Test multiple document retrieval
    def test_multiple_document_retrieval(self):

        result = self.processor.search(
            "programming",
            self.index,
            self.documents
        )

        self.assertEqual(
            {item["doc_id"] for item in result},
            {1, 2, 3}
        )

    # Test TF-IDF ranking
    def test_ranking_order(self):

        result = self.processor.search(
            "python programming",
            self.index,
            self.documents
        )

        self.assertEqual(
            [item["doc_id"] for item in result],
            [1, 2, 3]
        )

    # Test unknown query
    def test_unknown_query(self):

        result = self.processor.search(
            "xyzabc",
            self.index,
            self.documents
        )

        self.assertEqual(result, [])

    # Test invalid query input
    def test_invalid_query(self):

        with self.assertRaises(TypeError):

            self.processor.search(
                123,
                self.index,
                self.documents
            )

        # Test snippet extraction
    def test_create_snippet(self):

        content = "Python is a popular programming language."

        result = self.processor.create_snippet(
            content,
            {"python"}
        )

        self.assertEqual(
            result,
            "Python is a popular programming language."
        )

    # Test snippet length
    def test_snippet_length(self):

        content = "Python " + ("programming language " * 30)

        result = self.processor.create_snippet(
            content,
            {"python"}
        )

        self.assertLessEqual(len(result), 183)


if __name__ == "__main__":
    unittest.main()