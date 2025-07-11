@echo off
echo Starting Pizza Restaurant RAG AI Agent...
echo.
echo Please ensure that:
echo 1. Ollama is running (ollama serve)
echo 2. Required models are installed:
echo    - ollama pull llama3.2
echo    - ollama pull mxbai-embed-large
echo.
echo Starting Streamlit app...
streamlit run streamlit_app.py
