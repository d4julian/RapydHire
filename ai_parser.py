from typing import Dict, Any
from langchain.llms import Ollama

class AIJobParser:
    def __init__(self):
        self.llm = Ollama(model="llama3.2:latest")

    async def parse_job_description(self, description: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following job description and extract key requirements:
        {description}
        """
        response = await self.llm.acall(prompt)
        # TODO: Parse AI response into structured data
        return {}

    async def generate_application_responses(self, question: str, user_profile: Dict[str, Any]) -> str:
        prompt = f"""
        Given this user profile: {user_profile}
        Generate a professional response to this application question: {question}
        """
        response = await self.llm.acall(prompt)
        return response
