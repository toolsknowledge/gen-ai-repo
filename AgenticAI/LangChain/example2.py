from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# single sol
# OpenAIEmbeddings - Text -> embeddings
from langchain_openai import OpenAIEmbeddings


from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI

# Load document
# Step 1. load the doc
loader = TextLoader("company_policy.txt")
documents = loader.load()

# Split document 
# Step 2. Chunk Conf
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
) 

# Step3. docs (chunks)
docs = splitter.split_documents(documents)

# Convert text to embeddings
# Step 4. Create the Embeddings
embeddings = OpenAIEmbeddings(
    api_key=""
)

# Store in vector database
vector_store = FAISS.from_documents(
    docs,
    embeddings
)

# User question
question = "How many casual leaves are allowed?"

# Retrieve relevant content
retriever = vector_store.as_retriever()

relevant_docs = retriever.invoke(question)

context = "\n".join(
    [doc.page_content for doc in relevant_docs]
)

# Send context + question to LLM
prompt = f"""
Answer based on the context below.

Context:
{context}

Question:
{question}
"""

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=""
)

response = llm.invoke(prompt)

print(response.content)