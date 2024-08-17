import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory # TODO Integration for questions and answers for nodes and travels 
from langchain.schema import SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain.chains import LLMChain

class LLMSolver:
    def __init__(self, system_message):
        # TODO To be configurable if will be used OPEN AI or Claude
        #self.chat = ChatOpenAI(model_name=os.getenv("OPENAI_MODEL_NAME"))
        self.chat = ChatAnthropic(temperature=0, model_name=os.getenv("ANTHROPIC_MODEL_NAME"))
        self.content = system_message
        self.prompt = ChatPromptTemplate(
            input_variables=["content", "messages"],
            messages=[
                SystemMessage(content=self.content),
                MessagesPlaceholder(variable_name="messages"),  
                HumanMessagePromptTemplate.from_template("{content}")  
            ]
        )
        
        self.chain = LLMChain(llm=self.chat, prompt=self.prompt)

    def request(self, user_prompt):
        return self.chain.invoke(user_prompt)['text']