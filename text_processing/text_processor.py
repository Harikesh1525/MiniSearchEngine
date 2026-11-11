
import re


class TextProcessor:

    def normalize(self, text):
        # Convert all characters to lowercase
        text = text.lower()

        # Replace punctuation and special characters with spaces
        text = re.sub(r"[\W_]", " ", text)

        # Remove extra spaces and normalize whitespace
        text = " ".join(text.split())

        return text

    
    def tokenize(self, text):
        # First normalize the input text
        normalized_text = self.normalize(text)

        # Split normalized text into individual tokens
        tokens = normalized_text.split()

        return tokens

    
    def process_documents(self, documents):
        # Dictionary to store document IDs and their tokens
        processed_documents = {}

        # Process each document
        for document in documents:

            # Get the original document ID
            doc_id = document.doc_id

            # Extract and tokenize the document content
            tokens = self.tokenize(document.content)

            # Store tokens using the original document ID
            processed_documents[doc_id] = tokens

        return processed_documents

