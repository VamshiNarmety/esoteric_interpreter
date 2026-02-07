#!/usr/bin/env python3
"""
Esoteric Pascal Interpreter Runner
Supports both file execution and interactive REPL mode.
"""
import sys
import os
import argparse

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter
from src.errors import LexerError, ParserError, SemanticError, RuntimeError


def run_file(filename):
    """Execute a program from a file."""
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        print(f"Running '{filename}'...")
        print("=" * 70)
        
        lexer = Lexer(code)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()
        
        print("=" * 70)
        print(f"✓ Program '{filename}' executed successfully")
        
        if interpreter.GLOBAL_SCOPE:
            print("\nGlobal Variables:")
            for var, value in sorted(interpreter.GLOBAL_SCOPE.items()):
                print(f"  {var} = {value}")
        
        return 0
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return 1
    except (LexerError, ParserError, SemanticError, RuntimeError) as e:
        print(f"\n{e}")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_repl():
    """Run interactive REPL."""
    print("=" * 70)
    print("Esoteric Pascal Interpreter - Interactive Mode")
    print("=" * 70)
    print("\nCommands:")
    print("  show    - Display all global variables")
    print("  clear   - Reset all variables")
    print("  exit    - Exit the interpreter")
    print("  help    - Show this help message")
    print("\nEnter your Pascal code and end with '.' to execute.")
    print("Multi-line input is supported.\n")
    print("=" * 70 + "\n")

    while True:
        try:
            text = input('pascal> ')
            
            if not text:
                continue
            
            cmd = text.strip().lower()
            
            # Handle commands
            if cmd == 'show':
                if Interpreter.GLOBAL_SCOPE:
                    print("\nGlobal Variables:")
                    for var, value in sorted(Interpreter.GLOBAL_SCOPE.items()):
                        print(f"  {var} = {value}")
                else:
                    print("No variables defined yet.")
                continue
                
            elif cmd == 'clear':
                Interpreter.GLOBAL_SCOPE.clear()
                print("✓ All variables cleared")
                continue
                
            elif cmd in ('exit', 'quit'):
                print("Goodbye!")
                break
                
            elif cmd == 'help':
                print("\nCommands:")
                print("  show    - Display all global variables")
                print("  clear   - Reset all variables")
                print("  exit    - Exit the interpreter")
                print("  help    - Show this help message\n")
                continue
            
            # Multi-line input until '.'
            while not text.rstrip().endswith('.'):
                line = input('...    ')
                text += '\n' + line
            
            # Wrap in PROGRAM structure if not already present
            if not text.strip().upper().startswith('PROGRAM'):
                text = f"PROGRAM repl;\nBEGIN\n{text}\nEND."
            
            # Execute
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            interpreter.interpret()
            
            print("✓ Executed successfully")
            
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\n^C\nGoodbye!")
            break
        except (LexerError, ParserError, SemanticError, RuntimeError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Esoteric Pascal Interpreter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_interpreter.py program.txt      # Run code from file
  python run_interpreter.py                  # Start interactive REPL
  python run_interpreter.py --help           # Show this help
  
File format:
  Any text file containing valid Pascal-like code
  Must start with PROGRAM declaration
  
Interactive mode:
  Enter code line by line
  End with '.' to execute
  Special commands: show, clear, exit, help
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Source file to execute (omit for interactive REPL)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='Esoteric Pascal Interpreter 1.0'
    )
    
    args = parser.parse_args()
    
    if args.file:
        return run_file(args.file)
    else:
        run_repl()
        return 0


if __name__ == '__main__':
    sys.exit(main())
