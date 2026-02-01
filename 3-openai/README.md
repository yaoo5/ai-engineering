# 笔记

链接：[B站｜黑马程序员大模型RAG与Agent智能体项目实战教程](https://www.bilibili.com/video/BV1yjz5BLEoY?spm_id_from=333.788.videopod.episodes&vd_source=622cfd4425afe4729159a73ce5cc2552&p=18)

```bash
pip install langchain langchain-community langchain-ollama dashscope chromadb
```

- langchain:核心包
- langchain-community:社区支持包,提供了更多的第三方模型调用(我们用的阿里云千问模型就需要这个包)
- langchain-ollama:Ollama支持包,支持调用0llama托管部署的本地模型
- dashscope:阿里云通义千问的PythonSDK
- chromadb:轻量向量数据库(后续使用)


## RAG的工作原理
离线流程：文档/私有知识加载 -> 分割 -> 向量化 -> 向量数据库

检索流程：用户提问  -> 检索环节 -> Prompt融合 -> 大模型回答

- 向量：embedding模型。一般1536维是比较好的选择。
- 余弦相似度：


## 三种大模型

- 大语言模型：qwen-max

- 聊天模型：qwen3-max

- 文本嵌入模型（向量）：

## 专业术语
- Ollama：一个基于Python的AI模型平台，支持本地部署和云服务。

- LangChain：一个基于Python的AI框架，用于构建大模型应用。

- Chroma：一个基于Python的向量数据库，用于存储和检索向量数据。

- 