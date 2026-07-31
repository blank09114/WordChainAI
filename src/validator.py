from state import GameState
from openai_client import OpenAIClient

class Validator:
    def __init__(self, client: OpenAIClient):
        self.client = client

    # 검증
    def validate(self, previous: str, current: str, state: GameState):
        # 중복 검증
        if self.is_duplicate(current, state):
            return False, "이미 사용한 단어입니다."

        # 규칙 검증
        if not self.is_valid_chain(previous, current):
            return False, "끝말잇기 규칙에 맞지 않습니다."

        # 사유 출력
        result = self.client.validate_word(current)
        if not result["exists"]:
            return False, result["reason"]

        # 한방단어 검증
        if state.allow_one_shot:
            if len(state.used_words) <= 10 and result["one_shot"]:
                return False, "10체인 이하에서는 한방단어를 사용할 수 없습니다."
        else:
            if result["one_shot"]:
                return False, "한방단어는 사용할 수 없습니다."

        return True, ""

    def is_duplicate(self, word: str, state: GameState) -> bool:
        return state.is_used(word)

    def is_valid_chain(self, previous: str, current: str) -> bool:
        if not previous or not current:
            return False

        return current[0] in self.get_allowed_initials(previous[-1])
    
    # 두음 법칙
    def get_allowed_initials(self, last_char: str) -> set[str]:
        mapping = {
            "녀": {"녀", "여"},
            "뇨": {"뇨", "요"},
            "뉴": {"뉴", "유"},
            "니": {"니", "이"},
            "랴": {"랴", "야"},
            "량": {"량", "양"},
            "려": {"려", "여"},
            "력": {"력", "역"},
            "렬": {"렬", "열"},
            "렴": {"렴", "염"},
            "렵": {"렵", "엽"},
            "령": {"령", "영"},
            "례": {"례", "예"},
            "로": {"로", "노"},
            "료": {"료", "요"},
            "뢰": {"뢰", "뇌"},
            "루": {"루", "누"},
            "류": {"류", "유"},
            "률": {"률", "율"},
            "륭": {"륭", "융"},
            "리": {"리", "이"},
        }

        return mapping.get(last_char, {last_char})