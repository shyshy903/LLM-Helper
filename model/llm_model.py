from model.chat_glm import ChatGLM
from model.gpt import GPT3


class LLMBaseModel:

    def __int__(self):
        pass

    def ask_without_stream(self, request: str, history_msg: list) -> str:
        return ''

    def ask_with_stream(self, request: str, history_msg: list):
        return []


model_map = {
    "gpt-3.5": GPT3,
    "chat-glm": ChatGLM
}


def get_llm_model(model_type: str):
    return model_map.get(model_type)
