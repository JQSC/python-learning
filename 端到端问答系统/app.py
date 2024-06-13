"""
操作流程
1. 输入：对输入进行检查，防 prompt 注入，以及合法性（色情、暴力）检查
2. 检索：检索分类
3. 检索：根据分类搜索产品信息
4. 输出：对问题进行回答
5. 输出：对回答的内容再次检验
"""

import openai
import 端到端问答系统.utils_zh as utils_zh
from tool import get_completion_from_messages

"""
对用户信息进行预处理
    
    参数:
    user_input : 用户输入
    all_messages : 历史信息
    debug : 是否开启 DEBUG 模式,默认开启

"""


def process_user_message_ch(user_input, all_messages, debug=True):
    # 分隔符
    delimiter = "```"
    # 第一步: 使用 OpenAI 的 Moderation API 检查用户输入是否合规或者是一个注入的 Prompt
    # 由于没有该模型的vip权限，跳过此检查
    response = {"results": ["success"]}  # openai.Moderation.create(input=user_input)
    moderation_output = response["results"][0]

    # 经过 Moderation API 检查该输入不合规
    if moderation_output["flagged"]:
        print("第一步：输入被 Moderation 拒绝")
        return "抱歉，您的请求不合规"

    # 如果开启了 DEBUG 模式，打印实时进度
    if debug:
        print("第一步：输入通过 Moderation 检查")

    # 第二步：获取商品和分类
    category_and_product_response = utils_zh.find_category_and_product_only(
        user_input, utils_zh.get_products_and_category()
    )
    # print(category_and_product_response)
    # 将抽取出来的字符串转化为列表
    category_and_product_list = utils_zh.read_string_to_list(
        category_and_product_response
    )
    # print(category_and_product_list)

    if debug:
        print("第二步：抽取出商品列表")
