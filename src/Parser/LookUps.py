from typing import Any
from src.Lexer.TokenKinds import TokenKind

value = -1
def n():
    global value
    value+=1
    return value

class BindingPower:
    def_bp = n()
    comma = n()
    assignment = n()
    logical = n()
    relational = n()
    additive = n()
    multiplictive = n()
    unary = n()
    call = n()
    member = n()
    primary = n()

stmt_lu: dict[TokenKind, Any] = {}
nud_lu: dict[TokenKind, Any] = {}
led_lu: dict[TokenKind, Any] = {}
bp_lu: dict[TokenKind, int] = {TokenKind.Semi : BindingPower.def_bp, TokenKind.EOF : BindingPower.def_bp}

def led(Kind: TokenKind, bp: int, led_fn):
    bp_lu[Kind] = bp
    led_lu[Kind] = led_fn

def nud(Kind: TokenKind, nud_fn):
    bp_lu[Kind] = BindingPower.primary
    nud_lu[Kind] = nud_fn

def stmt(Kind: TokenKind, stmt_fn):
    bp_lu[Kind] = BindingPower.def_bp
    stmt_lu[Kind] = stmt_fn
