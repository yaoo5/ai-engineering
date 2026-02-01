from langchain_community.chat_models.tongyi import ChatTongyi
import os
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

chat = ChatTongyi(model="qwen3-max", api_key=os.getenv("ALI_BIANLIAN_API_KEY"))

messages = [
    # SystemMessage(content="你是一名来自边塞的诗人"),
    # 以下为元组格式
    # ("user", "今天天气是：{weather}") 元组的好处在于可以传变量
    ("system", "你是一名来自边塞的诗人"),
    ("user", "给我写一首唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦"),   
    ("user", "给予你上一首的格式，再来一首")
]

for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)