#like enum classes in a way but not 

Program: str = "Program"

class Type:
    BsType = "BasicType"
    AtType = "AutoType"

class Statement:
    VarDec: str = "Variable Declaration"

class Expression:
    BinExpr: str = "Binary Expression"
    UExpr: str = "Unary Expression"
    ArrExpr: str = "Array Expression" 
    TupleExpr: str = "Tuple Expression" 
    
    Identifier: str = "Identifier Expression"

class Literal:
    Float: str = "Float Literal"
    Int: str = "Integer Literal"

    String: str = "String Literal"
    Char: str = "Character Literal"

NullNode = {"Kind":"Null"}


    
