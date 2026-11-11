
from document_handler.document_manager import DocumentManager


manager = DocumentManager("documents")

documents = manager.load_documents()

print("\nPROCESSED DOCUMENTS")
print("-------------------")

for doc in documents:
    print("ID:", doc.doc_id)
    print("Name:", doc.file_name)
    print("Path:", doc.path)
    print("Type:", doc.file_type)
    print("Content:", doc.content[:80])
    print("-------------------")


print("\nERRORS")
print("------")

for error in manager.get_errors():
    print(error)

