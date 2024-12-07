import openai
class OpenAIClient():
    def __init__(self, api_key):
        self.openai = openai
        self.openai.api_type = "azure"
        self.openai.api_base = "https://search.bytedance.net/gpt/openapi/online/v2/crawl"
        self.openai.api_version = "2023-03-15-preview"
        self.openai.api_key = api_key
    def summary(self, prompt, contents):
        inputs = prompt + '\n' + contents
        messages = [
            {
                'role': 'user', 'content': inputs[:1024]
            }
        ]
        response = self.openai.ChatCompletion.create(
            engine='gpt-35-turbo',
            messages=messages,
        )
        return response['choices'][0]['message']['content']
    def embedding(self, contents):
        response = self.openai.Embedding.create(
            engine="text-embedding-ada-002", # 固定为text-embedding-ada-002
            input=contents,
        )
        response = response['data'][0]['embedding']
        return response


x = OpenAIClient('iZeMPYmFdnt4c3TOxms9ncXZIn3hFfaQ')
print(x.summary('你好', '请问你是？'))
from aitool import make_dir