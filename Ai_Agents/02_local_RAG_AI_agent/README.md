# Local RAG AI Agent

A Retrieval-Augmented Generation (RAG) system using local LLMs and vector embeddings to answer questions about pizza restaurant reviews. This project demonstrates how to build a conversational AI agent that retrieves relevant information from a document collection and provides contextual answers.

---

## Features

- 🤖 **Local LLM Integration:** Uses Ollama with Llama 3 model for text generation
- 🔍 **Vector Search:** Implements ChromaDB for efficient similarity search
- 📊 **Document Processing:** Processes restaurant reviews from CSV data
- 💬 **Interactive Chat:** Command-line interface for asking questions
- 🍕 **Domain-Specific:** Specialized for pizza restaurant review analysis

---

## Architecture

The system consists of three main components:

1. **Vector Store (`vector.py`):**
    - Loads restaurant reviews from CSV
    - Creates embeddings using Ollama's `mxbai-embed-large` model
    - Stores vectors in ChromaDB for fast retrieval

2. **Main Application (`main.py`):**
    - Implements the chat interface
    - Combines retrieved reviews with user questions
    - Generates responses using Llama 3

3. **Data:**
    - CSV file containing realistic pizza restaurant reviews with ratings and dates (or your own CSV file with reviews)

---

## Prerequisites

- Python 3.8+
- Ollama installed locally
- Required Ollama models:
    - `llama3` (for text generation)
    - `mxbai-embed-large` (for embeddings)

---

## Installation

1. **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd 02_local_RAG_AI_agent
    ```

2. **Set Up Python Environment**
    ```bash
    conda create -n local_rag_ai_agent python=3.11 -y
    conda activate local_rag_ai_agent
    pip install -r requirements.txt
    ```

3. **Install and Configure Ollama**
    - Download and install Ollama from [https://ollama.ai](https://ollama.ai)
    - Pull the required models:
      ```bash
      ollama pull llama3
      ollama pull mxbai-embed-large
      ```

4. **Prepare Data**
    - Use the provided `realistic_restaurant_reviews.csv` or replace it with your own CSV file containing reviews.

---

## Usage

1. **Initialize the Vector Database (first run only):**
    ```bash
    python vector.py
    ```
    This will create the `chrome_langchain_db` directory with embedded reviews.

2. **Start the Chat Application:**
    ```bash
    python main.py
    ```

3. **Ask Questions about the Restaurant:**
    ```
    Ask your question (q to quit): What do customers say about the pizza crust?
    Ask your question (q to quit): Which pizzas have the best ratings?
    Ask your question (q to quit): Are there any gluten-free options?
    Ask your question (q to quit): q
    ```

---

## Example Queries

- What do customers say about the pizza crust?
- Are there any complaints about delivery?
- What are the most popular toppings?
- Which reviews mention gluten-free options?
- What do customers think about the pricing?

---

## Project Structure

```
02_local_RAG_AI_agent/
├── main.py                           # Main chat application
├── vector.py                         # Vector store setup and retrieval
├── realistic_restaurant_reviews.csv  # Sample restaurant review data
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── chrome_langchain_db/              # ChromaDB storage (created on first run)
```

---

## Dependencies

- `langchain`: Core framework for building LLM applications
- `langchain-ollama`: Ollama integration for LangChain
- `langchain-chroma`: ChromaDB vector store integration
- `pandas`: Data manipulation and CSV processing

---

## How It Works

1. **Data Loading:** Restaurant reviews are loaded from the CSV file containing titles, dates, ratings, and review text.
2. **Document Embedding:** Each review is converted into a vector embedding using the `mxbai-embed-large` model via Ollama.
3. **Vector Storage:** Embeddings are stored in ChromaDB for efficient similarity search.
4. **Query Processing:** When a user asks a question:
    - The question is embedded using the same model
    - Top 5 most similar reviews are retrieved
    - Retrieved reviews are combined with the question in a prompt template
5. **Response Generation:** The Llama 3 model generates a contextual response based on the retrieved reviews and the user's question.

---

## Customization

### Adding New Data

Replace `realistic_restaurant_reviews.csv` with your own data. Ensure it has columns:

- `Title`: Review title
- `Date`: Review date
- `Rating`: Numeric rating
- `Review`: Review text content

### Changing Models

Modify the model names in:

- `main.py`: Change `OllamaLLM(model="llama3")` to your preferred model
- `vector.py`: Change `OllamaEmbeddings(model="mxbai-embed-large")` to your preferred embedding model

### Adjusting Retrieval

In `vector.py`, modify the retriever parameters:

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}  # Retrieve top 5 documents
)
```

---

## Troubleshooting

- **Ollama Connection Issues:** Ensure Ollama is running (`ollama serve`)
- **Model Not Found:** Pull the required models using `ollama pull <model-name>`
- **Memory Issues:** Consider using smaller models or reducing the number of retrieved documents
- **Database Issues:** Delete the `chrome_langchain_db` directory to rebuild the vector store

---

## Future Enhancements

- Web interface using Streamlit or FastAPI
- Support for multiple data sources (CSV, PDF, Word, Text)
- Advanced filtering and search options
- Chat history and conversation memory
- Performance metrics and evaluation

---

## License

This project is for educational purposes and demonstrates RAG implementation with local LLMs.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

---

## Acknowledgements

- [Ollama](https://ollama.ai)
- [LangChain](https://python.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Codanics](https://codanics.com/)

---

## Tasks for Students

- Build an app where you can use this method to generate RAG-based questions and answers for any kind of document: CSV, PDF, Word, Text.
- Build a web app using Streamlit or FastAPI to interact with the RAG system.

---

# About the Author

<div style="background-color: #f8f9fa; border-left: 5px solid #28a745; padding: 20px; margin-bottom: 20px; border-radius: 5px;">
  <h2 style="color: #28a745; margin-top: 0; font-family: 'Poppins', sans-serif;">Muhammad Atif Latif</h2>
  <p style="font-size: 16px; color: #495057;">Data Scientist & Machine Learning Engineer</p>
  
  <p style="font-size: 15px; color: #6c757d; margin-top: 15px;">
    Passionate about building AI solutions that solve real-world problems. Specialized in machine learning, 
    deep learning, and data analytics with experience implementing production-ready models.
  </p>
</div>

## Connect With Me

<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
  <a href="https://github.com/m-Atif-Latif" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-Follow-212121?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://www.kaggle.com/matiflatif" target="_blank">
    <img src="https://img.shields.io/badge/Kaggle-Profile-20BEFF?style=for-the-badge&logo=kaggle" alt="Kaggle">
  </a>
  <a href="https://www.linkedin.com/in/muhammad-atif-latif-13a171318" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin" alt="LinkedIn">
  </a>
  <a href="https://x.com/mianatif5867" target="_blank">
    <img src="https://img.shields.io/badge/Twitter-Follow-1DA1F2?style=for-the-badge&logo=twitter" alt="Twitter">
  </a>
  <a href="https://www.instagram.com/its_atif_ai/" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-Follow-E4405F?style=for-the-badge&logo=instagram" alt="Instagram">
  </a>
  <a href="mailto:muhammadatiflatif67@gmail.com">
    <img src="https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail" alt="Email">
  </a>
</div>

---