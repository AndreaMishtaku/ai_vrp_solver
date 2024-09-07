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

anthopic_model = ChatAnthropic(model_name = os.getenv("ANTHROPIC_MODEL_NAME"))
open_ai_model = ChatOpenAI(model_name= os.getenv("OPENAI_MODEL_NAME"))

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
    def __init__(self):
        model='openai'
        self.model =  open_ai_model if model=="openai" else anthopic_model if model=="claude" else None
        self.model_name = os.getenv("OPENAI_MODEL_NAME") if model=="openai" else anthopic_model if model=="claude" else None
        self.parser= JsonOutputParser(pydantic_object=VRPResponse)
        self.prompt = PromptTemplate(
            system_message=system_message,
            input_variables=['locations', 'distances', 'vehicle_depo', "schema"],
            template=prompt_template
        )
        
        self.chain = self.prompt | self.model | self.parser

    def solve(self, inputs):
        if self.model is None:
            raise Error(message='Model not specified')
        return self.chain.invoke(inputs)
