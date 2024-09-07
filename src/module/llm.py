import os
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
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
        self.prompt = PromptTemplate(
            system_message=system_message,
            input_variables=['locations', 'distances', 'vehicle_depo', "schema"],
            template=prompt_template
        )
        
        self.chain = self.prompt | self.model | self.parser
        
    def get_model(self, model):
        if model == LLM_ModelName.GPT4:
            return  ChatOpenAI(model_name = "gpt-4o")
        elif model == LLM_ModelName.GPT3:
            return  ChatOpenAI(model_name = "gpt-3.5-turbo")
        elif model == LLM_ModelName.Claude3:
            return  ChatAnthropic(model_name = "claude-3-sonnet-20240229")
        elif model == LLM_ModelName.Claude3_5:
            return ChatAnthropic(model_name = "claude-3-5-sonnet-20240620")
        else:
            return None
    
    def solve(self, inputs):
        if self.model is None:
            raise Error(message='Model not specified')
        return self.chain.invoke(inputs)
