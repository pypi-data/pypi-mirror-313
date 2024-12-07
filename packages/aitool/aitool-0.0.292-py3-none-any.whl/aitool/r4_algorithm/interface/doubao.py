# -*- coding: UTF-8 -*-
"""

"""
from aitool import singleton, pip_install, USER_CONFIG


@singleton
class Client:
    def __init__(self, base_url, api_key):
        try:
            from volcenginesdkarkruntime import Ark
        except ModuleNotFoundError:
            pip_install('volcenginesdkarkruntime')
            from volcenginesdkarkruntime import Ark

        self.client = Ark(
            base_url=base_url,
            api_key=api_key,
        )


def infer_doubao(
        texts,
        base_url=USER_CONFIG['doubao_base_url'],
        api_key=USER_CONFIG['doubao_api_key'],
        model=USER_CONFIG['doubao_model'],
):
    """

    :param texts:
    :return:

    >>> infer_doubao(['今天是星期二'])    # 单次对话
    >>> infer_doubao(['今天是星期二', '那么明天是星期几？'])   # 多轮对话
    """
    client = Client(base_url, api_key)
    completion = client.client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "{}".format(texts[0])},
        ],
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    import doctest

    doctest.testmod()
