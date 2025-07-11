import streamlit as st
import os
import ssl
import urllib3
import warnings
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import json

# Set environment variables to disable SSL verification and telemetry before any other imports
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ['LANGCHAIN_TELEMETRY'] = 'false'
os.environ['LANGSMITH_TRACING'] = 'false'
os.environ['LANGCHAIN_ANALYTICS'] = 'false'
os.environ['LANGCHAIN_CALLBACKS_MANAGER'] = 'false'
os.environ['LANGCHAIN_VERBOSE'] = 'false'
os.environ['LANGCHAIN_DEBUG'] = 'false'

# Suppress warnings
warnings.filterwarnings("ignore")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Import LangChain components
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Set page configuration
st.set_page_config(
    page_title="Pizza Restaurant RAG AI Agent",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B 0%, #FFD93D 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 0.8rem;
        border-radius: 10px 10px 2px 10px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .bot-message {
        background-color: #28a745;
        color: white;
        padding: 0.8rem;
        border-radius: 10px 10px 10px 2px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
    
    .example-questions {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background-color: #007bff;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vector_store_initialized' not in st.session_state:
    st.session_state.vector_store_initialized = False
if 'model_initialized' not in st.session_state:
    st.session_state.model_initialized = False

@st.cache_data
def load_restaurant_data():
    """Load and cache restaurant review data"""
    try:
        df = pd.read_csv("realistic_restaurant_reviews.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Restaurant reviews CSV file not found!")
        return None

@st.cache_resource
def initialize_vector_store():
    """Initialize and cache the vector store"""
    try:
        df = load_restaurant_data()
        if df is None:
            return None, None
        
        # Initialize embeddings
        embeddings = OllamaEmbeddings(
            model="mxbai-embed-large",
            base_url="http://localhost:11434"
        )
        
        db_location = "./chrome_langchain_db"
        add_documents = not os.path.exists(db_location)
        
        if add_documents:
            with st.spinner("🔄 Creating vector database for the first time..."):
                documents = []
                ids = []
                
                for i, row in df.iterrows():
                    document = Document(
                        page_content=row["Title"] + " " + row["Review"],
                        metadata={"rating": row["Rating"], "date": row["Date"]},
                        id=str(i)
                    )
                    ids.append(str(i))
                    documents.append(document)
                
                vector_store = Chroma(
                    collection_name="restaurant_reviews",
                    persist_directory=db_location,
                    embedding_function=embeddings
                )
                
                vector_store.add_documents(documents=documents, ids=ids)
        else:
            vector_store = Chroma(
                collection_name="restaurant_reviews",
                persist_directory=db_location,
                embedding_function=embeddings
            )
        
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        return vector_store, retriever
        
    except Exception as e:
        st.error(f"❌ Error initializing vector store: {str(e)}")
        return None, None

@st.cache_resource
def initialize_model():
    """Initialize and cache the LLM model"""
    try:
        model = OllamaLLM(
            model="llama3.2",
            base_url="http://localhost:11434"
        )
        
        template = """
You are an expert pizza restaurant review analyst. You help customers understand what others think about this pizza restaurant.

Here are some relevant reviews from customers: {reviews}

Based on these reviews, please answer the following question: {question}

Please provide a comprehensive and helpful answer based on the review content. If the reviews don't contain enough information to answer the question, please say so.
"""
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        
        return chain
        
    except Exception as e:
        st.error(f"❌ Error initializing model: {str(e)}")
        return None

def create_analytics_dashboard(df):
    """Create analytics dashboard with charts"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_rating = df['Rating'].mean()
        st.metric("Average Rating", f"{avg_rating:.1f}⭐")
    
    with col2:
        total_reviews = len(df)
        st.metric("Total Reviews", total_reviews)
    
    with col3:
        high_ratings = len(df[df['Rating'] >= 4])
        st.metric("High Ratings (4-5★)", high_ratings)
    
    with col4:
        recent_reviews = len(df[pd.to_datetime(df['Date']) >= '2024-02-01'])
        st.metric("Recent Reviews", recent_reviews)
    
    # Rating distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        fig_ratings = px.histogram(
            df, 
            x='Rating', 
            title='Rating Distribution',
            color_discrete_sequence=['#FF6B6B'],
            nbins=5
        )
        fig_ratings.update_layout(
            xaxis_title="Rating",
            yaxis_title="Number of Reviews",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
    
    with col2:
        # Ratings over time
        df['Date'] = pd.to_datetime(df['Date'])
        monthly_ratings = df.groupby(df['Date'].dt.to_period('M'))['Rating'].mean().reset_index()
        monthly_ratings['Date'] = monthly_ratings['Date'].astype(str)
        
        fig_timeline = px.line(
            monthly_ratings,
            x='Date',
            y='Rating',
            title='Average Rating Over Time',
            color_discrete_sequence=['#FFD93D']
        )
        fig_timeline.update_layout(
            xaxis_title="Month",
            yaxis_title="Average Rating",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🍕 Pizza Restaurant RAG AI Agent</h1>
        <p>Ask questions about our pizza restaurant reviews using AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 System Status")
        
        # Check Ollama connection
        try:
            from langchain_ollama.llms import OllamaLLM
            test_model = OllamaLLM(model="llama3.2", base_url="http://localhost:11434")
            # Try a simple test
            test_result = test_model.invoke("Hi")
            st.success("✅ Ollama Connected")
        except Exception as e:
            st.error("❌ Ollama Not Connected")
            st.info("Please ensure Ollama is running with models: llama3.2 and mxbai-embed-large")
        
        st.header("📊 Quick Stats")
        df = load_restaurant_data()
        if df is not None:
            st.metric("Total Reviews", len(df))
            st.metric("Average Rating", f"{df['Rating'].mean():.1f}⭐")
            st.metric("Date Range", f"{df['Date'].min()} to {df['Date'].max()}")
        
        st.header("💡 Example Questions")
        example_questions = [
            "Which pizzas have the best ratings?",
            "What do customers say about the pizza crust?",
            "Are there any gluten-free options?",
            "What are customers' main complaints?",
            "Tell me about the delivery service",
            "What do vegans think about this place?",
            "How is the pricing compared to other places?",
            "What makes this restaurant special?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{hash(question)}"):
                st.session_state.selected_question = question

    # Main content area
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Analytics", "📋 Reviews"])
    
    with tab1:
        # Initialize components
        if not st.session_state.vector_store_initialized:
            with st.spinner("🚀 Initializing AI system..."):
                vector_store, retriever = initialize_vector_store()
                if vector_store and retriever:
                    st.session_state.vector_store = vector_store
                    st.session_state.retriever = retriever
                    st.session_state.vector_store_initialized = True
                    st.success("✅ Vector store initialized!")
                else:
                    st.error("❌ Failed to initialize vector store")
                    st.stop()
        
        if not st.session_state.model_initialized:
            with st.spinner("🤖 Loading AI model..."):
                chain = initialize_model()
                if chain:
                    st.session_state.chain = chain
                    st.session_state.model_initialized = True
                    st.success("✅ AI model loaded!")
                else:
                    st.error("❌ Failed to load AI model")
                    st.stop()
        
        # Chat interface
        st.header("💬 Ask Questions About Pizza Reviews")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for i, (question, answer) in enumerate(st.session_state.chat_history):
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {question}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="bot-message">
                    <strong>AI Assistant:</strong> {answer}
                </div>
                """, unsafe_allow_html=True)
        
        # Question input
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_question = st.text_input(
                "Ask your question about the pizza restaurant:",
                key="user_input",
                placeholder="e.g., Which pizzas have the best ratings?"
            )
        
        with col2:
            ask_button = st.button("🚀 Ask", type="primary")
        
        # Handle example question selection
        if 'selected_question' in st.session_state:
            user_question = st.session_state.selected_question
            ask_button = True
            del st.session_state.selected_question
        
        # Process question
        if ask_button and user_question:
            if st.session_state.vector_store_initialized and st.session_state.model_initialized:
                with st.spinner("🔍 Analyzing reviews and generating response..."):
                    try:
                        # Retrieve relevant reviews
                        reviews = st.session_state.retriever.invoke(user_question)
                        
                        # Generate response
                        result = st.session_state.chain.invoke({
                            "reviews": reviews, 
                            "question": user_question
                        })
                        
                        # Add to chat history
                        st.session_state.chat_history.append((user_question, result))
                        
                        # Display the new response
                        st.markdown(f"""
                        <div class="user-message">
                            <strong>You:</strong> {user_question}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="bot-message">
                            <strong>AI Assistant:</strong> {result}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show relevant reviews used
                        with st.expander("📄 View source reviews used for this answer"):
                            for i, review in enumerate(reviews, 1):
                                st.write(f"**Review {i}:**")
                                st.write(f"*Rating: {review.metadata.get('rating', 'N/A')}⭐ | Date: {review.metadata.get('date', 'N/A')}*")
                                st.write(review.page_content)
                                st.divider()
                        
                    except Exception as e:
                        st.error(f"❌ Error processing question: {str(e)}")
            else:
                st.warning("⚠️ System not fully initialized. Please wait a moment and try again.")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    with tab2:
        st.header("📊 Restaurant Review Analytics")
        df = load_restaurant_data()
        if df is not None:
            create_analytics_dashboard(df)
        else:
            st.error("❌ Unable to load review data for analytics")
    
    with tab3:
        st.header("📋 All Reviews")
        df = load_restaurant_data()
        if df is not None:
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                rating_filter = st.selectbox(
                    "Filter by Rating",
                    ["All", "5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"]
                )
            
            with col2:
                sort_by = st.selectbox(
                    "Sort by",
                    ["Date (Newest)", "Date (Oldest)", "Rating (Highest)", "Rating (Lowest)"]
                )
            
            # Apply filters
            filtered_df = df.copy()
            if rating_filter != "All":
                rating_value = int(rating_filter.split()[0])
                filtered_df = filtered_df[filtered_df['Rating'] == rating_value]
            
            # Apply sorting
            if sort_by == "Date (Newest)":
                filtered_df = filtered_df.sort_values('Date', ascending=False)
            elif sort_by == "Date (Oldest)":
                filtered_df = filtered_df.sort_values('Date', ascending=True)
            elif sort_by == "Rating (Highest)":
                filtered_df = filtered_df.sort_values('Rating', ascending=False)
            elif sort_by == "Rating (Lowest)":
                filtered_df = filtered_df.sort_values('Rating', ascending=True)
            
            st.write(f"Showing {len(filtered_df)} of {len(df)} reviews")
            
            # Display reviews
            for idx, row in filtered_df.iterrows():
                with st.expander(f"⭐ {row['Rating']} - {row['Title']} ({row['Date']})"):
                    st.write(row['Review'])
        else:
            st.error("❌ Unable to load review data")

if __name__ == "__main__":
    main()
