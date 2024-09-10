import os
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate,  HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from .system_message import system_message
from .prompt import prompt_template
from src.payload import Error
from src.enums.llm_model_name import LLM_ModelName

class Route(BaseModel):
    plate: Optional[str] = Field(description="Plate of the vehicle")
    route: Optional[List[int]] = Field(description="Array with id of nodes visited in order")
    load: Optional[int] = Field(description="Total load transported by the vehicle")
    distance: Optional[int] = Field(description="Distance covered by the vehicle through the route")

class VRPResponse(BaseModel):
    routes: List[Route] = Field(description="List of routes for each vehicle")
    total_distance: Optional[int] = Field(description="Total distance covered by all routes")
    total_load: Optional[int] = Field(description="Total load transported by all routes")

class LLMSolver:
    def __init__(self, model):
        self.model = self.get_model(model)
        self.parser= JsonOutputParser(pydantic_object=VRPResponse)
        self.prompt = self.get_prompt(system_message,prompt_template)
        self.chain = self.get_prompt(system_message,prompt_template) | self.model | self.parser
        
    def get_model(self, model):
        if model == LLM_ModelName.GPT4:
            return  ChatOpenAI(model_name = "gpt-4o",temperature=0)
        elif model == LLM_ModelName.GPT3:
            return  ChatOpenAI(model_name = "gpt-3.5-turbo",temperature=0)
        elif model == LLM_ModelName.Claude3:
            return  ChatAnthropic(model_name = "claude-3-sonnet-20240229")
        elif model == LLM_ModelName.Claude3_5:
            return ChatAnthropic(model_name = "claude-3-5-sonnet-20240620")
        else:
            return None

    def get_prompt(self, s_template, p_template):
        system_message_prompt= SystemMessagePromptTemplate.from_template(s_template)

        human_message_prompt = HumanMessagePromptTemplate.from_template(p_template)

        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        return chat_prompt

    
    
    def solve(self, inputs):
        if self.model is None:
            raise Error(message='Model not specified')
        return self.chain.invoke(inputs)
