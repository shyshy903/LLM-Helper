import model.llm_model as llm


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
        [{"user": "你是谁", "helper": "我是datamesh产品的helper"}]
        """

    def save_history_msg(self):
        """
        保存消息到消息文件中
        """

    def ask_without_stream(self) -> str:
        """
        无流式的返回消息
        """
        # 获取llm模型
        llm_model = llm.get_llm_model(self.model)
        # 加载历史消息
        history_msg = self.load_history_msg()
        # 提问模型
        answer = llm_model.ask_without_stream(history_msg, self.request)
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
        answer = llm_model.ask_with_stream(history_msg, self.request)

        # 构建一个生成器
        def generate():
            for token in answer:
                yield token

        return generate
