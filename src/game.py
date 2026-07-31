from state import GameState
from openai_client import OpenAIClient


class Game:
    def __init__(self):
        self.state = GameState()
        self.client = OpenAIClient()

    def run(self):
        print("끝말잇기를 시작합니다!")

        # 시작 단어
        self.state.add_word("사과")
        print(f"시작 단어: {self.state.current_word}")

        while not self.state.game_over:
            # 사용자 차례
            user_word = input("당신 > ").strip()
            self.state.add_word(user_word)

            # AI 차례
            response = self.client.generate(
                current_word=self.state.current_word,
                used_words=self.state.used_words
            )

            if not response["success"]:
                print("AI가 더 이상 단어를 찾지 못했습니다.")
                self.state.finish("USER")
                break

            ai_word = response["word"]

            print(f"AI > {ai_word}")

            self.state.add_word(ai_word)

        # 게임 종료
        print()
        print("게임 종료")

        if self.state.winner == "USER":
            print("승리했습니다!")
        elif self.state.winner == "AI":
            print("패배했습니다...")