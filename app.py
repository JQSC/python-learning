import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# 获取环境变量
api_key = os.environ["OPENAI_API_KEY_LOCAL"]


client = OpenAI(api_key=api_key, base_url="https://api.aigc369.com/v1")


# 调用openAI
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": """
         你的任务是分析使用三个单引号扩起来的源代码，生成函数的说明文档。
         首先理解代码中使用export导出的函数，理解函数的入参、返回值和函数功能。
         
         最后根据分析的结果以指定格式生成函数的功能文档。
         
         文档内容的格式如下，其中使用《》扩起来的为你需要补充的内容:
         ## 《函数命名》
         《简略的对函数功能的描述》
          
          #### Arguments
          《函数只有一个参数则为空，有多个参数则填充内容为：- 》《参数名称》：（`《参数的类型》`）: 《参数的功能说明》

          #### Returns
          `《参数的返回值类型》`:《返回值的功能说明》
         """,
        },
        {"role": "user", "content": prompt},
    ]

    # api文档：https://platform.openai.com/docs/api-reference/chat/object
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return completion.choices[0].message.content


# 获取目录下所有文件路径
def get_folder_path(folder_path):
    files = os.listdir(folder_path)
    list = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            list.append(file_path)
        else:
            list += get_folder_path(file_path)
    return list


# 生成文档
def run():
    # 读文件
    files = get_folder_path("./__test__/c")
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            # 调用模型
            content = f.read()
            message = get_completion(content)
            with open("./README_test.md", "a", encoding="utf-8") as fw:
                fw.write(message + "\n")
                print("开始写入:", file_path)
    print("完成!")


run()
