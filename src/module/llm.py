import os
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from .system_message import system_message
from .prompt import prompt_template


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
        # TODO To be configurable if will be used OPEN AI or Claude
        # self.chat = ChatAnthropic(temperature=0, model_name=os.getenv("ANTHROPIC_MODEL_NAME"))
        self.model =ChatOpenAI(model_name=os.getenv("OPENAI_MODEL_NAME"))
        self.parser=JsonOutputParser(pydantic_object=VRPResponse)
        self.prompt = PromptTemplate(
            system_message=system_message,
            input_variables=[ "nodes", "depos", "edges", "vehicles", "demands", "schema"],
            template=prompt_template
        )
        
        self.chain = self.prompt | self.model | self.parser

    def solve(self, inputs):
        return self.chain.invoke(inputs)
