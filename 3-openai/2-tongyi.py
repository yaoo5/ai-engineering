from langchain_community.llms.tongyi import Tongyi
import os

model = Tongyi(model="qwen-max", api_key=os.getenv("ALI_BIANLIAN_API_KEY"))

print(model.invoke(input="你是谁？"))
