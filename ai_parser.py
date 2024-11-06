import asyncio
from ollama import Chat
from config import load_user_profile

class AIJobParser:
    def __init__(self):
        self.client = AsyncClient(host = "https://localhost:11434")
        self.model = 'llama3.2:latest'

    async def generate(self, message: str) -> str:
        message = {'role': 'user', 'content': str}
        return await self.client.generate(messages=[message], model=self.model)

    async def parse_job_description(self, description: str) -> [str]:
        prompt = f"""
        Analyze the following job description and extract key requirements:
        {description}
        """
        return await self.generate(prompt)

    async def answer_question(self, user_profile: UserProfile, question: str) -> str:
        prompt = f"""
        Given this user profile: {user_profile}
        Generate a professional response to this application question: {question}
        Please only give me a response and not the question itself. Do not apply markdown formatting.
        """
        return await self.generate(prompt)
    