from knowledge import knowledge

class Prompt:
    """
    该类是一个prompt工具类, 根据会话问题，和prompt类型生成不同的特点的prompt
    """
    def __init__(self) -> None:
        pass

    def gen(self) -> str:
        return ''


class PromptDataMeshHelperCommon(Prompt):
    context = ""
    question = ""

    def __init__(self, question: str) -> None:
        super().__init__()
        self.question = question
        self.context = knowledge.call_knowledge(question)

    def gen(self) -> str:
        return f'现在你是腾讯PCG大数据平台部datamesh的技术支持人员，' \
               f': {self.context}' \
               f'请根据上面的背景信息回答用户的问题，你可以根据历史消息和下面的问题综合回答用户的咨询问题，问题如下:{self.question}，' \
               f'请注意，这是一些注意事项：你需要根据背景信息和历史对话信息进行回答问题，但是回复中不要涉及背景信息等词汇，' \
                f'回复时你需要以DataMesh的客服机器人的角色认知只需要回答用户的问题；' \
               f'如果你无法根据背景信息回答问题，只回答下面的句子，你的回答应该是：' \
               f'不好意思，目前我还无法回复您的问题，如果需要更多帮助可以参考我们的知识库，' \
               f'知识库链接是https://iwiki.woa.com/pages/viewpage.action?pageId=4007614588，或者企业微信联系DataMeshHelper小助手接入人工服务，请求帮助'


prompts_map = {
    "datamesh_helper": PromptDataMeshHelperCommon
}


def newPromptCMD(request: str, type: str):
    # 后续可以增加根据消息进行意图分类选择不同的模版
    if type not in prompts_map.keys():
        return False, None
    return True, prompts_map.get(type)(request)
