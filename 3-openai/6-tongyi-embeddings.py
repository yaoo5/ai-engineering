from langchain_community.embeddings import DashScopeEmbeddings
import os

embed = DashScopeEmbeddings(model="text-embedding-v3", dashscope_api_key=os.getenv("ALI_BIANLIAN_API_KEY"))

print("**** embed example ****")
print(embed.embed_query("我喜欢你"))
print(embed.embed_documents(["我喜欢你", "我稀饭你", "晚上吃啥"]))