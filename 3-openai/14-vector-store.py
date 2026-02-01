from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
import os

# 生产环境可以用 chroma
vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(dashscope_api_key=os.getenv("ALI_BIANLIAN_API_KEY")),
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",
)

documents = loader.load()

vector_store.add_documents(
    documents=documents,
    ids=[f"id{i}" for i in range(1, len(documents)+1)]
)
vector_store.delete(["id1", "id2"])

results = vector_store.similarity_search("python是不是简单易学啊", 3)
for result in results:
    print(result.page_content)
    print("="*20)
