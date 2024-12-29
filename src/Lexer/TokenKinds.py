from enum import Enum, auto
from typing import Union



class TokenKind(Enum):
    Minus = auto()
    Plus = auto()
    Star = auto()
    Divide = auto()
    Mod = auto()
    And = auto()
    ConstAdr = auto()

    Inc = auto()
    Dec = auto()


    Int = auto()
    Float = auto()
    String = auto()
    Char = auto()


    Colon_Equals = auto() #there is no suck thing as a walrus operator its called Colon Equals trust me bro
    Equals = auto()
    Colon = auto()

    Comma = auto()

    OpenBrack = auto()
    CloseBrack = auto()
    Open_C_Brack = auto()
    Close_C_Brack = auto() 
    Open_S_Brack = auto()
    Close_S_Brack = auto()

    Open_Arrow = auto()
    Close_Arrow = auto()

    Semi = auto()
    Ident = auto()

    Let = auto()
    Mut = auto()

    Type = auto()

    Null = auto()
    EOF = auto()

Token = dict[str, Union[int, str, TokenKind]]


NullToken: Token = {'Value': 'NULL', 'Kind': TokenKind.Null, 'Line': 0, 'Start': 0, 'End': 0}
