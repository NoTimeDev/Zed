from time import process_time
from src.Parser.Nodes import *
from src.Lexer.TokenKinds import *
from src.Parser.LookUps import *
from src.Utils.Utils import *
from typing import Any, Callable

class Parser:
    def __init__(self, Name: str, SourceLines: list[str], Tokens: list[Token]):
        self.Name: str = Name
        self.SourceLines: list[str] = SourceLines
        self.Tokens: list[Token] = Tokens
        self.Pos: int = 0

        self.Ast: dict = {
            "Kind" : Program,
            "FileName" : self.Name,
            "Body" : []
        }

        self.CreateTokenLookUps()
        self.Err: int = 0
        self.Recerr: bool = False
        self.Eof = False
        
    def CreateTokenLookUps(self):
        nud(TokenKind.Int, self.Parse_Primary)
        nud(TokenKind.Float, self.Parse_Primary)
        nud(TokenKind.String, self.Parse_Primary)
        nud(TokenKind.Char, self.Parse_Primary)

        nud(TokenKind.Minus, self.Parse_Prefix_Expr)
        

        nud(TokenKind.OpenBrack, self.Parse_Sequence)
        nud(TokenKind.Open_C_Brack, self.Parse_Sequence)
        nud(TokenKind.Open_S_Brack, self.Parse_Sequence)
        nud(TokenKind.Ident, self.ParseIdentifier)

        led(TokenKind.Divide, BindingPower.multiplictive, self.Parse_BinExpr)
        led(TokenKind.Star, BindingPower.multiplictive, self.Parse_BinExpr)
        led(TokenKind.Mod, BindingPower.multiplictive, self.Parse_BinExpr)

        led(TokenKind.Plus, BindingPower.additive, self.Parse_BinExpr)
        led(TokenKind.Minus, BindingPower.additive, self.Parse_BinExpr)


        stmt(TokenKind.Let, self.Parse_VarDec)
        stmt(TokenKind.Mut, self.Parse_VarDec)

    def Parse(self) -> dict[Any, Any]: 

        while self.HasTokens():
            self.Ast['Body'].append(self.Parse_Stmt())
        
        if self.Err > 0:
            exit(1)

        return self.Ast


    def Peek(self, num: int) -> Token:
        try:
            self.Tokens[self.Pos + num] # type: ignore
        except IndexError:
            return self.Tokens[-1]
        else:
            return self.Tokens[self.Pos + num]
        
    def CurrentToken(self) -> Token:
        return self.Tokens[self.Pos]
    
    def CurrentTokenKind(self) -> TokenKind:
        return self.CurrentToken().get("Kind") # type: ignore
    
    def Advance(self) -> Token:

        if self.Eof == False:
            tk: Token = self.CurrentToken()
            if self.CurrentTokenKind() == TokenKind.EOF:
                self.Eof = True
            else:
                self.Pos+=1
            return tk
        else:
            self.ZedEofError()
    
    
    def HasTokens(self) -> bool:
        return self.Pos < len(self.Tokens) and self.CurrentTokenKind() != TokenKind.EOF 
    
    def ZedEofError(self):
        rprint(f"{BrightWhite}{self.Name}:{self.CurrentToken().get("Line")}:{self.CurrentToken().get("Start")}: {BrightRed}error: {BrightWhite}Reached end of file while Parsing{Reset}")
        rprint(f"{self.CurrentToken().get("Line")}|{self.SourceLines[self.CurrentToken().get("Line") - 1]}") #type: ignore
        rprint(f"{spaceout(self.CurrentToken().get("Line"))}|{(self.CurrentToken().get("Start") - 1) * ' '}{BrightRed}^{Reset}") #type: ignore 
        exit(1)

    def BasicExpectError(self, msg: str, expects: str):
        CToken = self.Peek(-1)

        rprint(f"{BrightWhite}{self.Name}:{CToken.get("Line")}:{CToken.get("Start")}: {BrightRed}error: {BrightWhite}{Format(msg, {"Before":self.Peek(-1).get("Value"), "After":self.Peek(1).get("Value"), "Got":self.CurrentToken().get("Value")})}{Reset}")
        rprint(f"{CToken.get("Line")}|{self.SourceLines[CToken.get("Line") - 1]}") #type: ignore
        rprint(f"{spaceout(CToken.get("Line"))}|{(CToken.get("End")) * ' '}{BrightRed}{'^'}{Reset}") #type: ignore
        rprint(f"{spaceout(CToken.get("Line"))}|{(CToken.get("End")) * ' '}{BrightBlue}{expects}{Reset}") #type: ignore

        self.Error()
    
    def NodeExpectError(self, msg: str, peek: int, expects: str, Under=False):

        rprint(f"{BrightWhite}{self.Name}:{self.Peek(peek).get("Line")}:{self.Peek(peek).get("Start")}: {BrightRed}error:{BrightWhite} {Format(msg, {"Before":self.Peek(peek - 1).get("Value"), "After":self.Peek(peek + 1).get("Value"), "Got":self.CurrentToken().get("Value")})}{Reset}")
        rprint(f"{self.Peek(peek).get("Line")}|{self.SourceLines[self.Peek(peek).get("Line") - 1]}") # type: ignore
        if Under == False:
            rprint(f"{len(str(self.Peek(peek).get("Line"))) * " "}|{(self.Peek(peek).get("Start") - 1) * " "}{BrightRed}^{Reset}") #type: ignore
            rprint(f"{len(str(self.Peek(peek).get("Line"))) * " "}|{(self.Peek(peek).get("Start") - 1) * " "}{BrightGreen}{expects}{Reset}") #type: ignore
        else:
            rprint(f"{len(str(self.Peek(peek).get("Line"))) * " "}|{(self.Peek(peek).get("Start") - 1) * " "}{BrightRed}^{Reset}") #type: ignore
            rprint(f"{len(str(self.Peek(peek).get("Line"))) * " "}|{(self.Peek(peek).get("Start") - 1) * " "}{BrightGreen}{expects}{Reset}") #type: ignore
            
        self.Error()
    
    def Error(self, Reset: bool =False):
        if Reset == True:
            self.Recerr = False
        else:
            self.Err+=1
            self.Recerr = True

    def Expect(self, Kind: TokenKind, err_msgfunc, Eat: bool=True, Recerr: bool = False, Arg=()) -> Token:
        if Kind == self.CurrentTokenKind():
            return self.Advance()
        else:
            if Recerr == True:
                if self.Recerr == False:
                    err_msgfunc(*Arg)
            
            if(Eat == True): self.Advance()

            return NullToken
        
        
    def Parse_Stmt(self) -> dict:
        stmt_fn = stmt_lu.get(self.CurrentTokenKind())

        if stmt_fn != None:
            return stmt_fn()
        
        expr = self.Parse_Expr(BindingPower.def_bp)
        self.Expect(TokenKind.Semi, self.BasicExpectError, False, True, ("expected ';' after !{Before}", ';'))

        return expr
    
    def Parse_Expr(self, bp: int):
        TKind: TokenKind = self.CurrentTokenKind()
        nud_fn = nud_lu.get(TKind)

        if nud_fn == None:
            self.NodeExpectError("expected expression after '!{Before}'", -1, "Expression")
            self.Advance()

            return NullNode
        
        left: dict = nud_fn()

        while bp_lu.get(self.CurrentTokenKind(), BindingPower.def_bp) > bp:
            TKind = self.CurrentTokenKind()
            led_fn = led_lu.get(TKind)

            if led_fn == None:
                return left

            left = led_fn(left, bp_lu[self.CurrentTokenKind()])

        return left
     
    def Parse_Primary(self) -> dict:
        match self.CurrentTokenKind():
            case TokenKind.Int:
                return {
                    "Kind": Literal.Int,
                    "Value": self.Advance().get("Value")
                }
            case TokenKind.Float:
                return {
                    "Kind": Literal.Float,
                    "Value": self.Advance().get("Value")
                }
            case TokenKind.String:
                return {
                    "Kind" : Literal.String,
                    "Value": self.CheckString(self.CurrentToken().get("Value", ""))
                }
            case TokenKind.Char:
                return {
                    "Kind" : Literal.Char,
                    "Value" : self.CheckString(self.CurrentToken().get("Value", ""))
                }

        return NullNode
    
    def CheckString(self, String: str):
        Pos: int = 1;   
        
        while Pos < len(String) - 1:
            if String[Pos] == "\\":
                if String[Pos + 1] not in ["n", "\\", "t", 'b', "r", "f", "v", "'", '"', "a", "o", "x", "0"]:
                    rprint(f"{BrightWhite}{self.Name}:{self.CurrentToken().get("Line")}:{self.CurrentToken().get("Start") + Pos}: {BrightMagenta}warning:{BrightWhite} '\\{String[Pos + 1]}' is not a valid escape sequence{Reset}")
                    rprint(f"{self.CurrentToken().get("Line")}|{self.SourceLines[self.CurrentToken().get("Line") - 1]}")
                    rprint(f"{spaceout(self.CurrentToken().get("Line"))}|{(self.CurrentToken().get("Start") + Pos - 1) * " "}{BrightMagenta}^~{Reset}")
            Pos+=1
        
        self.Advance()
        return String

    def ParseIdentifier(self):   
        Ident = self.Advance()
        TypeList = []
        Arguments = []

        if self.CurrentTokenKind() == TokenKind.Open_Arrow:
            self.Advance()

            while self.CurrentTokenKind() not in [TokenKind.EOF, TokenKind.Close_Arrow]:
                if self.CurrentTokenKind() == TokenKind.Comma:
                    self.Advance()
                        
                elif  self.CurrentTokenKind() == TokenKind.EOF:
                    self.ZedEofError()
                            
                elif  self.CurrentTokenKind() == TokenKind.Close_Arrow:
                    break 

                else:
                    TypeList.append(self.ParseType())

            self.Expect(TokenKind.Close_Arrow, self.BasicExpectError, True, True, ("expected closing '>' before '!{Before}'", ">"))
    
        if self.CurrentTokenKind() == TokenKind.OpenBrack:
            self.Advance()

            while self.CurrentTokenKind() not in [TokenKind.EOF, TokenKind.CloseBrack]:
                if self.CurrentTokenKind() == TokenKind.Comma:
                    self.Advance()
                        
                elif  self.CurrentTokenKind() == TokenKind.EOF:
                    self.ZedEofError()
                            
                elif  self.CurrentTokenKind() == TokenKind.CloseBrack:
                    break 

                else:
                    Arguments.append(self.Parse_Expr(BindingPower.def_bp))

            self.Expect(TokenKind.CloseBrack, self.BasicExpectError, True, True, ("expected closing ')' before '!{Before}'", ")"))
    
               
        self.Error(True) 
        return {
            "Kind" : Expression.Identifier,
            "Identifier" : Ident.get("Value"),
            "TemplateList" : TypeList,
            "Arguments" : Arguments
        }

    def Parse_BinExpr(self, left: dict, bp: int) -> dict:
        Op: str = self.Advance().get("Value") # type: ignore
        right: dict = self.Parse_Expr(bp)

        return {
            "Kind" : Expression.BinExpr,
            "Left" : left,
            "Right" : right,
            "Op" : Op
        }

    def ParseType(self) -> dict:
        match self.CurrentTokenKind():
            case TokenKind.Type:  
                return {
                    "Kind" : Type.BsType,
                    "Type" : self.Advance().get("Value"),
                }

            case _:
                self.BasicExpectError("'!{Got}' is not a valid type", "")
                self.Advance()
        return NullNode

    def Parse_VarDec(self) -> dict:
        IsMut: bool = TokenKind.Mut == self.Advance().get("Kind") #eat let, mut
        
        VarNames: list[str] = []
        while self.CurrentTokenKind() == TokenKind.Ident:
            VarNames.append(self.Advance().get("Value")) # type: ignore

            if self.CurrentTokenKind() == TokenKind.Comma:
                self.Advance()
        
        if self.CurrentTokenKind() == TokenKind.Colon_Equals:
            self.Advance()
            Expr: dict = self.Parse_Expr(BindingPower.def_bp)
            

            self.Expect(TokenKind.Semi, self.BasicExpectError, False, True, ("expected ';' after variable declartion", ';'))
            self.Error(True)

            return {
                "Kind" : Statement.VarDec,
                "IsMut" : IsMut,
                "Name(s)" : VarNames,
                "Type" : {
                    "Kind" : Type.AtType,
                    "Type" : "Auto",
                },
                "Initializer" : Expr, 
            }

        else:
            self.Expect(TokenKind.Colon, self.BasicExpectError, True, True, ("expected ':' after '!{Before}'", ':'))
            TypeOfVar: dict = self.ParseType()
            
            if self.CurrentTokenKind() == TokenKind.Semi:
                if IsMut == False:
                    if self.Recerr == False:
                        self.NodeExpectError("constant variables must have some initializer", 0, "= Expression?", True)
                self.Advance()

                self.Error(True)
                return {
                    "Kind" : Statement.VarDec,
                    "IsMut" : IsMut,
                    "Name(s)" : VarNames,
                    "Type" : TypeOfVar,
                    "Initializer" : NullNode
                } 
                
            self.Expect(TokenKind.Equals, self.BasicExpectError, True, True, ("expected '=' after '!{Before}'", "="))
            Expr = self.Parse_Expr(BindingPower.def_bp)
            self.Expect(TokenKind.Semi, self.BasicExpectError, False, True, ("expected ';' after variable declartion", ';'))


            return {
                "Kind" : Statement.VarDec,
                "IsMut" : IsMut,
                "Name(s)" : VarNames,
                "Type" : TypeOfVar,
                "Initializer" : Expr
            }
    
    def Parse_Prefix_Expr(self) -> dict:
        match self.CurrentTokenKind():
            case TokenKind.Minus:
                return {
                    "Kind" : Expression.UExpr,
                    "Operator" : self.Advance().get("Value"),
                    "Expr" : self.Parse_Expr(BindingPower.def_bp)
                }

        return NullNode

    def Parse_Sequence(self) -> dict:
        match self.CurrentTokenKind():
            case TokenKind.OpenBrack:
                self.Advance()
                

                Expr = self.Parse_Expr(BindingPower.def_bp)
                
                if self.CurrentTokenKind() ==  TokenKind.Comma:
                    ExprList: list[dict] = [Expr]

                    while self.CurrentTokenKind() not in [TokenKind.EOF, TokenKind.CloseBrack]:
                        if self.CurrentTokenKind() == TokenKind.Comma:
                            self.Advance()
                        
                        elif  self.CurrentTokenKind() == TokenKind.EOF:
                            self.ZedEofError()
                            
                        elif  self.CurrentTokenKind() == TokenKind.CloseBrack:
                            break 

                        else:
                            ExprList.append(self.Parse_Expr(BindingPower.def_bp))

                    self.Expect(TokenKind.CloseBrack, self.BasicExpectError, True, True, ("expected closing ')' before !{Before}'", ")"))
                    return {
                            "Kind" : Expression.TupleExpr,
                            "Items" : ExprList,
                            "Types" : [] #this will be filled in the typechecker 
                    }

                else:
                    self.Expect(TokenKind.CloseBrack, self.BasicExpectError, True, True, ("expected closing ')' before !{Before}'", ")"))
                    return Expr

            case TokenKind.Open_C_Brack:
                self.Advance()
                
                Expr = self.Parse_Expr(BindingPower.def_bp)
                
                
                ExprList: list[dict] = [Expr]

                while self.CurrentTokenKind() not in [TokenKind.EOF, TokenKind.Close_C_Brack]:
                    if self.CurrentTokenKind() == TokenKind.Comma:
                        self.Advance()
                        
                    elif  self.CurrentTokenKind() == TokenKind.EOF:
                        self.ZedEofError()
                            
                    elif  self.CurrentTokenKind() == TokenKind.Close_C_Brack:
                        break 

                    else:
                        ExprList.append(self.Parse_Expr(BindingPower.def_bp))

                self.Expect(TokenKind.Close_C_Brack, self.BasicExpectError, True, True, ("expected closing '}' before '!{Before}'", "}"))

                return {
                    "Kind" : Expression.ArrExpr,
                    "Items" : ExprList,
                }  

            case TokenKind.Open_S_Brack:
                self.Advance()
                
                Expr = self.Parse_Expr(BindingPower.def_bp)
                
                
                ExprList: list[dict] = [Expr]

                while self.CurrentTokenKind() not in [TokenKind.EOF, TokenKind.Close_S_Brack]:
                    if self.CurrentTokenKind() == TokenKind.Comma:
                        self.Advance()
                        
                    elif  self.CurrentTokenKind() == TokenKind.EOF:
                        self.ZedEofError()
                            
                    elif  self.CurrentTokenKind() == TokenKind.Close_S_Brack:
                        break 

                    else:
                        ExprList.append(self.Parse_Expr(BindingPower.def_bp))

                self.Expect(TokenKind.Close_S_Brack, self.BasicExpectError, True, True, ("expected closing ']' before !{Before}'", "]"))
                return {
                    "Kind" : Expression.ArrExpr,
                    "Items" : ExprList,
                }
            case _:
                return NullNode
