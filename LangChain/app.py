import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

_ = load_dotenv(find_dotenv())


# 获取环境变量
api_key = os.environ["OPENAI_API_KEY_LOCAL"]
base_url = os.environ["OPENAI_BASE_URL"]


# chat = ChatOpenAI(api_key=api_key, base_url=base_url, temperature=0, max_tokens=2048)

# print(chat)


# 首先，构造一个提示模版字符串：`template_string`
template_string = """把由三个反引号分隔的文本\
翻译成一种{style}风格。\
文本: ```{text}```
"""

# 然后，我们调用`ChatPromptTemplatee.from_template()`函数将
# 上面的提示模版字符`template_string`转换为提示模版`prompt_template`

prompt_template = ChatPromptTemplate.from_template(template_string)


print("\n", prompt_template.messages[0].prompt)
