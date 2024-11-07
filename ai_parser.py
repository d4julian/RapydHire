import asyncio
from ollama import AsyncClient
from config import user_profile

class AIJobParser:
    def __init__(self):
        self.client = Client(host = "https://localhost:11434")
        self.model = 'llama3.2:latest'
        self.system_context = self._create_system_context()
        
    def _create_system_context(self) -> dict:
        """Create system context with user profile/resume"""
        return {
            'role': 'system',
            'content': f"""You are an AI assistant helping with job applications.
            Here is the candidate's profile and resume information:
            {user_profile.to_dict()}
            
            Use this information to help answer job application questions.""" }

    def generate(self, message: str, stream: bool):
        return self.client.generate(messages=[self.system_context, { 'role': 'user', 'content': str }], model=self.model, stream=stream)

    def parse_job_description(self, description: str) -> [str]:
        prompt = f"""
        Analyze the following job description and extract key requirements:
        {description}
        """
        print(f"Prompt: {prompt}")
        return self.generate(prompt)

    def answer_question(self, question: str, stream: bool):
        prompt = f"""
        Generate a professional response to this application question: {question}
        Please only give me a response and not the question itself. Do not apply markdown formatting.
        """
        print(f"Prompt: {prompt}")
        return self.generate(prompt, stream=stream)
