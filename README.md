#  LangChain RAG Chatbot App with Streamlit & Pinecone for self introduction

![Python](https://img.shields.io/badge/python-3.10%2B-blueviolet)

 **Retrieval-Augmented Generation (RAG)** chatbot built with **Streamlit** as a frontend, **LangChain** for orchestration, **OpenAI** for language and embedding models, and **Pinecone** as the vector database. It supports **context-aware conversation** and dynamically retrieves relevant content to answer user queries based on chat history.


##  Key Components

### 1. **Streamlit Frontend (`chatbot_app.py`)**
- Provides an interactive chat UI.
- Maintains chat history in `st.session_state`.
- Takes user input from `st.chat_input()` and renders messages.
- On each message:
  - Sends it to a LangChain RAG pipeline (`generate_ans`)
  - Displays streaming responses

### 2. **Contextual RAG Pipeline (`querying.py`)**
This script defines a full pipeline that includes:
- **History-Aware Question Rewriting**  
  Uses a prompt to make user questions standalone using previous context.
- **Retriever Creation**
  Wraps a Pinecone retriever with LangChain’s `create_history_aware_retriever`.
- **Contextual Answering**
  Uses retrieved documents to generate a concise, friendly answer using GPT-4-style LLM.
- **Streaming Response**
  Streams each token of the generated output back to the Streamlit frontend.

### 3. **Secrets Management**
You securely load credentials from:
- `secrets/openai_key.json` for OpenAI API Key
- `secrets/pinecone_key.json` for Pinecone API Key


