"""
Demo script to test the vector store initialization for the Pizza Restaurant RAG AI Agent
"""

import os
import ssl
import urllib3
import warnings

# Set environment variables before any other imports
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ['LANGCHAIN_TELEMETRY'] = 'false'
os.environ['LANGSMITH_TRACING'] = 'false'
os.environ['LANGCHAIN_ANALYTICS'] = 'false'

warnings.filterwarnings("ignore")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

def test_ollama_connection():
    """Test if Ollama is accessible"""
    try:
        from langchain_ollama.llms import OllamaLLM
        print("🔄 Testing Ollama connection...")
        
        model = OllamaLLM(
            model="llama3.2",
            base_url="http://localhost:11434"
        )
        
        response = model.invoke("Hello, this is a test.")
        print("✅ Ollama connection successful!")
        print(f"📝 Test response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {str(e)}")
        return False

def test_embedding_model():
    """Test if embedding model is available"""
    try:
        from langchain_ollama import OllamaEmbeddings
        print("🔄 Testing embedding model...")
        
        embeddings = OllamaEmbeddings(
            model="mxbai-embed-large",
            base_url="http://localhost:11434"
        )
        
        test_embedding = embeddings.embed_query("This is a test query")
        print("✅ Embedding model working!")
        print(f"📊 Embedding dimension: {len(test_embedding)}")
        return True
    except Exception as e:
        print(f"❌ Embedding model failed: {str(e)}")
        return False

def test_vector_store():
    """Test vector store initialization"""
    try:
        print("🔄 Testing vector store initialization...")
        import pandas as pd
        from langchain_ollama import OllamaEmbeddings
        from langchain_chroma import Chroma
        from langchain_core.documents import Document
        
        # Load sample data
        df = pd.read_csv("realistic_restaurant_reviews.csv")
        print(f"📋 Loaded {len(df)} reviews from CSV")
        
        # Initialize embeddings
        embeddings = OllamaEmbeddings(
            model="mxbai-embed-large",
            base_url="http://localhost:11434"
        )
        
        # Check if vector store exists
        db_location = "./chrome_langchain_db"
        if os.path.exists(db_location):
            print(f"📁 Vector store already exists at {db_location}")
            vector_store = Chroma(
                collection_name="restaurant_reviews",
                persist_directory=db_location,
                embedding_function=embeddings
            )
        else:
            print("🆕 Creating new vector store...")
            documents = []
            for i, row in df.head(5).iterrows():  # Test with first 5 reviews
                document = Document(
                    page_content=row["Title"] + " " + row["Review"],
                    metadata={"rating": row["Rating"], "date": row["Date"]},
                    id=str(i)
                )
                documents.append(document)
            
            vector_store = Chroma(
                collection_name="restaurant_reviews",
                persist_directory=db_location,
                embedding_function=embeddings
            )
            
            vector_store.add_documents(documents=documents, ids=[str(i) for i in range(5)])
            print("✅ Vector store created successfully!")
        
        # Test retrieval
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})
        results = retriever.invoke("pizza quality")
        print(f"🔍 Retrieved {len(results)} relevant documents for test query")
        
        return True
    except Exception as e:
        print(f"❌ Vector store test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🍕 Pizza Restaurant RAG AI Agent - System Test")
    print("=" * 50)
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Embedding Model", test_embedding_model),
        ("Vector Store", test_vector_store)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        results[test_name] = test_func()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed! You can now run the Streamlit app.")
        print("💡 Run: streamlit run streamlit_app.py")
    else:
        print("\n⚠️  Some tests failed. Please check your setup:")
        print("   1. Ensure Ollama is running: ollama serve")
        print("   2. Install required models:")
        print("      - ollama pull llama3.2")
        print("      - ollama pull mxbai-embed-large")
        print("   3. Check that the CSV file exists in the current directory")

if __name__ == "__main__":
    main()
