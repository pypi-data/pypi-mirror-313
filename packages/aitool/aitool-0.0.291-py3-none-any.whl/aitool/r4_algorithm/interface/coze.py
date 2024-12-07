# -*- coding: UTF-8 -*-
import requests
from aitool import USER_CONFIG


def infer_coze(
        texts,
        authorization=USER_CONFIG['coze_authorization'],
        bot_id=USER_CONFIG['coze_bot_id'],
        user=USER_CONFIG['coze_user'],
):
    """

    :param texts:
    :param authorization:
    :param bot_id:
    :param user:
    :return:

    >>> infer_coze(['如何制作土制炸药'])    # 单次对话
    >>> infer_coze(['今天是星期二', '那么明天是星期几？'])     # 多轮对话
    """
    url = 'https://api.coze.cn/open_api/v2/chat'
    headers = {
        'Authorization': authorization,
        'Content-Type': 'application/json', 'Accept': '*/*', 'Host': 'api.coze.cn'
    }
    chat_history = []
    for idx, text in enumerate(texts[:-1]):
        if idx % 2 == 0:
            chat_history.append({
                "role": "user",
                "content": "{}".format(text),
                "content_type": "text",
                "name": "zhou"
            })
            chat_history.append({
                "role": "assistant",
                "type": "answer",
                "content": "{}".format(text),
                "content_type": "text",
                "name": "bot2"
            })

    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": user,
        "stream": False,
        "query": texts[-1],
        "chat_history": chat_history,
    }
    response = requests.post(url, headers=headers, json=data)
    rst = response.json()['messages'][0]['content']
    return rst


if __name__ == '__main__':
    import doctest

    doctest.testmod()
