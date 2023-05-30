import model.llm_model as llm


class ChatAgency:
    """
    该类是一个chatAgency工具类, 属于会话层的基本结构，用于对模型进行提问和获取回答
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
        [{"user": "你是谁", "helper": "我是datamesh产品的helper"}]
        """



    def ask_without_stream(self):
        llm_model = llm.get_llm_model(self.model)
        history_msg = self.load_history_msg();
        answer = llm_model.ask(history_msg, self.request)





