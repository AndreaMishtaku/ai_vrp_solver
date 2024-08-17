import os
from src.module.llm import LLMSolver
from src.utils.file import read_file

class LLMService:
    def solve(user_prompt):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, "assets", "system_message.txt")

        system_message=read_file(file_path=file_path)
        chat_bot = LLMSolver(system_message=system_message)  
        
        test=chat_bot.request(user_prompt=user_prompt)

        return test