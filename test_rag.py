from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Connect to the saved policy database
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Search the company policy
results = vectorstore.similarity_search(
    "Can employees upload customer data to personal cloud storage?",
    k=2
)

for doc in results:
    print("\nPolicy information:")
    print(doc.page_content)
