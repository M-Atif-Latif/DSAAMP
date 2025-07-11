# 🍕 Pizza Restaurant RAG AI Agent - Streamlit App

A professional Streamlit web application that brings the Local RAG AI Agent to life with a beautiful, interactive interface. This app allows users to ask questions about pizza restaurant reviews using AI-powered analysis with real-time chat, analytics dashboards, and comprehensive review management.

## ✨ Features

### 🤖 AI-Powered Chat Interface
- **Interactive Chat**: Real-time conversation with AI about restaurant reviews
- **Smart Retrieval**: Uses vector embeddings to find relevant reviews
- **Context-Aware Responses**: AI provides detailed answers based on actual customer reviews
- **Source Transparency**: View the exact reviews used to generate each answer

### 📊 Analytics Dashboard
- **Real-time Statistics**: Average ratings, total reviews, and trends
- **Interactive Charts**: Rating distribution and timeline analysis using Plotly
- **Performance Metrics**: Track restaurant performance over time

### 📋 Review Management
- **Complete Review Database**: Browse all restaurant reviews
- **Advanced Filtering**: Filter by rating, date, and other criteria
- **Smart Sorting**: Sort reviews by date, rating, or relevance
- **Rich Display**: Beautiful cards showing review details

### 🎨 Professional UI/UX
- **Modern Design**: Clean, professional interface with custom CSS
- **Responsive Layout**: Works perfectly on desktop and mobile
- **Interactive Elements**: Smooth animations and hover effects
- **Intuitive Navigation**: Easy-to-use tabs and sidebar

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running locally
3. Required Ollama models:
   ```bash
   ollama pull llama3.2
   ollama pull mxbai-embed-large
   ```

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd Ai_Agents/02_local_RAG_AI_agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama (if not already running):**
   ```bash
   ollama serve
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```
   
   Or use the launcher scripts:
   - **Windows Batch**: Double-click `run_app.bat`
   - **PowerShell**: Run `.\run_app.ps1`

5. **Open your browser** to `http://localhost:8501`

## 🖥️ App Interface

### Chat Tab 💬
- Ask natural language questions about the restaurant
- Get AI-powered responses based on customer reviews
- View chat history and source reviews
- Use example questions for quick starts

### Analytics Tab 📊
- Overview metrics (average rating, total reviews, etc.)
- Interactive rating distribution chart
- Timeline analysis showing rating trends
- Visual insights into customer satisfaction

### Reviews Tab 📋
- Browse all customer reviews
- Filter by rating (1-5 stars)
- Sort by date or rating
- Expandable review cards with full details

## 💡 Example Questions

Try asking these questions to see the AI in action:

- "Which pizzas have the best ratings?"
- "What do customers say about the pizza crust?"
- "Are there any gluten-free options?"
- "What are customers' main complaints?"
- "Tell me about the delivery service"
- "What do vegans think about this place?"
- "How is the pricing compared to other places?"
- "What makes this restaurant special?"

## 🔧 Technical Architecture

### Frontend (Streamlit)
- **Main App**: `streamlit_app.py` - Complete web interface
- **Styling**: Custom CSS for professional appearance
- **Charts**: Plotly for interactive visualizations
- **State Management**: Streamlit session state for chat history

### Backend (LangChain + Ollama)
- **Vector Store**: ChromaDB for efficient similarity search
- **Embeddings**: `mxbai-embed-large` model for text vectorization
- **LLM**: `llama3.2` for natural language generation
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate responses

### Data Processing
- **CSV Loader**: Pandas for restaurant review data
- **Document Processing**: LangChain Document objects with metadata
- **Caching**: Streamlit caching for optimal performance

## 📁 File Structure

```
02_local_RAG_AI_agent/
├── streamlit_app.py              # Main Streamlit application
├── main.py                       # Original command-line version
├── vector.py                     # Vector store initialization
├── requirements.txt              # Python dependencies
├── realistic_restaurant_reviews.csv  # Sample data
├── run_app.bat                   # Windows batch launcher
├── run_app.ps1                   # PowerShell launcher
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── chrome_langchain_db/         # Vector database (auto-created)
└── README_STREAMLIT.md          # This file
```

## ⚙️ Configuration

### Streamlit Settings
The app includes custom configuration in `.streamlit/config.toml`:
- Custom theme colors matching the pizza restaurant theme
- Optimized server settings
- Privacy-focused analytics settings

### Model Configuration
- **LLM Model**: `llama3.2` (can be changed in the code)
- **Embedding Model**: `mxbai-embed-large` (can be changed in the code)
- **Vector Search**: Top 5 most relevant reviews per query
- **Ollama URL**: `http://localhost:11434` (default)

## 🛠️ Customization

### Adding Your Own Data
Replace `realistic_restaurant_reviews.csv` with your own data. Ensure it has these columns:
- `Title`: Review title
- `Date`: Review date (YYYY-MM-DD format)
- `Rating`: Numeric rating (1-5)
- `Review`: Full review text

### Changing Models
Modify the model names in `streamlit_app.py`:
```python
# Change LLM model
model = OllamaLLM(model="your-preferred-model")

# Change embedding model
embeddings = OllamaEmbeddings(model="your-embedding-model")
```

### UI Customization
The app uses custom CSS in the `st.markdown()` sections. You can modify:
- Colors and gradients
- Typography and spacing
- Component styling
- Layout and animations

## 🚨 Troubleshooting

### Common Issues

1. **Ollama Not Connected**
   - Ensure Ollama is running: `ollama serve`
   - Check if models are installed: `ollama list`
   - Verify Ollama is accessible at `http://localhost:11434`

2. **Vector Store Issues**
   - Delete `chrome_langchain_db` folder to rebuild
   - Check CSV file format and location
   - Ensure sufficient disk space

3. **Performance Issues**
   - Close unused browser tabs
   - Restart the Streamlit app
   - Check system memory usage

4. **Model Loading Errors**
   - Pull required models: `ollama pull llama3.2` and `ollama pull mxbai-embed-large`
   - Check internet connection for first-time model downloads
   - Ensure sufficient disk space for models

### Error Messages

- **"CSV file not found"**: Ensure `realistic_restaurant_reviews.csv` is in the same directory
- **"Vector store initialization failed"**: Check Ollama connection and embedding model availability
- **"Model loading failed"**: Verify LLM model is available in Ollama

## 🔮 Future Enhancements

### Planned Features
- **Multi-document Support**: Upload your own CSV files through the UI
- **Advanced Analytics**: Sentiment analysis and keyword extraction
- **Export Functionality**: Download chat history and analytics reports
- **User Preferences**: Save favorite questions and custom settings
- **Real-time Data**: Connect to live review feeds
- **Multi-language Support**: Support for reviews in different languages

### Contribution Ideas
- Add more chart types and visualizations
- Implement user authentication and sessions
- Create mobile-responsive design improvements
- Add voice input/output capabilities
- Integrate with external review platforms

## 📄 License

This project is for educational purposes and demonstrates RAG implementation with local LLMs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the original project README
3. Open an issue on the repository

---

**Enjoy exploring the power of RAG AI with this professional Streamlit interface! 🍕✨**
