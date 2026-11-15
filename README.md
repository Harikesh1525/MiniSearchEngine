# Mini Search Engine

A Python-based mini search engine that searches local documents using text processing, an inverted index, and TF-IDF ranking.

## Features

- Reads TXT, PDF, and DOCX files.
- Recursively scans a selected folder and its subfolders for supported documents.
- Extracts text from documents, normalizes it, and tokenizes it.
- Builds an inverted index containing each term's frequency in each document.
- Processes queries using the same normalization and tokenization steps.
- Supports prefix matching (for example, `pyth` can match `python`).
- Ranks matching documents using a TF-IDF-style score.
- Displays filenames, file paths, matched terms.
- Reports files that could not be read while continuing with readable documents.

## Project structure

```
MiniSearchEngine/
├── document_handler/
│   ├── __init__.py
│   ├── document.py
│   ├── document_reader.py
│   └── document_manager.py
├── text_processing/
│   ├── __init__.py
│   └── text_processor.py
├── inverted_index/
│   ├── __init__.py
│   └── inverted_index.py
├── query_processing/
│   ├── __init__.py
│   └── query_processor.py
├── documents/
├── tests/
│   ├── test_document_handler.py
│   ├── test_inverted_index.py
│   ├── test_query_processor.py
│   └── test_text_processor.py
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

Dependencies are listed in `requirements.txt`:

- `pypdf` — PDF text extraction
- `python-docx` — DOCX text extraction
- `reportlab` — used by the document-handler tests to generate sample PDFs

## Installation

Open a terminal in the project root directory.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Linux / macOS**
```bash
source venv/bin/activate
```

**Windows (Command Prompt)**
```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the search engine

From the project root, execute:

```bash
python main.py
```

When prompted, enter the path to the folder you want to search. The program recursively scans it for `.txt`, `.pdf`, and `.docx` files.

Example:

```
Enter the folder path to search: documents

Loading documents...
Loaded 3 documents.

Processing documents...
Building inverted index...

Search engine is ready!
Enter a search query, or type 'exit' to quit.

Search: python
```

## How it works

1. **Document handling** — discovers supported files, extracts their text, and assigns document IDs.
2. **Text processing** — converts text to lowercase, replaces punctuation and special characters with spaces, and splits the normalized text into tokens.
3. **Inverted indexing** — stores each token with the document IDs in which it occurs and its frequency in each document.
4. **Query processing** — applies the same normalization and tokenization to the user's query.
5. **Matching and ranking** — finds indexed terms that begin with each query token and calculates a TF-IDF-style score for documents containing those terms.
6. **Displaying results** — presents matching documents in descending score order with matched terms and a text snippet.

The scoring implementation uses:

- Term frequency(TF): 1 + ln(term frequency)
- Inverse document frequency(IDF): 1 + ln((N + 1) / (document frequency + 1))

Here, N is the number of indexed documents.

## Run the tests

From the project root, run:

```bash
python -m pytest -q
```

Alternatively, the tests use Python's `unittest` framework:

```bash
python -m unittest discover -s tests -v
```

The test suite covers document reading and loading, text normalization and tokenization, inverted-index construction, query processing, prefix matching, ranking, and snippet generation.

## Supported document formats

| Format | Extension | Reader |
| Plain text | `.txt` | Python text file handling |
| PDF | `.pdf` | `pypdf` |
| Word document | `.docx` | `python-docx` |

""Files with other extensions are ignored during folder scanning.""

## Current scope and limitations

- The engine searches local files; it does not crawl websites or the internet.
- Only TXT, PDF, and DOCX files are supported.
- Image-only or scanned PDFs may not provide extractable text.
- Search uses prefix matching, not fuzzy or semantic search.
- The index is built when the program starts and is not persisted between runs.
- The interface is terminal-based.

## Used Topics

- Python
- OOP
- Bash
- Git
- Unix Commands

## Team

**Project 13: Mini Search Engine**

-Document Handling and Processing - HARIKESH (document_handler).
-Text Processing and Tokenization - BHUVAN (text_processing).
-Building Inverted Index          - HARSHITH (inverted_index).
-Query Processing                 - DEVA CHARAN (query_processing).
-Ranking, Integration, testing    - MURALI KRISHNA (Developed ranking in query_processing and main.py).
