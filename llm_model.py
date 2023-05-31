import json
from venus_api_base.http_client import HttpClient
from venus_api_base.config import Config
import config as global_config
import config
import openai
import json


class LLMBaseModel:
    model_name = ""

    def __int__(self):
        pass

    def ask_without_stream(self, request: str, history_msg: list) -> str:
        return ''

    def ask_with_stream(self, request: str, history_msg: list):
        return []


class GPT3(LLMBaseModel):
    '''
    model: gpt-3.5-turbo
    '''

    header = None

    def __init__(self) -> None:
        openai.api_key = config.OPENAI_API_KEY
        self.header = {"Content-Type": "application/json",
                       "Authorization": "Bearer " + config.OPENAI_API_KEY}
        pass

    def get_history_message(self, history_msg) -> list:
        li = []
        for item in history_msg:
            li.append(
                {
                    "role": "user", "content": item['request']
                }
            )
            li.append(
                {
                    "role": "assistant", "content": item['answer']
                }
            )
        return li

    def ask_without_stream(self, request: str, history_msg: list):
        message_list = self.get_history_message(history_msg)
        message_list.append({"role": "user", "content": request})
        print(message_list)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_list, stream=False)
        answer = response.choices[0].message['content']
        return answer

    def ask_with_stream(self, request: str, history_msg: list):
        message_list = self.get_history_message(history_msg)
        message_list.append({"role": "user", "content": request})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_list, stream=True)
        for trunk in response:
            data = ''
            if trunk['choices'][0]['finish_reason'] is not None:
                data = '[DONE]'
            else:
                data = trunk['choices'][0]['delta'].get('content', '')
            yield data


class ChatGLM(LLMBaseModel):
    '''
    model: chat-glm-6b
    '''
    client = HttpClient(config=Config(), secret_id=global_config.VENUS_SECRET_ID,
                        secret_key=global_config.VENUS_SECRET_KEY)
    header = {
        'Content-Type': 'application/json'
    }
    body = {
        'appGroupId': 1,
        'model': 'chat-glm-6b',
        'request': "你是谁?",
        "history": [
            ["你好", "我是腾讯DataMesh产品的技术支持人员，有什么可以帮助您的吗"]
        ],
        "temperature": 0.2,
        "top_p": 1,
        "max_length": 1000
    }
    chat_single_url = 'http://v2.open.venus.oa.com/chat/single'
    list_model_url = "http://v2.open.venus.oa.com/chat/model/list?appGroupId=1"

    def __int__(self):
        pass

    def get_history_msg(self, history_msg) -> list:
        li = []
        for item in history_msg:
            li.append([item['request'], item['answer']])
        return li

    def ask_without_stream(self, request: str, history_msg: list) -> str:
        message_list = self.get_history_msg(history_msg)
        body = self.body
        body['request'] = request
        body['history'] = message_list
        ret = self.client.post(url=self.chat_single_url, header=self.header, body=json.dumps(body))
        answer = ret['data']['response']
        return answer

    def list_all_model(self):
        ret = self.client.get(url=self.list_model_url, header=self.header)
        return ret


model_map = {
    "gpt-3.5": GPT3,
    "chat-glm": ChatGLM
}


def get_llm_model(model_type: str):
    return model_map.get(model_type)()
