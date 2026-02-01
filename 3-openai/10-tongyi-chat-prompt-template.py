from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
import os


chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一名来自边塞的诗人"),
    MessagesPlaceholder("history"),
    ("human", "请帮我写一首关于岁月蹉跎的诗")
])

history_data = [
    ("human", "给我写一首唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦"),
    ("human", "给予你上一首的格式，再来一首"),
    ("ai", "床前明月光，疑是地上霜。举头望明月，低头思故乡")
]

prompt_value = chat_template.invoke({"history": history_data}).to_string()
print(prompt_value)

chat = ChatTongyi(model="qwen3-max", api_key=os.getenv("ALI_BIANLIAN_API_KEY"))
res = chat.invoke(prompt_value)
print(res.content)
