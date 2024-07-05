import json
from pathlib import Path
from pprint import pprint, pformat
from SoupStrainer import bs4
from langchain_community.document_loaders import WebBaseLoader

# 使用 JSONLoader
from langchain_community.document_loaders import JSONLoader


def getJson():
    # 返回 pathlib.Path 对象
    file_path = Path(__file__).parent / "chat.json"

    data = json.loads(file_path.read_text())

    formatted_data = pformat(data)
    print(formatted_data)


# JsonLoader
def getJsonLoader():
    file_path = Path(__file__).parent / "chat.json"

    loader = JSONLoader(
        file_path=file_path,
        jq_schema=".messages[].content",
        text_content=False,
    )

    data = loader.load()
    pprint(data)


def webLoader():
    bs4_strainer = SoupStrainer(class_=("post-title", "post-header", "post-content"))

    loader = WebBaseLoader(
        web_path="https://lilianweng.github.io/posts/2023-06-23-agent/",
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    pprint(docs)


webLoader()
