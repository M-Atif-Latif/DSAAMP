# Python AI Research Agent

## Overview

This project provides a command-line AI agent designed to assist with research tasks. The agent leverages large language models (LLMs) and custom tools to answer queries, summarize information, and provide structured research insights. It supports both OpenAI and Anthropic models, and uses Pydantic for robust output parsing.

## Features

- Query knowledge bases using natural language.
- Summarize and structure research results.
- Cite sources and list tools used for transparency.
- Command-line interface for easy interaction.
- Supports multiple LLM providers (OpenAI, Anthropic).
- Extensible with custom research tools.
- Graceful error handling and output validation.

## How It Works

1. **Environment Setup**: Loads API keys and environment variables from a `.env` file.
2. **Model Selection**: Uses OpenAI's GPT-4o-mini by default (switchable to Anthropic's Claude).
3. **Prompt Engineering**: Crafts a structured prompt for the LLM, instructing it to use tools and return output in a specific format.
4. **Tool Integration**: Integrates custom tools (search, wiki, save) for enhanced research capabilities.
5. **Output Parsing**: Uses Pydantic to validate and parse the LLM's response into a structured format.
6. **User Interaction**: Prompts the user for a research query and displays structured results.

## Example Usage

```bash
$ python research_agent.py
What can I help you research? Quantum computing applications in medicine
```

Example output:
```json
{
    "topic": "Quantum computing applications in medicine",
    "summary": "Quantum computing is being explored for drug discovery, genomics, and medical imaging. It offers potential speedups for complex simulations and data analysis.",
    "sources": [
        "https://www.nature.com/articles/s41586-019-1666-5",
        "https://www.ibm.com/blog/quantum-computing-healthcare/"
    ],
    "tools_used": [
        "search_tool",
        "wiki_tool"
    ]
}
```

## Requirements

- Python 3.10+
- `langchain`, `langchain_openai`, `langchain_anthropic`
- `pydantic`
- `python-dotenv`
- API keys for OpenAI and/or Anthropic (in `.env`)

## Setup

1. Clone the repository.
2. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
3. Create a `.env` file with your API keys:
     ```
     OPENAI_API_KEY=your_openai_key
     ANTHROPIC_API_KEY=your_anthropic_key
     ```
4. Run the agent:
     ```bash
     python main.py
     ```

## Customization

- Add or modify tools in `tools.py` to extend agent capabilities.
- Switch LLM providers by commenting/uncommenting the relevant lines in the code.

## License

This project is licensed under the MIT License.

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
