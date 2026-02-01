from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables.base import RunnableSerializable
import os

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一名来自边塞的诗人"),
    MessagesPlaceholder("history"),
    ("human", "请帮我写一首关于岁月日航的诗")
])

history_data = [
    ("human", "给我写一首唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土。未知，未知"),
    ("human", "给予你上一首的格式，再来一首"),
    ("ai", "床前明月光，疑是地上霜。举头望明月，低头思故乡")
]

model = ChatTongyi(model="qwen3-max", api_key=os.getenv("ALI_BIANLIAN_API_KEY"))

chain: RunnableSerializable = chat_prompt_template | model

chain.invoke({"history": history_data})

for chunk in chain.stream({"history": history_data}):
    print(chunk.content, end="", flush=True)