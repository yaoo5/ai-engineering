from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.llms.tongyi import Tongyi
import os

example_template = PromptTemplate.from_template("单词：{word}， 反义词：{antonym}")

example_data = [
    {"word": "好", "antonym": "坏"},
    {"word": "大", "antonym": "小"},
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=example_data,
    prefix="给出给定词的反义词，有如下示例：",
    suffix="基于示例告诉我，{input_word}的反义词是？",
    input_variables=["input_word"],
)

prompt_text = few_shot_prompt.invoke(input={"input_word": "左"}).to_string()
print(prompt_text)

model = Tongyi(model="qwen-max", api_key=os.getenv("ALI_BIANLIAN_API_KEY"))

res = model.invoke(input=prompt_text)
print(res)
