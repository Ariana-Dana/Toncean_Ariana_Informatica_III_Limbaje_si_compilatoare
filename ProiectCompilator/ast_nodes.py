from dataclasses import dataclass, field
from typing import List, Optional, Any


class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]


@dataclass
class VarDecl(ASTNode):
    var_type: str
    name: str


@dataclass
class Assignment(ASTNode):
    name: str
    expr: ASTNode


@dataclass
class PrintStmt(ASTNode):
    expr: ASTNode


@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_block: Block


@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode
    body: Block


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    op: str
    operand: ASTNode


@dataclass
class Literal(ASTNode):
    value: Any
    literal_type: str   


@dataclass
class Variable(ASTNode):
    name: str