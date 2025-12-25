"""Pascal Interpreter REPL."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter

def main():
    print("Pascal Interpreter REPL")
    print("\nVariables are stored in GLOBAL_SCOPE. Type 'show' to see all variables.\n")

    while True:
        try:
            text = input('pascal> ')
            if not text:
                continue
            if text.strip().lower() == 'show':
                print("GLOBAL_SCOPE:", Interpreter.GLOBAL_SCOPE)
                continue
            if text.strip().lower() == 'clear':
                Interpreter.GLOBAL_SCOPE.clear()
                print("GLOBAL_SCOPE cleared")
                continue
            while not text.rstrip().endswith('.'):
                line = input('>> ')
                text += '\n' + line
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            interpreter.interpret()
            print("Program executed successfully")
        except EOFError:
            print("\nExit")
            break
        except KeyboardInterrupt:
            print("\nExit")
            break
        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    main()