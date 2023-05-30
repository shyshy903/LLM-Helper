import logging
import config
from datetime import datetime, timedelta
import openai
import json
import requests
from llm_model import LLMBaseModel


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

    def __get_message_list(self, chat_id: str) -> list:
        '''
        [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
        ]
        '''
        li = []
        from_time = datetime.now().__add__(timedelta(hours=-1))
        for doc in self.col.find(
                {"chat_id": chat_id, "ask_mode": "chatgpt", "status": 2, "created_at": {"$gte": from_time}},
                {"prompt": 1, "answer": 1}):
            if doc.get("prompt"):
                li.append({"role": "user", "content": doc.get("prompt")})
            if doc.get("answer"):
                li.append({"role": "assistant", "content": doc.get("answer")})
        return li

    def ask(self, chat_id: str, prompt: str) -> dict:
        message_list = self.__get_message_list(chat_id)
        message_list.append({"role": "user", "content": prompt})
        logging.info(f"gpt3.ask chat_id={chat_id}, message_list={message_list}")
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_list, stream=False)
        answer = response.choices[0].message['content']
        return answer

    def get_response_stream_generate_from_ChatGPT_API(self, chat_id: str, prompt: str):
        message_list = self.__get_message_list(chat_id)
        message_list.append({"role": "user", "content": prompt})
        data = {
            "model": "gpt-3.5-turbo",
            "messages": message_list,
            "stream": True
        }
        url = "https://api.openai.com/v1/chat/completions"
        try:
            response = requests.request("POST", url, headers=self.header, json=data, stream=True)

            def generate():
                stream_content = str()
                one_message = {"role": "assistant", "content": stream_content}
                i = 0
                for line in response.iter_lines():
                    # print(str(line))
                    line_str = str(line, encoding='utf-8')
                    if line_str.startswith("data:"):
                        line_json = json.loads(line_str[5:])
                        if 'choices' in line_json:
                            if len(line_json['choices']) > 0:
                                choice = line_json['choices'][0]
                                if 'delta' in choice:
                                    delta = choice['delta']
                                    if 'role' in delta:
                                        role = delta['role']
                                    elif 'content' in delta:
                                        delta_content = delta['content']
                                        i += 1
                                        if i < 40:
                                            print(delta_content, end="")
                                        elif i == 40:
                                            print("......")
                                        one_message['content'] = one_message['content'] + delta_content
                                        yield delta_content

                    elif len(line_str.strip()) > 0:
                        print(line_str)
                        yield line_str
        except Exception as e:
            ee = e

            def generate():
                yield "request error:\n" + str(ee)
        return generate
