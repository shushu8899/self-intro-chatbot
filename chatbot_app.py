import os
import json
import getpass
from openai import OpenAI
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#!pip install langchain_pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders.csv_loader import CSVLoader
import time
from typing import Sequence
import streamlit as st
from langchain_core.messages import HumanMessage
import bs4
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing_extensions import Annotated, TypedDict
from uuid import uuid4
from langchain_core.documents import Document

from querying import generate_ans

### cd to demo folder
### Comand to run: streamlit run chatbot_app.py

with open("secrets/openai_key.json", "r") as f:
    openai_secrets = json.load(f)
os.environ["OPENAI_API_KEY"] = openai_secrets["openai_api_key"]
client = OpenAI()

with open("secrets/pinecone_key.json", "r") as f:
    pinecone_secrets = json.load(f)
pc = Pinecone(pinecone_secrets["pinecone_api_key"])

index_name = "langchain-test-index"  # change if desired

index = pc.Index(index_name)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

vector_store = PineconeVectorStore(index=index, embedding=embeddings)
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.5},
)

st.title("Ask me anything")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = generate_ans(prompt, st.session_state.messages, llm, retriever)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})