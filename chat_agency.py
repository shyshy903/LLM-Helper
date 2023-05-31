import llm_model as llm
from dao import chat_record

class ChatAgency:
    """
    该类是一个chatAgency工具类, 属于会话层与模型交流的中间层（属于一个通用的结构层插件）
    包含属性 user_id (用户) , session_id （会话）, 事件（span_id), request (请求), model (模型), answer (回答),
    """
    user_id = "123"
    session_id = "abc123"
    span_id = "def123",
    request = "1+1等于几"
    model = "chat-glm-6b",
    answer = "2"

    def __int__(self, user_id, session_id, span_id, request, model, answer):
        self.user_id = user_id
        self.session_id = session_id
        self.span_id = span_id
        self.request = request
        self.model = model
        self.answer = answer

    def load_history_msg(self) -> list:
        """
        加载历史消息, 格式为
        [{"request": "你是谁", "answer": "我是datamesh产品的helper"}]
        """
        message_list = []
        session_info = chat_record.get_session_info(self.user_id, self.session_id)
        for span_id, value_dict in session_info.items():
            span_dict = {'request': value_dict['request'], 'answer': value_dict['answer']}
            message_list.append(span_dict)
        return message_list

    def save_history_msg(self):
        """
        保存消息到消息文件中
        """
        chat_record.insert(self.user_id, self.session_id, self.span_id, self.request, self.answer)

    def ask_without_stream(self) -> str:
        """
        无流式的返回消息
        """
        # 获取llm模型
        llm_model = llm.get_llm_model(self.model)
        # 加载历史消息
        history_msg = self.load_history_msg()
        print(history_msg)
        # 提问模型
        answer = llm_model.ask_without_stream(request=self.request, history_msg=history_msg)
        self.answer = answer
        # 保存消息
        self.save_history_msg()
        return answer

    def ask_with_stream(self):
        """
        流式的返回消息
        """
        # 获取llm模型
        llm_model = llm.get_llm_model(self.model)
        # 加载历史消息
        history_msg = self.load_history_msg()
        # 提问模型
        answer = llm_model.ask_with_stream(request=self.request, history_msg=history_msg)

        # 构建一个生成器
        def generate():
            for token in answer:
                yield token
        return generate


if __name__ == "__main__":
    # chat_agency = ChatAgency("123", "123", "001", "你是谁", "gpt", "我是datamesh")
    chat_agency = ChatAgency()
    chat_agency.user_id = "123"
    chat_agency.session_id = "123"
    chat_agency.request = "你是谁"
    chat_agency.answer = "我是helper"
    chat_agency.span_id = "001"
    chat_agency.save_history_msg()
    print(chat_agency.load_history_msg())
    chat_agency.model = "gpt-3.5"
    print(chat_agency.ask_without_stream())