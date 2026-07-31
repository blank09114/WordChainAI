from state import GameState
from openai_client import OpenAIClient
from validator import Validator

class Game:
    def __init__(self):
        self.state = GameState()
        self.client = OpenAIClient()
        self.validator = Validator(self.client)

    # 실행
    def run(self):

        self.start()

        while not self.state.game_over:

            self.user_turn()

            if self.state.game_over:
                break

            self.ai_turn()

        self.end()

    # 게임 시작
    def start(self):
        print("끝말잇기를 시작합니다!")

        self.state.add_word("사과")

        print(f"시작 단어: {self.state.current_word}")

    # 게임 종료
    def end(self):
        print()
        print("게임 종료")

        if self.state.winner == "USER":
            print("승리!")

        elif self.state.winner == "AI":
            print("패배...")

    # 사용자 입력
    def user_turn(self):
        while not self.state.game_over:
            user_word = input("당신 > ").strip()

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

    # 단어 검증
    def process_word(self, player: str, word: str) -> bool:
        valid, reason = self.validator.validate(
            previous=self.state.current_word,
            current=word,
            state=self.state
        )

        if valid:
            self.state.add_word(word)
            return True

        game_over = self.handle_mistake(player, word, reason)

        if game_over:
            return True

        return False

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

        print(f"{name}가 실수를 했습니다.")
        print(f"단어: {word}")
        print(f"사유: {reason}")
        print(f"실수 횟수: {mistakes}/3")

        if mistakes >= 4:
            self.state.finish(winner)
            return True

        return False