import math

from text_processing.text_processor import TextProcessor


class QueryProcessor:

    def __init__(self, text_processor=None):
        self.text_processor = text_processor or TextProcessor()

    # Convert user query into tokens
    def process_query(self, query):

        if not isinstance(query, str):
            raise TypeError("Query must be a string")

        return self.text_processor.tokenize(query)

    # Calculate Term Frequency
    def calculate_tf(self, frequency):

        return 1 + math.log(frequency)

    # Calculate Inverse Document Frequency
    def calculate_idf(self, total_documents, document_frequency):

        return 1 + math.log(
            (total_documents + 1) / (document_frequency + 1)
        )

        # Extract a short sentence containing a matched word
    def create_snippet(self, content, matched_terms, max_length=180):

        import re

        if not content or not matched_terms:
            return ""

        # Split document content into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)

        # Find the sentence containing a matched word
        for sentence in sentences:

            for term in matched_terms:

                pattern = r'\b' + re.escape(term) + r'\b'

                if re.search(pattern, sentence, re.IGNORECASE):

                    # Return the complete sentence if it is short
                    if len(sentence) <= max_length:
                        return sentence.strip()

                    # Otherwise extract a short section around the word
                    match = re.search(
                        pattern,
                        sentence,
                        re.IGNORECASE
                    )

                    start = max(0, match.start() - 70)
                    end = min(len(sentence), start + max_length)

                    snippet = sentence[start:end].strip()

                    if start > 0:
                        snippet = "..." + snippet

                    if end < len(sentence):
                        snippet += "..."

                    return snippet

        return ""

    # Search documents using the inverted index
    def search(self, query, inverted_index, documents):

        # Step 1: Process query
        query_tokens = self.process_query(query)

        if not query_tokens:
            return []

        # Step 2: Remove duplicate query tokens
        query_tokens = list(dict.fromkeys(query_tokens))

        # Step 3: Get index information
        index_data = inverted_index.get_index()

        total_documents = len(inverted_index.get_document_ids())

        if total_documents == 0:
            return []

        # Step 4: Find matching indexed words
        matching_terms = set()

        for query_token in query_tokens:

            for term in index_data:

                if term.startswith(query_token):
                    matching_terms.add(term)

        # Step 5: Calculate TF-IDF scores
        scores = {}
        matched_terms = {}

        for term in matching_terms:

            postings = inverted_index.get_postings(term)

            document_frequency = inverted_index.get_document_frequency(term)

            idf = self.calculate_idf(
                total_documents,
                document_frequency
            )

            for doc_id, frequency in postings.items():

                tf = self.calculate_tf(frequency)

                tf_idf = tf * idf

                if doc_id not in scores:
                    scores[doc_id] = 0
                    matched_terms[doc_id] = set()

                scores[doc_id] += tf_idf

                matched_terms[doc_id].add(term)

        # Step 6: Create document lookup dictionary
        document_map = {
            document.doc_id: document
            for document in documents
        }

        # Step 7: Rank documents by relevance
        ranked_doc_ids = sorted(
            scores,
            key=lambda doc_id: (-scores[doc_id], doc_id)
        )

        # Step 8: Prepare search results
        results = []

        for doc_id in ranked_doc_ids:

            document = document_map.get(doc_id)

            if document is None:
                continue

            results.append({
                "doc_id": doc_id,
                "file_name": document.file_name,
                "path": document.path,
                "matched_terms": sorted(matched_terms[doc_id]),
                "snippet": self.create_snippet(
                    document.content,
                    matched_terms[doc_id]
                )
            })

        return results