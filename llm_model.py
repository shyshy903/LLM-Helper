import asyncio
import json
from venus_api_base.http_client import HttpClient
from venus_api_base.config import Config
import config as global_config
import config
import openai
import json
import sseclient
import requests
import time
import main


class LLMBaseModel:
    model_name = ""

    def __int__(self):
        pass

    def ask_without_stream(self, request: str, history_msg: list, session_id: str) -> str:
        return ''

    def ask_with_stream(self, request: str, history_msg: list, session_id: str):
        return None, ''



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

    def ask_without_stream(self, request: str, history_msg: list, session_id: str):
        message_list = self.get_history_message(history_msg)
        message_list.append({"role": "user", "content": request})
        print(message_list)
        print(openai.api_key)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_list, stream=False)
        answer = response.choices[0].message['content']
        return answer

    def ask_with_stream(self, request: str, history_msg: list, session_id: str):
        # message_list = self.get_history_message(history_msg)
        # message_list = history_msg
        message_list = [i for i in history_msg[:-1]]
        message_list.append({"role": "user", "content": request})
        print(message_list)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_list, stream=True)
        # print(response)
        answer = ''
        def generate():
            stream_content = str()
            one_message = {"role": "assistant", "content": stream_content}
            history_msg.append(one_message)
            for trunk in response:
                if trunk['choices'][0]['finish_reason'] is not None:
                    asyncio.run(main.save_all_user_dict())
                    data = ''
                else:
                    data = trunk['choices'][0]['delta'].get('content', '')
                    # print(data)
                one_message['content'] = one_message['content'] + data
                yield data
        print('aws', answer)
        return generate


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

    def ask_without_stream(self, request: str, history_msg: list, session_id: str) -> str:
        # message_list = self.get_history_msg(history_msg)
        body = self.body
        body['request'] = request
        body['history'] = []
        print(body)
        ret = self.client.post(url=self.chat_single_url, header=self.header, body=json.dumps(body))
        answer = ret['data']['response']
        return answer

    def ask_with_stream(self, request: str, history_msg: list, session_id: str):
        body = {
            'sessionId': session_id, 'request': 'hello',
        }

        url = 'http://v2.open.venus.oa.com'
        path = '/chat/sse'
        timestamp = str(int(time.time()))
        sign = self.client.gen_venus_sign_with_timestamp(path, '', json.dumps(body), timestamp)
        headers = {
            'Content-Type': 'application/json',
            'Venusopenapi-Request-Timestamp': timestamp,
            'Venusopenapi-Authorization': sign,
            "Venusopenapi-Secret-Id": global_config.VENUS_SECRET_ID
        }

        # 发送请求, 注意需要设置 stream 为 True, 表示流式接收返回数据
        response = requests.post(url + path, stream=True, headers=headers, data=json.dumps(body))
        client = sseclient.SSEClient(response)
        def generate():
            stream_content = str()
            one_message = {"role": "assistant", "content": stream_content}
            history_msg.append(one_message)
            for event in client.events():
                print(event)
                if event.event == '[DONE]':
                    asyncio.run(main.save_all_user_dict())
                if event.event == '[DATA]':
                    data = event.data["data"]
                    one_message['content'] = one_message['content'] + data
                    yield data
        return generate

    def list_all_model(self):
        ret = self.client.get(url=self.list_model_url, header=self.header)
        return ret


model_map = {
    "gpt": GPT3,
    "chatglm": ChatGLM
}


def get_llm_model(model_type: str):
    return model_map.get(model_type)()


if __name__ == "__main__":
    chat_glm = ChatGLM()
    print(chat_glm.ask_without_stream("你是谁",[],"123"))