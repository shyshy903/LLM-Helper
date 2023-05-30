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
               f'请根据背景信息回答问题：背景信息如下: {self.context}' \
               f'请根据上面的背景信息回答用户的问题，你可以根据历史消息和下面的问题综合回答问题，问题如下:{self.question}，' \
               f'请注意，回答的过程应尽量避免使用背景信息、用户、回答等词汇；' \
               f'如果你无法根据背景信息回答问题，请按照下面的话术进行回复：' \
               f'不好意思，目前我还无法回复您的问题，如果需要更多帮助可以参考我们的知识库，' \
               f'知识库链接是https://iwiki.woa.com/pages/viewpage.action?pageId=4007614588，或者点击人工，请求帮助'


prompts_map = {
    "datamesh_helper": PromptDataMeshHelperCommon
}


def newPromptCMD(request: str, type: str):
    # 后续可以增加根据消息进行意图分类选择不同的模版
    if type not in prompts_map.keys():
        return False, None
    return True, prompts_map.get(type)(request)
