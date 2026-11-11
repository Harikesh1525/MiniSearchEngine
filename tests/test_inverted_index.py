
import unittest

from inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.obj = InvertedIndex()

        self.documents = {
            1: ["python", "programming", "python"],
            2: ["python", "oop"],
            3: ["search", "engine"]
        }

        self.obj.build_index(self.documents)

    # Test 1: Basic index construction
    def test_basic_index(self):

        expected = {
            "python": {1: 2, 2: 1},
            "programming": {1: 1},
            "oop": {2: 1},
            "search": {3: 1},
            "engine": {3: 1}
        }

        self.assertEqual(self.obj.get_index(), expected)

    # Test 2: Repeated tokens
    def test_repeated_tokens(self):

        postings = self.obj.get_postings("python")

        self.assertEqual(postings, {1: 2, 2: 1})

    # Test 3: Multiple documents
    def test_multiple_documents(self):

        self.assertEqual(
            self.obj.get_document_ids(),
            [1, 2, 3]
        )

    # Test 4: Empty document
    def test_empty_document(self):

        documents = {
            1: ["python"],
            2: [],
            3: ["java"]
        }

        self.obj.build_index(documents)

        self.assertEqual(
            self.obj.get_document_ids(),
            [1, 2, 3]
        )

        self.assertEqual(
            self.obj.get_postings("java"),
            {3: 1}
        )

    # Test 5: Empty collection
    def test_empty_collection(self):

        self.obj.build_index({})

        self.assertEqual(self.obj.get_index(), {})

        self.assertEqual(self.obj.get_document_ids(), [])

    # Test 6: Single document
    def test_single_document(self):

        documents = {
            10: ["python", "python", "oop"]
        }

        self.obj.build_index(documents)

        expected = {
            "python": {10: 2},
            "oop": {10: 1}
        }

        self.assertEqual(self.obj.get_index(), expected)

    # Test 7: Postings retrieval
    def test_postings_retrieval(self):

        self.assertEqual(
            self.obj.get_postings("oop"),
            {2: 1}
        )

        self.assertEqual(
            self.obj.get_postings("java"),
            {}
        )

    # Test 8: Document frequency
    def test_document_frequency(self):

        self.assertEqual(
            self.obj.get_document_frequency("python"),
            2
        )

        self.assertEqual(
            self.obj.get_document_frequency("search"),
            1
        )

        self.assertEqual(
            self.obj.get_document_frequency("java"),
            0
        )

    # Test 9: Invalid inputs
    def test_invalid_inputs(self):

        with self.assertRaises(TypeError):
            self.obj.build_index(None)

        with self.assertRaises(TypeError):
            self.obj.build_index({1: "python"})

        with self.assertRaises(TypeError):
            self.obj.build_index({1: [123]})

        with self.assertRaises(ValueError):
            self.obj.build_index({1: [""]})

        with self.assertRaises(TypeError):
            self.obj.get_postings(123)

    # Test 10: Multiple index-building operations
    def test_multiple_build_operations(self):

        new_documents = {
            4: ["java", "programming"],
            5: ["java", "oop"]
        }

        self.obj.build_index(new_documents)

        expected = {
            "java": {4: 1, 5: 1},
            "programming": {4: 1},
            "oop": {5: 1}
        }

        self.assertEqual(self.obj.get_index(), expected)

        self.assertEqual(
            self.obj.get_document_ids(),
            [4, 5]
        )


if __name__ == "__main__":
    unittest.main()
