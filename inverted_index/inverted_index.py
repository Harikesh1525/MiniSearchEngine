class InvertedIndex:

    # Constructor
    def __init__(self):
        self.index = {}
        self.document_ids = []

    # Build the inverted index
    def build_index(self, documents):

        # Validate input
        if not isinstance(documents, dict):
            raise TypeError("Documents must be a dictionary")

        # Temporary index
        new_index = {}

        # Preserve document IDs
        new_document_ids = list(documents.keys())

        # Process each document
        for doc_id, tokens in documents.items():

            # Validate token list
            if not isinstance(tokens, list):
                raise TypeError("Each document must contain a list of tokens")

            # Process each token
            for token in tokens:

                # Validate token
                if not isinstance(token, str):
                    raise TypeError("Tokens must be strings")

                if token == "":
                    raise ValueError("Empty tokens are not allowed")

                # Create token entry if it doesn't exist
                if token not in new_index:
                    new_index[token] = {}

                # Calculate term frequency
                if doc_id not in new_index[token]:
                    new_index[token][doc_id] = 1
                else:
                    new_index[token][doc_id] += 1

        # Update the index
        self.index = new_index
        self.document_ids = new_document_ids

    # Retrieve postings for a particular token
    def get_postings(self, token):

        if not isinstance(token, str):
            raise TypeError("Token must be a string")

        # Return postings if token exists
        if token in self.index:
            return self.index[token].copy()

        # Return empty dictionary if token doesn't exist
        return {}

    # Retrieve the complete inverted index
    def get_index(self):

        # Return a copy to protect the original index
        result = {}

        for token, postings in self.index.items():
            result[token] = postings.copy()

        return result

    # Calculate document frequency
    def get_document_frequency(self, token):

        if not isinstance(token, str):
            raise TypeError("Token must be a string")

        if token in self.index:
            return len(self.index[token])

        return 0

    # Retrieve all document IDs
    def get_document_ids(self):

        return self.document_ids.copy()