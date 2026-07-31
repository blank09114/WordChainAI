import json
from openai import OpenAI
from config import OPENAI_API_KEY, MODEL, TIMEOUT
from prompt import SYSTEM_PROMPT, VALIDATOR_PROMPT

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    # 응답 생성
    def generate(self, current_word: str, used_words: set[str]) -> dict:
        prompt = (
            f"현재 단어: {current_word}\n"
            f"사용한 단어: {', '.join(sorted(used_words))}"
        )

        response = self.client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )

        return json.loads(response.output_text)

    # 응답 검증
    def validate_word(self, word: str) -> dict:
        response = self.client.responses.create(
            model=MODEL,
            instructions=VALIDATOR_PROMPT,
            input=word,
        )

        return json.loads(response.output_text)