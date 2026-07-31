class Validator:

    def __init__(self, client):
        self.client = client

    def validate(self, previous: str, current: str, state) -> tuple[bool, str]:

        current = current.strip()

        # 빈 문자열
        if not current:
            return False, "단어를 입력해주세요."

        # 첫 턴이 아닌 경우 끝말잇기 규칙 검사
        if previous and not self.is_valid_chain(previous, current):
            return False, "끝말잇기 규칙에 맞지 않습니다."

        # 중복 단어
        if self.is_duplicate(current, state):
            return False, "이미 사용한 단어입니다."

        # AI 검증
        result = self.client.validate_word(current)

        if not result.get("success", True):
            return False, result["reason"]

        # 표준국어대사전 등재 여부
        if not result["exists"]:
            return False, "표준국어대사전의 일반 명사가 아님"

        # 한방단어 검사
        if result["one_shot"]:
            if state.allow_one_shot:
                # 11번째 단어부터 허용
                if len(state.used_words) <= 10:
                    return False, "10체인 이하에서는 한방단어를 사용할 수 없습니다."
            else:
                return False, "한방단어는 사용할 수 없습니다."

        return True, ""

    def is_valid_chain(self, previous: str, current: str) -> bool:
        return current[0] in self.get_allowed_initials(previous[-1])

    def is_duplicate(self, word: str, state) -> bool:
        return state.is_used(word)

    # 두음 법칙
    def get_allowed_initials(self, last_char: str) -> set[str]:
        mapping = {
            "라": {"라", "나"},
            "락": {"락", "낙"},
            "란": {"란", "난"},
            "랄": {"랄", "날"},
            "람": {"람", "남"},
            "랍": {"랍", "납"},
            "랑": {"랑", "낭"},
            "래": {"래", "내"},
            "랭": {"랭", "냉"},
            "략": {"략", "약"},
            "량": {"량", "양"},
            "려": {"려", "여"},
            "력": {"력", "역"},
            "련": {"련", "연"},
            "렬": {"렬", "열"},
            "렴": {"렴", "염"},
            "렵": {"렵", "엽"},
            "령": {"령", "영"},
            "례": {"례", "예"},
            "로": {"로", "노"},
            "록": {"록", "녹"},
            "론": {"론", "논"},
            "롱": {"롱", "농"},
            "뢰": {"뢰", "뇌"},
            "료": {"료", "요"},
            "루": {"루", "누"},
            "류": {"류", "유"},
            "륙": {"륙", "육"},
            "륜": {"륜", "윤"},
            "률": {"률", "율"},
            "륭": {"륭", "융"},
            "르": {"르", "느"},
            "린": {"린", "인"},
            "림": {"림", "임"},
            "립": {"립", "입"},
        }

        return mapping.get(last_char, {last_char})