from .handle_google_searchai import *


from .handle_search_ai import handle_search_ai

class FeatureHandlerMain:
    def __init__(self, chatbot, agent_type, query, web_search):
        self.chatbot = chatbot
        self.agent_type = agent_type
        self.query = query
        self.web_search = web_search

    def generate(self):
        match self.agent_type:
            case "QuestionAnswer":
                return self.chatbot.generator(self.query)
            case "SearchAI":
                return handle_search_ai(chatbot=self.chatbot, query=self.query)
            case _:
                return "None"
