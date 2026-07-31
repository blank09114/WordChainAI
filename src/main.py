from state import GameState
from openai_client import OpenAIClient

client = OpenAIClient()
state = GameState()

print("끝말잇기를 시작합니다!")

# 시작 단어
state.add_word("사과")
print(f"시작 단어: {state.current_word}")

# 게임 루프
while not state.game_over:
    # 사용자 입력
    user_word = input("당신 > ").strip()
    state.add_word(user_word)

    # AI 호출
    response = client.generate(
        current_word=user_word,
        used_words=state.used_words
    )

    ai_word = response["word"]

    print(f"AI > {ai_word}")

    state.add_word(ai_word)