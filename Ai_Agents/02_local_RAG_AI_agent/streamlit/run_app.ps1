Write-Host "🍕 Starting Pizza Restaurant RAG AI Agent..." -ForegroundColor Green
Write-Host ""
Write-Host "Please ensure that:" -ForegroundColor Yellow
Write-Host "1. Ollama is running (ollama serve)" -ForegroundColor White
Write-Host "2. Required models are installed:" -ForegroundColor White
Write-Host "   - ollama pull llama3.2" -ForegroundColor White
Write-Host "   - ollama pull mxbai-embed-large" -ForegroundColor White
Write-Host ""
Write-Host "Starting Streamlit app..." -ForegroundColor Green
streamlit run streamlit_app.py
