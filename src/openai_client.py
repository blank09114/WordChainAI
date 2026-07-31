from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, TIMEOUT

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=MODEL,
            input=prompt,
        )

        return response.output_text