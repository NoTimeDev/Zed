from typing import Union
from src.Lexer.TokenKinds import *
from src.Utils.Utils import *

#i Could care less how slow this is

class Lexer:
    def __init__(self, Code: str, Name: str):
        self.SourceCode: str = Code
        self.SourceLines: list[str] = Code.split('\n')
        self.Name: str = Name
        self.Err: int = 0

        self.Alphas: dict[str, TokenKind] = {
            #Keywords
            "let" : TokenKind.Let,
            "mut" : TokenKind.Mut,

            #Types
            "i64" : TokenKind.Type,
            "i32" : TokenKind.Type,
            "i16" : TokenKind.Type,
            "i8" : TokenKind.Type,
            "bool" : TokenKind.Type,
            
            "f32" : TokenKind.Type,
            "f64" : TokenKind.Type,
            
            "String" : TokenKind.Type,
            "Any" : TokenKind.Type,
            
        }

    def Lex(self) -> list[Token]:
        Tokens: list[Token] = []
        
        Line: int = 1
        Coloum: int = 1
        Pos: int = 0

        def push(Val: str, Kind: TokenKind, Line: int, Start: int, End: int):
            Tokens.append({"Value": Val, "Kind":Kind, "Line":Line, "Start":Start, "End":End})

        def peek(num: int):
            return self.SourceCode[Pos + num : Pos + num + 1]
        
        while Pos < len(self.SourceCode):
            match self.SourceCode[Pos]:
                case ' ':
                    Pos+=1; Coloum+=1
                
                case '\n':
                    Pos+=1; Coloum = 1; Line+=1
                
                case '+':
                    push("+", TokenKind.Plus, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1                
                
                case '-':
                    push("-", TokenKind.Minus, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1                
                
                case '*':
                    push("*", TokenKind.Star, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1               
                
                case '/':
                    push("/", TokenKind.Divide, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1                
                
                case '%':
                    push("%", TokenKind.Mod, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case ';':
                    push(";", TokenKind.Semi, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case '&':
                    if peek(1) == "&":
                        push("&&", TokenKind.ConstAdr, Line, Coloum, Coloum + 1)
                    else:
                        push("&", TokenKind.And, Line, Coloum, Coloum)
                case ':':
                    if peek(1) == "=":
                        push(":=", TokenKind.Colon_Equals, Line, Coloum, Coloum + 1)
                        Pos+=2; Coloum+=2
                    else:
                        push(":", TokenKind.Colon, Line, Coloum, Coloum)
                        Pos+=1; Coloum+=1
                
                case '=':
                    push("=", TokenKind.Equals, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case '(':
                    push("(", TokenKind.OpenBrack, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case ')':
                    push(")", TokenKind.CloseBrack, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case '[':
                    push("[", TokenKind.Open_S_Brack, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case ']':
                    push("]", TokenKind.Close_S_Brack, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1                
                
                case '{':
                    push("{", TokenKind.Open_C_Brack, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case '}':
                    push("}", TokenKind.Close_C_Brack, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case '<':
                    push("<", TokenKind.Open_Arrow, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1 
                
                case '>':
                    push(">", TokenKind.Close_Arrow, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1 
                    
                case ',':
                    push(",", TokenKind.Comma, Line, Coloum, Coloum)
                    Pos+=1; Coloum+=1
                
                case _:
                    if self.SourceCode[Pos].isdigit():
                        NUMBERLIST = '0123456789abcdefABCDEF_.Xx'
                        NUMBERHEXLIST = "abcdefxABCDEFX"
                        Number: str = ""
                        DotCount: int = 0
                        Start: int = Coloum
                        Dots = []

                        while self.SourceCode[Pos] in NUMBERLIST:
                            if self.SourceCode[Pos] != '_':
                                if self.SourceCode[Pos] == '.':
                                    DotCount+=1
                                    Dots.append(Coloum)

                                Number+=self.SourceCode[Pos]
                            Pos+=1; Coloum+=1

                        if DotCount >= 1:
                            #throw error if hexi decimal
                            if DotCount > 1:
                                rprint(f"{BrightWhite}{self.Name}:{Line}:{Start}{BrightRed}: error:{BrightWhite} a constant float must not multiple points(.){Reset}")
                                rprint(f"{Line}|{self.SourceLines[Line - 1]}")
                                rprint(f"{spaceout(Line)}|{BrightRed}{repp(" ", Dots)}{Reset}")

                                self.Err+=1

                            else:
                                try:
                                    float(Number)
                                except ValueError:
                                    rprint(f"{BrightWhite}{self.Name}:{Line}:{Start}{BrightRed}: error:{BrightWhite} a constant float cannot contain a hexi decimal number{Reset}")
                                    rprint(f"{Line}|{self.SourceLines[Line - 1]}")
                                    rprint(f"{spaceout(Line)}|{BrightBlue}{fillfrp("^", Dots, len(Number))}{Reset}")
                                    self.Err+=1

                            push(Number, TokenKind.Float, Line, Start, Coloum - 1)
                        else: 
                            if Number.lower().startswith('0x'):
                                Number = str(int(Number, 16))

                            ishex = False
                            for i in Number:
                                if i in NUMBERHEXLIST:
                                    ishex = True

                            if ishex == True:
                                rprint(f"{BrightWhite}{self.Name}:{Line}:{Start}{BrightRed}: error:{BrightWhite} '{Number}' is not a valid hexi decimal number{Reset}")
                                rprint(f"{Line}|{self.SourceLines[Line - 1]}")
                                rprint(f"{spaceout(Line)}|{BrightRed}{(Start - 1) * " "}{len(Number) * "^"}{Reset}")
                                self.Err+=1             
                            push(Number, TokenKind.Int, Line, Start, Coloum - 1)
                    elif self.SourceCode[Pos].isalpha() or self.SourceCode[Pos] == '_':
                        Start: int = Coloum
                        Alpha: str = ""
                        while self.SourceCode[Pos].isalnum() or self.SourceCode[Pos] == '_':
                            Alpha+=self.SourceCode[Pos]

                            Pos+=1; Coloum+=1
                        
                        if self.Alphas.get(Alpha) != None:
                            push(Alpha, self.Alphas[Alpha], Line, Start, Coloum - 1)
                        else:
                            push(Alpha, TokenKind.Ident, Line, Start, Coloum - 1)
                    elif self.SourceCode[Pos] == '"':
                        Start: int = Coloum
                        String: str = "\""
                        Got_Unterminated: bool = False
                        Pos+=1; Coloum+=1
                        while True:
                            if String[-1] != '\\' and self.SourceCode[Pos] == '"':
                                break
                            if self.SourceCode[Pos] == '\n':
                                rprint(f"{BrightWhite}{self.Name}:{Line}:{Coloum}: {BrightRed}error:{BrightWhite} missing terminating \" character{Reset}")
                                rprint(f"{Line}|{self.SourceLines[Line - 1]}")
                                rprint(f"{spaceout(Line)}|{BrightRed}{(Start - 1) * ' '}^{(len(String) - 1) * '~'}{Reset}")
                                Got_Unterminated = True
                                self.Err+=1
                                break
                                 
                            String+=self.SourceCode[Pos]
                            Pos+=1; Coloum+=1
                        
                        if Got_Unterminated == False:
                            Pos+=1; Coloum+=1
                        
                        push(String + '"', TokenKind.String, Line, Start, Coloum - 1)
                    elif self.SourceCode[Pos] == "'":
                        Start: int = Coloum
                        Character: str = "'"
                        Got_Unterminated: bool = False
                        Pos+=1; Coloum+=1
                        while True:
                            if Character[-1] != '\\' and self.SourceCode[Pos] == "'":
                                break
                            elif self.SourceCode[Pos] == '\n':
                                rprint(f"{BrightWhite}{self.Name}:{Line}:{Coloum}: {BrightRed}error:{BrightWhite} missing terminating ' character{Reset}")
                                rprint(f"{Line}|{self.SourceLines[Line - 1]}")
                                rprint(f"{spaceout(Line)}|{BrightRed}{(Start - 1) * ' '}^{(len(Character) - 1) * '~'}{Reset}")
                                Got_Unterminated = True
                                self.Err+=1
                                break

                            Character+=self.SourceCode[Pos]
                            Pos+=1; Coloum+=1
                        
                        if Got_Unterminated == False:
                            Pos+=1; Coloum+=1

                        if Got_Unterminated == False:
                            if len(Character) > 2:
                                if len(Character) != 1 and Character[1] != "\\":
                                    rprint(f"{BrightWhite}{self.Name}:{Line}:{Coloum}: {BrightRed}error:{BrightWhite} multi-character char constant")
                                    rprint(f"{Line}|{self.SourceLines[Line - 1]}")
                                    rprint(f"{spaceout(Line)}|{BrightRed}{(Start - 1) * ' '}^{(len(Character) - 1) * '~'}{Reset}")
                                    self.Err+=1

                        push(Character + "'", TokenKind.Char, Line, Start, Coloum - 1)
                    else:
                        rprint(f"{BrightWhite}{self.Name}:{Line}:{Coloum}{BrightRed}: error:{BrightWhite} unrecognized token '{self.SourceCode[Pos]}'{Reset}")
                        rprint(f"{Line}|{self.SourceLines[Line - 1]}")
                        rprint(f"{spaceout(Line)}|{BrightRed}{(Coloum - 1) * " "}^{Reset}")
                        self.Err+=1             
                        Pos+=1; Coloum+=1                                    

        if self.Err > 0:
            exit(1)

        if len(Tokens) != 0:
            push("end of file", TokenKind.EOF, Tokens[-1].get("Line"), Tokens[-1].get("End") + 1, Tokens[-1].get("End") + 1) #type: ignore
       
        return Tokens

