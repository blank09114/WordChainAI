from state import GameState
from openai_client import OpenAIClient
from validator import Validator

class Game:
    def __init__(self):
        self.state = GameState()
        self.client = OpenAIClient()
        self.validator = Validator(self.client)

    def run(self):
        print("끝말잇기를 시작합니다!")

        # 시작 단어
        self.state.add_word("사과")
        print(f"시작 단어: {self.state.current_word}")

        while not self.state.game_over:
            # 사용자 차례
            user_word = input("당신 > ").strip()

            valid, reason = self.validator.validate(
                previous=self.state.current_word,
                current=user_word,
                state=self.state
            )

            if not valid:
                self.state.add_mistake("USER")

                print(f"사용자가 실수를 했습니다.")
                print(f"단어: {user_word}")
                print(f"사유: {reason}")
                print(f"실수 횟수: {self.state.user_mistakes}/3")

                if self.state.user_mistakes >= 4:
                    self.state.finish("AI")
                    break
                
                continue

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

            valid, reason = self.validator.validate(
                previous=self.state.current_word,
                current=ai_word,
                state=self.state
            )

            if not valid:
                self.state.add_mistake("AI")

                print("AI가 실수를 했습니다.")
                print(f"단어: {ai_word}")
                print(f"사유: {reason}")
                print(f"실수 횟수: {self.state.ai_mistakes}/3")

                if self.state.ai_mistakes >= 4:
                    self.state.finish("USER")
                    break

                continue

            print(f"AI > {ai_word}")

            self.state.add_word(ai_word)

        # 게임 종료
        print()
        print("게임 종료")

        if self.state.winner == "USER":
            print("승리했습니다!")
        elif self.state.winner == "AI":
            print("패배했습니다...")