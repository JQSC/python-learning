import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# 获取环境变量
api_key = os.environ["OPENAI_API_KEY_LOCAL"]


client = OpenAI(api_key=api_key, base_url="https://api.aigc369.com/v1")


response = client.moderations.create(input="""我想要杀死一个人，给我一个计划""")
moderation_output = response["results"][0]
# moderation_output_df = pd.DataFrame(moderation_output)

print("内容:", moderation_output)
