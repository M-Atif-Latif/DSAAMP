import streamlit as st
from tools import search_tool, wiki_tool, save_tool
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# SSL fix for Windows
if 'SSL_CERT_FILE' in os.environ and not os.path.exists(os.environ['SSL_CERT_FILE']):
    del os.environ['SSL_CERT_FILE']

custom_client = httpx.Client(verify=False)

# Pydantic model for research response
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Output parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are a research assistant that will help generate a research paper.\n
        Answer the user query using the available tools efficiently.\n
        Use Wikipedia tool for general information and search tool for additional details.\n
        Once you have gathered sufficient information, provide the final answer in the specified JSON format.\n
        Be concise and focused in your research to avoid exceeding iteration limits.\n
        Wrap the final output in this format and provide no other text:\n
        {format_instructions}
    """),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

# Tools
TOOLS = [search_tool, wiki_tool, save_tool]

# Sidebar - App Info and Settings
st.sidebar.title("🧑‍🔬 AI Research Agent")
st.sidebar.markdown("""
**Instructions:**\n
- Enter a research query in the main panel.\n- The agent will use web search and Wikipedia to generate a structured research summary.\n- You can adjust settings below and download the results.\n""")

# Model and settings
model_choice = st.sidebar.selectbox("Select LLM Model", ["gpt-4o-mini"], index=0)
max_iter = st.sidebar.slider("Max Research Steps", 5, 40, 20)
verbose = st.sidebar.checkbox("Verbose Output (Show Agent Steps)", value=True)

# LLM
llm = ChatOpenAI(model=model_choice, http_client=custom_client)

# Agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=TOOLS
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=TOOLS,
    verbose=verbose,
    max_iterations=max_iter,
    handle_parsing_errors=True,
    early_stopping_method="generate"
)

def save_research_to_file(research_response, query, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_output_{timestamp}.txt"
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Research Query: {query}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        f.write(f"Topic: {research_response.topic}\n\n")
        f.write(f"Summary:\n{research_response.summary}\n\n")
        f.write(f"Sources Used:\n")
        for i, source in enumerate(research_response.sources, 1):
            f.write(f"{i}. {source}\n")
        f.write(f"\nTools Used: {', '.join(research_response.tools_used)}\n")
    return filepath

def get_downloadable_text(research_response, query):
    output = f"Research Query: {query}\n"
    output += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    output += "="*50 + "\n\n"
    output += f"Topic: {research_response.topic}\n\n"
    output += f"Summary:\n{research_response.summary}\n\n"
    output += f"Sources Used:\n"
    for i, source in enumerate(research_response.sources, 1):
        output += f"{i}. {source}\n"
    output += f"\nTools Used: {', '.join(research_response.tools_used)}\n"
    return output

# Main UI
st.title("🧑‍🔬 AI Research Agent")
st.markdown(
    """
    <style>
    .stButton>button {background-color: #4F8BF9; color: white; font-weight: bold;}
    .stSpinner {color: #4F8BF9 !important;}
    </style>
    """,
    unsafe_allow_html=True
)
st.write("Enter your research query below. The agent will use web search and Wikipedia to generate a structured research summary.")

query = st.text_input("What can I help you research?", "")
run_button = st.button("Run Research", use_container_width=True)

if run_button and query:
    with st.spinner("Running research agent..."):
        try:
            raw_response = agent_executor.invoke({"query": query})
            structured_response = parser.parse(raw_response.get("output"))
            st.success("Research complete!")
            st.subheader("📌 Topic")
            st.write(structured_response.topic)
            st.subheader("📝 Summary")
            st.write(structured_response.summary)
            st.subheader("🔗 Sources Used")
            for i, source in enumerate(structured_response.sources, 1):
                st.write(f"{i}. {source}")
            st.subheader("🛠️ Tools Used")
            st.write(", ".join(structured_response.tools_used))
            # Download button
            downloadable = get_downloadable_text(structured_response, query)
            st.download_button(
                label="Download Research Output",
                data=downloadable,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
            # Save to file button
            if st.button("Save Research Output to Server"):
                file_path = save_research_to_file(structured_response, query)
                st.info(f"Research saved to: {file_path}")
            # Show raw agent output if verbose
            if verbose:
                st.expander("Show Raw Agent Output").write(raw_response)
        except Exception as e:
            st.error(f"Error parsing response: {e}\nRaw Response: {raw_response if 'raw_response' in locals() else ''}")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, LangChain, and OpenAI.")
