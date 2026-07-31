import json
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, TIMEOUT
from prompt import SYSTEM_PROMPT

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate(self, current_word: str, used_words: set[str]) -> dict:
        prompt = f"""
            현재 단어: {current_word}
            사용한 단어: {", ".join(used_words)}
        """

        response = self.client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )

        return json.loads(response.output_text)