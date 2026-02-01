from langchain_community.llms.tongyi import Tongyi
import os

model = Tongyi(model="qwen-max", api_key=os.getenv("ALI_BIANLIAN_API_KEY"))

res = model.stream(input="你是谁？")

for chunk in res:
    print(chunk, end="", flush=True)
