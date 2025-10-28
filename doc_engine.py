import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI as LlamaOpenAI

# Load your OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Please check your .env file or environment variables.")

# Initialize the LlamaIndex LLM wrapper
llama_llm = LlamaOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

# Load documents from the 'data' directory
documents = SimpleDirectoryReader('data').load_data()

# Create a vector store index from the documents
index = VectorStoreIndex.from_documents(documents)

# Create a query engine
query_engine = index.as_query_engine(llm=llama_llm)

# Define function to query the documents
def query_documents(user_query: str) -> str:
    response = query_engine.query(user_query)
    return str(response)
