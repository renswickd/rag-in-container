## RAG Policy Assistant

The RAG Policy Assistant is a Retrieval-Augmented Generation (RAG) application designed to answer user queries based on knowledge extracted from PDF documents and associated metadata. This application utilizes a knowledge graph and embeddings stored in Chroma DB to provide accurate and relevant responses.

### Project Structure

```
rag-policy-assistant
├── src
│   ├── components
│   │   ├── document_loader.py       # Loads PDF documents from the data/policy_documents/ directory.
│   │   ├── document_processor.py     # Processes loaded documents for analysis and embedding.
│   │   ├── embedding_manager.py      # Manages embedding of documents and metadata into Chroma DB.
│   │   ├── knowledge_graph.py        # Constructs a knowledge graph from embedded documents and metadata.
│   │   ├── metadata_handler.py       # Manages loading and processing of policy_records_metadata.csv.
│   │   ├── query_engine.py           # Handles user queries and retrieves information from the knowledge graph.
│   │   └── rag_nodes.py              # Defines nodes used in the Retrieval-Augmented Generation process.
│   ├── config
│   │   └── settings.py               # Contains configuration settings for the application.
│   ├── data
│   │   ├── policy_documents           # Directory for policy documents (PDFs).
│   │   └── policy_records_metadata.csv # Metadata related to the policy documents.
│   ├── utils
│   │   ├── logger.py                  # Provides logging functionality for the application.
│   │   └── helpers.py                 # Contains utility functions for various tasks.
│   ├── chromadb                       # Directory for Chroma DB files.
│   └── main.py                        # Entry point of the application.
├── tests                              # Directory for unit tests.
├── .env                               # Environment variables for the application.
├── .gitignore                         # Specifies files to be ignored by version control.
├── requirements.txt                   # Lists dependencies required for the project.
└── README.md                          # Documentation for the project.
```

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd rag-policy-assistant
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in the `.env` file as needed.

### Usage

To run the application, execute the following command:
```
python src/main.py
```

### Testing

To run the unit tests, use:
```
pytest tests/
```

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.# rag-in-container
