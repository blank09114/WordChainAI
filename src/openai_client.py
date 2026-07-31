import json

from openai import OpenAI

from config import OPENAI_API_KEY, MODEL
from prompt import SYSTEM_PROMPT, VALIDATOR_PROMPT


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    # 게임 AI
    def generate(self, current_word: str, used_words: set[str]) -> dict:
        prompt = (
            f"현재 단어: {current_word}\n"
            f"사용한 단어: {', '.join(sorted(used_words))}"
        )

        return self._request(
            instructions=SYSTEM_PROMPT,
            input_text=prompt,
            required_keys={"success", "word"}
        )

    # 검증 AI
    def validate_word(self, word: str) -> dict:
        return self._request(
            instructions=VALIDATOR_PROMPT,
            input_text=word,
            required_keys={"exists", "one_shot", "reason"}
        )

    # 응답 형식 예외 처리
    def _request(
        self,
        instructions: str,
        input_text: str,
        required_keys: set[str]
    ) -> dict:

        response = self.client.responses.create(
            model=MODEL,
            instructions=instructions,
            input=input_text
        )

        try:
            result = json.loads(response.output_text)

        except json.JSONDecodeError:
            return {
                "success": False,
                "reason": "AI가 올바른 JSON을 반환하지 않았습니다."
            }

        if not isinstance(result, dict):
            return {
                "success": False,
                "reason": "JSON 객체가 아닙니다."
            }

        if not required_keys.issubset(result.keys()):
            return {
                "success": False,
                "reason": "JSON 형식이 올바르지 않습니다."
            }

        return result