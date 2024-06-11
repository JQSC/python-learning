import json
import openai
from collections import defaultdict

# 商品和目录的数据文件
products_file = "products.json"
categories_file = "categories.json"

# 分隔符
delimiter = "####"
# 第二步（抽取商品）系统信息文本
step_2_system_message_content = f"""
您将获得一次客户服务对话。最近的用户查询将使用{delimiter}字符进行分隔。

输出一个Python对象列表，其中每个对象具有以下格式：
'category': <包括以下几个类别：Computers and Laptops、martphones and Accessories、elevisions and Home Theater Systems、elevisions and Home Theater Systems、elevisions and Home Theater Systems、'category': <包括以下几个类别：Computers and Laptops、martphones and Accessories、elevisions and Home Theater Systems、elevisions and Home Theater Systems、elevisions and Home Theater Systems、相机和摄像机>,
或者
'products': <必须是下面的允许产品列表中找到的产品>

类别和产品必须在客户服务查询中找到。
如果提到了产品，它必须与下面的允许产品列表中的正确类别相关联。
如果未找到任何产品或类别，请输出一个空列表。
只列出之前对话的早期部分未提及和讨论的产品和类别。

允许的产品：

Computers and Laptops类别：
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Smartphones and Accessories类别：
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

Televisions and Home Theater Systems类别：
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV

Gaming Consoles and Accessories类别：
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

Audio Equipment类别：
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

Cameras and Camcorders类别：
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera

只输出对象列表，不包含其他内容。
"""

step_2_system_message = {"role": "system", "content": step_2_system_message_content}

# 第四步（生成用户回答）的系统信息
step_4_system_message_content = f"""
    你是一家大型电子商店的客户服务助理。
    以友好和乐于助人的语气回答，回答保持简洁明了。
    确保让用户提出相关的后续问题。
"""

step_4_system_message = {"role": "system", "content": step_4_system_message_content}

# 第六步（验证模型回答）的系统信息
step_6_system_message_content = f"""
    你是一个助手，评估客户服务代理的回答是否足够回答客户的问题，并验证助手从产品信息中引用的所有事实是否正确。
    对话历史、产品信息、用户和客户服务代理的消息将用```进行分隔。
    请用一个字母回答，不带标点符号：
    Y - 如果输出足够回答问题，并且回答正确使用了产品信息
    N - 输出不足够回答问题，或者没有正确使用产品信息

    只输出一个字母。
"""

step_6_system_message = {"role": "system", "content": step_6_system_message_content}


# 使用 ChatCompletion 接口
def get_completion_from_messages(
    messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500
):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]


# 获取目录数据
def get_categories():
    with open(categories_file, "r") as file:
        categories = json.load(file)
    return categories


# 获取商品列表
def get_product_list():
    """
    具体原理参见第四节课
    """
    products = get_products()
    product_list = []
    for product in products.keys():
        product_list.append(product)

    return product_list


# 获取商品和目录
def get_products_and_category():
    """
    具体原理参见第五节课
    """
    products = get_products()
    products_by_category = defaultdict(list)
    for product_name, product_info in products.items():
        category = product_info.get("category")
        if category:
            products_by_category[category].append(product_info.get("name"))

    return dict(products_by_category)


# 从商品数据中获取
def get_products():
    with open(products_file, "r") as file:
        products = json.load(file)
    return products


# 从用户问题中抽取商品和类别
def find_category_and_product(user_input, products_and_category):
    delimiter = "####"
    system_message = f"""
    您将获得客户服务查询。
    客户服务查询将使用{delimiter}字符分隔。
    输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
    'category': <包括以下几个类别：Computers and Laptops，Smartphones and Accessories，Televisions and Home Theater Systems，Gaming Consoles and Accessories，Audio Equipment，Cameras and Camcorders>
    以及
    'products': <必须是下面的允许产品列表中找到的产品列表>

    其中类别和产品必须在客户服务查询中找到。
    如果提到了产品，则必须将其与允许产品列表中的正确类别关联。
    如果未找到任何产品或类别，则输出一个空列表。
    除了列表外，不要输出其他任何信息！

    允许的产品以JSON格式提供。
    每个项的键表示类别。
    每个项的值是该类别中的产品列表。
    允许的产品：{products_and_category}
    
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_input}{delimiter}"},
    ]
    return get_completion_from_messages(messages)


# 相比上一个函数，可获取的商品直接在 template 中限定
def find_category_and_product_only(user_input, products_and_category):
    delimiter = "####"
    system_message = f"""
您将获得客户服务查询。
客户服务查询将使用{delimiter}字符作为分隔符。
请仅输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
'category': <包括以下几个类别：Computers and Laptops、Smartphones and Accessories、Televisions and Home Theater Systems、Gaming Consoles and Accessories、Audio Equipment、Cameras and Camcorders>,
以及
'products': <必须是下面的允许产品列表中找到的产品列表>

类别和产品必须在客户服务查询中找到。
如果提到了某个产品，它必须与允许产品列表中的正确类别关联。
如果未找到任何产品或类别，则输出一个空列表。
除了列表外，不要输出其他任何信息！

允许的产品：

Computers and Laptops category:
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Smartphones and Accessories category:
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

Televisions and Home Theater Systems category:
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV

Gaming Consoles and Accessories category:
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

Audio Equipment category:
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

Cameras and Camcorders category:
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera
    
只输出对象列表，不包含其他内容。
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_input}{delimiter}"},
    ]
    return get_completion_from_messages(messages)


# 从问题中抽取商品
def get_products_from_query(user_msg):
    """
    代码来自于第五节课
    """
    products_and_category = get_products_and_category()
    delimiter = "####"
    system_message = f"""
    您将获得客户服务查询。
    客户服务查询将使用{delimiter}字符作为分隔符。
    请仅输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
    'category': <包括以下几个类别：Computers and Laptops、Smartphones and Accessories、Televisions and Home Theater Systems、Gaming Consoles and Accessories、Audio Equipment、Cameras and Camcorders>,
    以及
    'products': <必须是下面的允许产品列表中找到的产品列表>

    类别和产品必须在客户服务查询中找到。
    如果提到了某个产品，它必须与允许产品列表中的正确类别关联。
    如果未找到任何产品或类别，则输出一个空列表。
    除了列表外，不要输出其他任何信息！

    允许的产品以JSON格式提供。
    每个项目的键表示类别。
    每个项目的值是该类别中的产品列表。

    以下是允许的产品：{products_and_category}

    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_msg}{delimiter}"},
    ]
    category_and_product_response = get_completion_from_messages(messages)

    return category_and_product_response


# 商品信息的搜索
def get_product_by_name(name):
    products = get_products()
    return products.get(name, None)


def get_products_by_category(category):
    products = get_products()
    return [product for product in products.values() if product["category"] == category]


def get_mentioned_product_info(data_list):
    """
    具体原理参见第五、六节课
    """
    product_info_l = []

    if data_list is None:
        return product_info_l

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        product_info_l.append(product)
                    else:
                        print(f"错误: 商品 '{product_name}' 未找到")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    product_info_l.append(product)
            else:
                print("错误：非法的商品格式")
        except Exception as e:
            print(f"Error: {e}")

    return product_info_l


# 以下函数原理参见第五节课
def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        input_string = input_string.replace(
            "'", '"'
        )  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print(input_string)
        print("错误：非法的 Json 格式")
        return None


def generate_output_string(data_list):
    output_string = ""

    if data_list is None:
        return output_string
    # print(data_list)
    for data in data_list:
        try:
            if "products" in data:
                # print(data)
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                    else:
                        print(f"错误: 商品 '{product_name}' 没有找到")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4) + "\n"
            else:
                print("错误：非法的商品格式")
        except Exception as e:
            print(f"Error: {e}")

    return output_string


# Example usage:
# product_information_for_user_message_1 = generate_output_string(category_and_product_list)
# print(product_information_for_user_message_1)
# 回答用户问题
def answer_user_msg(user_msg, product_info):
    """
    代码参见第五节课
    """
    delimiter = "####"
    system_message = f"""
    您是一家大型电子商店的客户服务助理。\
    请用友好和乐于助人的口吻回答问题，提供简洁明了的答案。\
    确保向用户提出相关的后续问题。
    """
    # user_msg = f"""
    # tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_msg}{delimiter}"},
        {"role": "assistant", "content": f"相关产品信息:\n{product_info}"},
    ]
    response = get_completion_from_messages(messages)
    return response
