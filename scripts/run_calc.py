"""Simple calculator REPL using the interpreter."""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.interpreter.interpreter import Interpreter

def main():
    print("Simple Calculator")
    while True:
        try:
            text = input('calc> ')
            if not text:
                continue
            interpreter = Interpreter(text)
            result = interpreter.expr()
            print(result)
        except EOFError:
            print("Exit")
            break
        except KeyboardInterrupt:
            print("Exit")
            break
        except Exception as e:
            print(f'Error: {e}')


if __name__=='__main__':
    main()