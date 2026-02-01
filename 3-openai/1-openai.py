import os
from openai import OpenAI

# - 新加坡: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
client = OpenAI(
    api_key=os.getenv("ALI_BIANLIAN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{'role': 'user', 'content': '你是谁？'}]
)
print(completion.choices[0].message.content)