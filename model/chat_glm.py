import json
from venus_api_base.http_client import HttpClient
from venus_api_base.config import Config
import config as global_config
from llm_model import LLMBaseModel


class ChatGLM(LLMBaseModel):
    '''
    model: chat-glm-6b
    '''
    client = HttpClient(config=Config(), secret_id=global_config.VENUS_SECRET_ID, secret_key=global_config.VENUS_SECRET_KEY)
    header = {
        'Content-Type': 'application/json'
    }
    body = {
        'appGroupId': 1,
        'model': 'chat-glm-6b',
        'request': "你是谁?",
        "history" : [
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

    def ask(self, chat_id: str, prompt: str) :
        history = self.__get_message_list(chat_id)
        body = self.body
        body['request'] = prompt
        body['history'] = history
        ret = self.client.post(url=self.chat_single_url, header=self.header, body=json.dumps(body))
        answer = ret['data']['response']
        return answer

    def __get_message_list(self, chat_id: str) -> list:
        li = []
        return li

    def list_all_model(self):
        ret = self.client.get(url=self.list_model_url, header=self.header)
        return ret
