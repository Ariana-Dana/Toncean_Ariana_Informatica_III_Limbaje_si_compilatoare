from ast_nodes import (
    Program, Block, VarDecl, Assignment, PrintStmt,
    IfStmt, WhileStmt, BinaryOp, UnaryOp, Literal, Variable
)


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        self.visit(node)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise SemanticError(f"Nu exista metoda de analiza pentru {type(node).__name__}")

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Block(self, node: Block):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node: VarDecl):
        if node.name in self.symbol_table:
            raise SemanticError(f"Variabila '{node.name}' este deja declarata")
        self.symbol_table[node.name] = node.var_type

    def visit_Assignment(self, node: Assignment):
        if node.name not in self.symbol_table:
            raise SemanticError(f"Variabila '{node.name}' nu a fost declarata")

        var_type = self.symbol_table[node.name]
        expr_type = self.visit(node.expr)

        if not self.is_assign_compatible(var_type, expr_type):
            raise SemanticError(
                f"Nu se poate atribui expresie de tip '{expr_type}' variabilei "
                f"'{node.name}' de tip '{var_type}'"
            )

    def visit_PrintStmt(self, node: PrintStmt):
        self.visit(node.expr)

    def visit_IfStmt(self, node: IfStmt):
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise SemanticError("Conditia din if trebuie sa fie de tip bool")
        self.visit(node.then_block)

    def visit_WhileStmt(self, node: WhileStmt):
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise SemanticError("Conditia din while trebuie sa fie de tip bool")
        self.visit(node.body)

    def visit_Literal(self, node: Literal):
        return node.literal_type

    def visit_Variable(self, node: Variable):
        if node.name not in self.symbol_table:
            raise SemanticError(f"Variabila '{node.name}' nu a fost declarata")
        return self.symbol_table[node.name]

    def visit_UnaryOp(self, node: UnaryOp):
        operand_type = self.visit(node.operand)

        if node.op == '!':
            if operand_type != "bool":
                raise SemanticError("Operatorul '!' se aplica doar pe bool")
            return "bool"

        elif node.op == '-':
            if operand_type not in ("int", "float"):
                raise SemanticError("Operatorul '-' unar se aplica doar pe int sau float")
            return operand_type

        raise SemanticError(f"Operator unar necunoscut: {node.op}")

    def visit_BinaryOp(self, node: BinaryOp):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op

        if op in ['+', '-', '*', '/', '%']:
            if left_type not in ("int", "float") or right_type not in ("int", "float"):
                raise SemanticError(
                    f"Operatorul '{op}' necesita operanzi numerici, nu '{left_type}' si '{right_type}'"
                )

            if op == '%':
                if left_type != "int" or right_type != "int":
                    raise SemanticError("Operatorul '%' functioneaza doar pe int")

            if op in ['/', '%'] and isinstance(node.right, Literal) and node.right.value == 0:
                raise SemanticError("Impartire la zero detectata")

            if left_type == "float" or right_type == "float":
                return "float"
            return "int"

        elif op in ['==', '!=', '<', '>', '<=', '>=']:
            if left_type != right_type:
                if not ({left_type, right_type} <= {"int", "float"}):
                    raise SemanticError(
                        f"Comparatie invalida intre '{left_type}' si '{right_type}'"
                    )
            return "bool"

        elif op in ['&&', '||']:
            if left_type != "bool" or right_type != "bool":
                raise SemanticError(
                    f"Operatorul '{op}' necesita operanzi bool, nu '{left_type}' si '{right_type}'"
                )
            return "bool"

        raise SemanticError(f"Operator necunoscut: {op}")

    def is_assign_compatible(self, var_type, expr_type):
        if var_type == expr_type:
            return True

        if var_type == "float" and expr_type == "int":
            return True

        return False