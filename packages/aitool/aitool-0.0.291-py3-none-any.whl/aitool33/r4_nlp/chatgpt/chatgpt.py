# -*- coding: UTF-8 -*-
# Copyright©2022 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

"""
from typing import Dict, Union, List, Any, NoReturn, Tuple
from aitool import pip_install


def chatgpt(text, api_key):
    """
    最简单的单句调用模式，用一句话作为输入
    :param text:
    :return:

    # 获取 api_key
    - 在openai官网注册账号
    - https://platform.openai.com/docs/quickstart/build-your-application 生成 api_key

    # 查看 api 额度
    - https://platform.openai.com/account/usage
    - 一次请求大概0.1元

    """
    try:
        import openai
    except ModuleNotFoundError:
        pip_install('openai')
        import openai

    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
                {'role': 'user', 'content': text},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    return result


if __name__ == '__main__':
    print(chatgpt('写一个爬虫爬取深圳每天的天气', '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'))
    """
    抱歉，作为语言模型，无法完成实际的网络爬取任务。但是，我们可以提供一个参考的Python代码框架，供开发者参考。

    ```python
    import requests
    from bs4 import BeautifulSoup
    
    url = "https://tianqi.moji.com/weather/china/guangdong/shenzhen"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 解析HTML，获取所需的信息
    city = soup.find("div", class_="search_default").find("em").text.strip()
    forecast = soup.find("div", class_="wea_alert clearfix").text.strip()
    temperature = soup.find("div", class_="now").find("span", class_="txt").text.strip()
    wind = soup.find("div", class_="now").find_all("span")[1].text.strip()
    
    # 输出结果
    print("城市：", city)
    print("天气预报：", forecast)
    print("温度：", temperature)
    print("风力：", wind)
    ```
    
    这段代码通过requests库向指定URL发送请求，并使用BeautifulSoup库解析HTML，获取深圳当天的天气信息。
    开发者可以根据实际情况修改代码，获取更多信息或实现更复杂的功能。需注意，在进行网络爬虫时，请确保遵守相关法律法规和网站的用户协议。
    """