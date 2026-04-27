from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    BOOL_LITERAL = auto()

    IDENTIFIER = auto()

    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    IF = auto()
    WHILE = auto()
    PRINT = auto()

    PLUS = auto()        
    MINUS = auto()       
    MUL = auto()         
    DIV = auto()         
    MOD = auto()         

    EQ = auto()         
    NEQ = auto()         
    LT = auto()         
    GT = auto()          
    LE = auto()          
    GE = auto()          

    AND = auto()         
    OR = auto()          
    NOT = auto()         

    ASSIGN = auto()      

    LPAREN = auto()      
    RPAREN = auto()      
    LBRACE = auto()      
    RBRACE = auto()      
    SEMICOLON = auto()   
    COMMA = auto()       

    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: object
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value}, line={self.line}, col={self.column})"