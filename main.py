
from document_handler.document_manager import DocumentManager
from text_processing.text_processor import TextProcessor
from inverted_index.inverted_index import InvertedIndex
from query_processing.query_processor import QueryProcessor


def main():
    print("=" * 50)
    print("          MINI SEARCH ENGINE")
    print("=" * 50)

    # Step 1: Get folder path from the user
    folder_path = input("\nEnter the folder path to search: ").strip()
    folder_path = folder_path.strip('"')

    if not folder_path:
        print("Error: Folder path cannot be empty.")
        return

    try:
        # Step 2: Load documents
        print("\nLoading documents...")
        document_manager = DocumentManager(folder_path)
        documents = document_manager.load_documents()

        if not documents:
            print("No supported documents found in this folder.")
            return

        print(f"Loaded {len(documents)} documents.")

        # Display files that could not be read
        errors = document_manager.get_errors()
        if errors:
            print(f"\nWarning: {len(errors)} file(s) could not be read.")
            for error in errors:
                print(f"- {error['path']}: {error['error']}")

        # Step 3: Process document text
        print("\nProcessing documents...")
        text_processor = TextProcessor()
        processed_documents = text_processor.process_documents(documents)

        # Step 4: Build inverted index
        print("Building inverted index...")
        inverted_index = InvertedIndex()
        inverted_index.build_index(processed_documents)

        # Step 5: Initialize query processor
        query_processor = QueryProcessor(text_processor)

        print("\nSearch engine is ready!")
        print("Enter a search query, or type 'exit' to quit.")

        # Step 6: Search loop
        while True:
            query = input("\nSearch: ").strip()

            if query.lower() == "exit":
                print("Thank you for using Mini Search Engine!")
                break

            if not query:
                print("Please enter a search query.")
                continue

            results = query_processor.search(
                query,
                inverted_index,
                documents
            )

            # Step 7: Display results
            if not results:
                print("No matching documents found.")
                continue

            print(f"\nFound {len(results)} matching document(s):")

            for rank, result in enumerate(results, start=1):
                print(f"\n{rank}. {result['file_name']}")
                print(f"   Path: {result['path']}")
                print(f"   Matched terms: {', '.join(result['matched_terms'])}")
                print(f"   Snippet: {result['snippet']}")

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"\nFolder error: {error}")

    except PermissionError as error:
        print(f"\nPermission error: {error}")

    except Exception as error:
        print(f"\nAn unexpected error occurred: {error}")


if __name__ == "__main__":
    main()
