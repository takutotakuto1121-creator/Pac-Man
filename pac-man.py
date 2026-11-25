from src import main
from sys import stderr

if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(f"[Error] {e}", file=stderr)
