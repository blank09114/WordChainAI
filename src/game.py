from state import GameState
from openai_client import OpenAIClient
from validator import Validator
from util import timed_input

class Game:
    def __init__(self):
        self.state = GameState()
        self.client = OpenAIClient()
        self.validator = Validator(self.client)

    # 실행
    def run(self):
        self.show_intro()

        self.setup()

        while not self.state.game_over:
            self.show_status(True)

            self.user_turn()

            if self.state.game_over:
                break

            self.show_status(False)

            self.ai_turn()
        self.show_result()

    # 시작 화면
    def show_intro(self):
        print("=========================")
        print("      WordChain AI")
        print("=========================")
        print()

        print("규칙")
        print("- 표준국어대사전 일반 명사만 사용")
        print("- 두음법칙 허용")
        print("- 실수 3회 허용(4회째 패배)")
        print()

    # 게임 설정
    def setup(self):

        print("한방단어 허용?")
        print("1. 허용")
        print("2. 비허용")
        print()
        print("* 허용 시 11번째 단어부터 사용 가능합니다.")
        print()

        while True:

            choice = input("> ").strip()

            if choice == "1":
                self.state.allow_one_shot = True
                break

            if choice == "2":
                self.state.allow_one_shot = False
                break

            print("1 또는 2를 입력해주세요.")

    # 현재 상태 출력
    def show_status(self, user_turn: bool):
        print()

        print("=========================")
        print(f"체인: {len(self.state.used_words)}")
        print()

        if self.state.current_word:
            print(f"현재 단어: {self.state.current_word}")
        else:
            print("현재 단어: 없음")

        print()

        if user_turn:
            print("10초 이내에 단어를 입력해주세요.")
        else:
            print("AI가 생각 중...")

        print()
        print("=========================")

    # 종료 화면
    def show_result(self):
        print()
        print("=========================")
        print()
        print("게임 종료")
        print()
        print(f"승자: {self.state.winner}")
        print(f"총 체인: {len(self.state.used_words)}")
        print()
        print("=========================")

    # 사용자 입력
    def user_turn(self):
        while not self.state.game_over:
            user_word = timed_input("당신 > ", 10)

            # 타임아웃
            if user_word is None:
                if self.handle_mistake(
                    "USER",
                    "(시간 초과)",
                    "10초 안에 입력하지 않았습니다."
                ):
                    return
                continue

            # 단어 검증
            if self.process_word("USER", user_word):
                return

    # AI 입력
    def ai_turn(self):
        while not self.state.game_over:
            response = self.client.generate(
                current_word=self.state.current_word,
                used_words=self.state.used_words
            )

            if not response["success"]:
                print("AI가 더 이상 단어를 찾지 못했습니다.")
                self.state.finish("USER")
                return

            ai_word = response["word"]

            if self.process_word("AI", ai_word):
                print(f"AI > {ai_word}")
                return

    # 단어 처리
    def process_word(self, player: str, word: str) -> bool:
        valid, reason = self.validator.validate(
            previous=self.state.current_word,
            current=word,
            state=self.state
        )

        if valid:
            self.state.add_word(word)
            return True

        return self.handle_mistake(player, word, reason)

    # 실수 처리
    def handle_mistake(self, player: str, word: str, reason: str) -> bool:
        self.state.add_mistake(player)

        if player == "USER":
            mistakes = self.state.user_mistakes
            winner = "AI"
            name = "사용자"
        else:
            mistakes = self.state.ai_mistakes
            winner = "USER"
            name = "AI"

        print()
        print("-------------------------")
        print()

        print(f"{name}가 실수를 했습니다.")
        print()
        print(f"단어: {word}")
        print(f"사유: {reason}")
        print(f"실수: {mistakes}/3")

        print()
        print("-------------------------")

        if mistakes >= 4:
            self.state.finish(winner)
            return True

        return False