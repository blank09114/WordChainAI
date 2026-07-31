import msvcrt
import time


def timed_input(prompt: str, timeout: int = 10) -> str | None:
    """
        timeout초 안에 입력하면 문자열 반환
        시간 초과 시 None 반환
    """

    print(prompt, end="", flush=True)

    text = ""
    start = time.time()

    while True:
        # 키 입력
        if msvcrt.kbhit():
            ch = msvcrt.getwche()

            # 엔터
            if ch == "\r":
                print()
                return text.strip()

            # 백스페이스
            elif ch == "\b":
                if text:
                    text = text[:-1]
                    # 화면에서도 한 글자 삭제
                    print(" \b", end="", flush=True)

            # Ctrl+C
            elif ch == "\x03":
                raise KeyboardInterrupt

            else:
                text += ch

        # 시간 초과
        if time.time() - start >= timeout:
            print()
            return None

        time.sleep(0.01)