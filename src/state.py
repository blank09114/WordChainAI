from dataclasses import dataclass, field


@dataclass
class GameState:
    current_word: str = "" # 현재 제시어
    user_mistakes: int = 0 # 사용자 실수 횟수
    ai_mistakes: int = 0 # AI 실수 횟수
    allow_one_shot: bool = False # 한방단어 허용 여부
    used_words: set[str] = field(default_factory=set) # 사용된 단어 목록
    game_over: bool = False # 게임 종료 여부
    winner: str | None = None # 승자

    # 새로운 단어 제시
    def add_word(self, word: str) -> None:
        self.current_word = word
        self.used_words.add(word)

    # 실수 처리
    def add_mistake(self, player: str) -> None:
        if player == "USER":
            self.user_mistakes += 1
        elif player == "AI":
            self.ai_mistakes += 1
        else:
            raise ValueError(f"알 수 없는 플레이어: {player}")

    # 게임 종료 플래그
    def finish(self, winner: str) -> None:
        self.game_over = True
        self.winner = winner

    # 사용한 단어 체크
    def is_used(self, word: str) -> bool:
        return word in self.used_words

    # 초기화
    def reset(self) -> None:
        self.current_word = ""
        self.user_mistakes = 0
        self.ai_mistakes = 0
        self.used_words.clear()
        self.game_over = False
        self.winner = None