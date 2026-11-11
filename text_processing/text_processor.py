
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
