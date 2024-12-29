import time
start = time.perf_counter()


import sys
from json import dumps

from src.Utils.Utils import *
from src.Lexer.Lexer import *
from src.Parser.Parser import *

"c\n"

def main():
    argv = sys.argv
    argc = len(argv)

    if argc == 1:
        rprint(f"{BrightWhite}zedc:{BrightRed} fatal error:{Reset} no input files")
        exit(1)

    filename: str = argv[1]

    try:
        with open(filename, "r") as File:
            SourceCode: str = File.read()
            SourceCode+="\n"
    except FileNotFoundError:
        rprint(f"{BrightRed}fatal error:{Reset} No such file or directory '{filename}'", )
        exit(1)

    LexerClass: Lexer = Lexer(SourceCode, filename)
    LexedToken: list[Token] = LexerClass.Lex()    

    if len(LexedToken) == 0:
        rprint(f"{BrightRed}fatal error:{Reset} Empty file")
        exit(1)

    if not "break-lex" in argv:
        ParserClass: Parser = Parser(filename, SourceCode.split('\n'), LexedToken)
        Ast: dict = ParserClass.Parse()
        print(dumps(Ast, indent=2))
    else:
        for i in LexedToken: print(i)
    

if __name__ == '__main__':
    main()
    
    #time
    end = time.perf_counter()
    d = end - start

    minutes = int(d // 60)
    sec = int(d % 60)
    mil = int((d % 1) * 1000)

    if minutes > 0:
        print(f"{minutes} min(s), {sec} sec(s), {mil} ms", end="")
    elif sec > 0:
        print(f"{sec} sec(s), {mil} ms", end="")
    else:
        print(f"{mil} ms", end="")

