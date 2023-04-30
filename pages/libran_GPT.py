#!/usr/bin/env python3
"""
Libran-GPT is a library for querying for conversational queries on personal PDFs
"""

__author__ = "Brian Koech"
__version__ = "0.1.0"
__license__ = "MIT"

# import libraries
import os
import re
import time
from io import BytesIO
from typing import Any, List, Dict

import openai
import streamlit as st
from langchain import LLMChain, OpenAI
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import VectorStore
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader

# Setup storage
this_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(this_dir)
data_dir = os.path.join(root_dir, "data")
images_dir = os.path.join(root_dir, "images")


# Parse PDF file and extract contents
@st.cache_data
def parse_data(file) -> List[str]:
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        # Merge hyphenated words
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        # Remove new lines in the middle of sentences
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        # Remove multiple newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)
        output.append(text)
    return output


# Define a function to convert the text to a list of documents
@st.cache_data
def text_to_docs(text: str) -> List[Document]:
    """Convert text to a list of documents with metadata."""
    if isinstance(text, str):
        # Take string and act as if it is a single document
        text = [text]
    page_docs = [Document(page_content=page) for page in text]

    # Add page numbers as metadata
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    # Split pages into chunks
    doc_chunks = []

    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            # Add source metadata
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)

    return doc_chunks


# Define a function for embedding the documents
@st.cache_data
def test_embed():
    embeddings = OpenAIEmbeddings(openai_api_key=api)
    # Indexing
    # Save in a VectorStore
    with st.spinner("Embedding documents..."):
        index = FAISS.from_documents(pages, embeddings)
    st.success("Embedding complete!", icon="✅")
    return index


# Setup Streamlit Interface

st.title("🤖 Libran-GPT: Personalised Conversational Search Bot With Memory 🧠")
st.markdown(
    """
        ####  🗨️ Chat with your PDF files 📜 with `Conversational Buffer Memory`
        > *Powered by [LangChain]('https://langchain.readthedocs.io/en/latest/modules/memory.html#memory') +
        [OpenAI]('https://platform.openai.com/docs/models/gpt-3-5') + [Streamlit](https://streamlit.io/)*
        ----
        """
)

st.markdown(
    """
    `openai`
    `langchain`
    `tiktoken`
    `pypdf`
    `faiss-cpu`

    ---------
    """
)

# Sidebar
st.sidebar.markdown(
    """
    ### Steps
    1. 📜 Upload PDF File
    2. 🔑 Enter OpenAI API Key
    2. 🤖 Chat with your PDF


    **Note : File content and API key not stored in any form.**
    """
)

# Upload PDF file
uploaded_file = st.file_uploader("**Upload Your PDF File**", type=["pdf"])

if uploaded_file:
    name_of_file = uploaded_file.name
    doc = parse_data(uploaded_file)
    pages = text_to_docs(doc)

if uploaded_file:
    name_of_file = uploaded_file.name
    doc = parse_data(uploaded_file)
    pages = text_to_docs(doc)
    if pages:
        # Allow the user to select a page and view its content
        with st.expander("Show Page Content", expanded=False):
            page_sel = st.number_input(
                label="Select Page", min_value=1, max_value=len(pages), step=1
            )
            pages[page_sel - 1]
        # Allow the user to enter an OpenAI API key
        api = st.text_input(
            "**Enter OpenAI API Key**",
            type="password",
            placeholder="sk-",
            help="https://platform.openai.com/account/api-keys",
        )
        if api:
            # Test the embeddings and save the index in a vector database
            index = test_embed()
            # Set up the question-answering system
            qa = RetrievalQA.from_chain_type(
                llm=OpenAI(openai_api_key=api),
                chain_type="map_reduce",
                retriever=index.as_retriever(),
            )
            # Set up the conversational agent
            tools = [
                Tool(
                    name="State of Union QA System",
                    func=qa.run,
                    description="Useful for when you need to answer questions about the aspects asked. Input may be a partial or fully formed question.",
                )
            ]
            prefix = """Have a conversation with a human, answering the following questions as best you can based on the context and memory available.
                        You have access to a single tool:"""
            suffix = """Begin!"
            {chat_history}
            Question: {input}
            {agent_scratchpad}"""

            prompt = ZeroShotAgent.create_prompt(
                tools,
                prefix=prefix,
                suffix=suffix,
                input_variables=["input", "chat_history", "agent_scratchpad"],
            )

            if "memory" not in st.session_state:
                st.session_state.memory = ConversationBufferMemory(
                    memory_key="chat_history"
                )

            llm_chain = LLMChain(
                llm=OpenAI(
                    temperature=0, openai_api_key=api, model_name="gpt-3.5-turbo"
                ),
                prompt=prompt,
            )
            agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
            agent_chain = AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=tools,
                verbose=True,
                memory=st.session_state.memory,
            )

            # Allow the user to enter a query and generate a response
            query = st.text_input(
                "**What's on your mind?**",
                placeholder="Ask me anything from {}".format(name_of_file),
            )

            if query:
                with st.spinner(
                    "Generating Answer to your Query : `{}` ".format(query)
                ):
                    res = agent_chain.run(query)
                    st.info(res, icon="🤖")

            # Allow the user to view the conversation history and other information stored in the agent's memory
            with st.expander("History/Memory"):
                st.session_state.memory

# Add a Image and a link to a blog post in the sidebar
with st.sidebar:
    logo_name = os.path.join(images_dir, "logo.png")
    st.image(logo_name, use_column_width=True)
