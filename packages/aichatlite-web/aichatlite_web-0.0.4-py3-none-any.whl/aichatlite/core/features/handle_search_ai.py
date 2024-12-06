from ..base import OmniCore
from visionlite import vision

def handle_search_ai(chatbot:OmniCore, query:str,k=1):
    context = vision(query,k=1,max_urls=5) # google search using chromedriver
    prompt = """
    <context>
    ### Search results:
    {context}
    </context>
    user query: 
    
    {query}
    """.format(context=context, query=query)
    return chatbot.generator(prompt)

