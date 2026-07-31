# 기획

## 프로젝트 개요

WordChainAI는 OpenAI Responses API 기반 끝말잇기 게임입니다.

본 프로젝트는 OpenAI API 활용, Prompt Engineering, JSON 기반 응답 처리 및 LLM 출력 검증을 학습하는 것을 목표로 개발합니다.

---
## 게임 규칙

* 표준국어대사전에 등재된 단어만 사용할 수 있습니다.
* 이미 사용한 단어는 다시 사용할 수 없습니다.
* 게임 시작 시 한방단어 허용 여부를 선택할 수 있습니다. 해당 옵션은 사용자와 AI 모두에 동일하게 적용됩니다.
    * 한방단어 허용 시, 10체인 이후부터 사용자와 AI 모두 한방단어를 사용할 수 있습니다.
* 사용자와 AI 모두 10초 이내에 응답해야 합니다. AI의 경우 OpenAI API 요청을 전송한 시점부터 응답을 수신할 때까지의 시간을 기준으로 판정합니다.
* 사용자가 규칙에 맞지 않는 단어를 입력하면 실수 횟수가 1회 증가합니다. 실수는 최대 3회까지 허용됩니다.
* AI의 응답이 JSON 형식을 따르지 않거나 게임 규칙 검증에 실패하면 실수 횟수가 1회 증가합니다. 실수는 최대 3회까지 허용됩니다.

---
# 시스템 설계

## 기술 스택

| 기술 | 용도 |
| --- | --- |
| Python 3 | 게임 로직 구현 |
| python-dotenv | 환경 변수 관리 |
| OpenAI Responses API | AI 응답 생성 |
| Git/GitHub | 버전 관리 |

---
## 디렉터리 구조

```text
WordChainAI/
├── src/
│   ├── main.py
│   ├── game.py
│   ├── openai_client.py
│   ├── validator.py
│   ├── prompt.py
│   └── config.py
├── docs/
│   └── Plan.md
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---
## 모듈 설계

| 파일 | 역할 |
| --- | --- |
| `main.py` | 프로그램의 진입점(Entry Point)입니다. 게임 객체를 생성하고 실행합니다. |
| `game.py` | 게임의 전체 진행을 담당합니다. 턴 관리, 게임 상태 관리, 사용자 입력 처리 및 승패 판정을 수행합니다. |
| `state.py` | 게임 상태(GameState)를 관리합니다. 현재 단어, 체인 수, 사용 단어 목록, 실수 횟수, 게임 종료 여부 등을 저장합니다. |
| `openai_client.py` | OpenAI Responses API와의 통신을 담당합니다. 프롬프트를 전송하고 응답을 반환합니다. |
| `validator.py` | 사용자와 AI의 응답을 검증합니다. JSON 형식, 끝말잇기 규칙, 중복 단어 등을 확인합니다. |
| `prompt.py` | AI에게 전달할 시스템 프롬프트와 응답 형식을 관리합니다. |
| `config.py` | 환경 변수와 프로젝트 설정을 관리합니다. |

---
## 시스템 흐름

프로그램은 아래와 같은 순서로 동작합니다.

```text
프로그램 시작
    │
    ▼
환경 변수 및 설정 로드
    │
    ▼
Game 객체 생성
    │
    ▼
게임 시작
    │
    ▼
사용자 입력
    │
    ▼
Validator(단어/규칙 검증)
    │
    ▼
OpenAI API 요청
    │
    ▼
AI 응답 수신
    │
    ▼
Validator(JSON/게임 규칙 검증)
    │
    ├───────────────┐
    │               │
    ▼               ▼
검증 성공      AI 실수 +1
    │               │
    └──────┬────────┘
           ▼
게임 상태 갱신
           │
           ▼
승패 판정
           │
           ▼
게임 종료 또는 다음 턴
```

### 모듈 간 상호작용

```text
            main.py
               │
               ▼
            game.py
    ┌──────────┼─────────────┐
    ▼          ▼             ▼
config.py validator.py openai_client.py
                             │
                             ▼
                          prompt.py
```

`game.py`가 사용자 입력을 받아 `validator.py`를 통해 규칙을 검증하고, `openai_client.py`를 통해 OpenAI API와 통신합니다. 이후 AI의 응답 역시 `validator.py`를 통해 JSON 형식과 게임 규칙을 검증한 뒤 게임 상태를 갱신하고 다음 턴을 진행합니다.

---
## AI 응답 형식

AI는 항상 아래 JSON 형식으로 응답하도록 설계합니다.

```json
{
    "word": "사과"
}
```

응답 수신 후 `validator.py`에서 JSON 형식과 게임 규칙을 모두 검증합니다.

---
## 게임 상태 형식

게임의 진행 상태는 하나의 객체로 관리하며, 매 턴 갱신됩니다.

```json
{
    "current_word": "사과",
    "turn": 12,
    "chain_count": 11,
    "user_mistakes": 1,
    "ai_mistakes": 0,
    "allow_one_shot": false,
    "used_words": [
        "학교",
        "교실",
        "실수",
        "수박",
        "박수",
        "수영"
    ],
    "game_over": false,
    "winner": null
}
```

| 필드 | 설명 |
| --- | --- |
| `current_word` | 현재 이어야 하는 단어 |
| `turn` | 현재 턴 번호 |
| `chain_count` | 현재까지 이어진 단어 개수 |
| `user_mistakes` | 사용자 실수 횟수 |
| `ai_mistakes` | AI 실수 횟수 |
| `allow_one_shot` | 한방단어 허용 여부 |
| `used_words` | 사용된 단어 목록 |
| `game_over` | 게임 종료 여부 |
| `winner` | 승자(`"USER"`, `"AI"`, 종료 전에는 `null`) |

---
# 구현 계획

## 개발 순서

| 단계 | 구현 내용 |
| --- | --- |
| 1 | 프로젝트 초기 설정 및 환경 변수 구성 |
| 2 | OpenAI Responses API 연동 |
| 3 | 시스템 프롬프트 및 AI 응답 형식 설계 |
| 4 | 게임 상태(GameState) 구현 |
| 5 | 사용자 입력 및 기본 게임 루프 구현 |
| 6 | 사용자 입력 검증(끝말잇기 규칙, 중복 단어 등) |
| 7 | AI 응답 검증(JSON 형식, 게임 규칙) |
| 8 | 실수 횟수 및 승패 판정 구현 |
| 9 | 응답 시간 제한 구현 |
| 10 | 게임 상태 출력 및 UI 개선 |
| 11 | 예외 처리 및 오류 메시지 개선 |
| 12 | README 및 프로젝트 문서 작성 |

---
## 구현 예정 기능

### 핵심 기능

- OpenAI Responses API 기반 AI 끝말잇기
- JSON 기반 AI 응답 처리
- 끝말잇기 규칙 검증
- 중복 단어 검증
- 사용자 및 AI 실수 횟수 관리
- 게임 상태(GameState) 관리
- 승패 판정
- 10초 응답 제한

### 부가 기능

- 한방단어 허용 여부 선택
- 현재 게임 상태 출력
- 상세 오류 메시지 출력
- 예외 상황 처리(API 오류, JSON 파싱 실패 등)

### 구현 원칙

- LLM의 응답은 항상 검증한 후 사용합니다.
- 게임 상태는 하나의 객체(GameState)에서 관리합니다.
- 각 모듈은 하나의 책임만 갖도록 분리합니다.