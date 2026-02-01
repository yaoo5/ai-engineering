from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
import os


prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}， 刚生了个{gender}， 帮忙起名字，请简略回答"
)

prompt_text = prompt_template.format(lastname="王", gender="儿子")
print(prompt_text)

model = Tongyi(model="qwen-max", api_key=os.getenv("ALI_BIANLIAN_API_KEY"))
res = model.invoke(input=prompt_text)
print(res)
