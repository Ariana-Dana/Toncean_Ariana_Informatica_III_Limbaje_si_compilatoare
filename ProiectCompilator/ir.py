from ast_nodes import (
    Program, Block, VarDecl, Assignment, PrintStmt,
    IfStmt, WhileStmt, BinaryOp, UnaryOp, Literal, Variable
)


class IRGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instruction):
        self.instructions.append(instruction)

    def generate(self, node):
        self.visit(node)
        return self.instructions

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"Nu exista metoda IR pentru {type(node).__name__}")

    def visit_Program(self, node: Program):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Block(self, node: Block):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node: VarDecl):
        self.emit(f"DECL {node.var_type} {node.name}")

    def visit_Assignment(self, node: Assignment):
        value = self.visit(node.expr)
        self.emit(f"{node.name} = {value}")

    def visit_PrintStmt(self, node: PrintStmt):
        value = self.visit(node.expr)
        self.emit(f"PRINT {value}")

    def visit_IfStmt(self, node: IfStmt):
        cond = self.visit(node.condition)
        label_true = self.new_label()
        label_end = self.new_label()

        self.emit(f"IF {cond} GOTO {label_true}")
        self.emit(f"GOTO {label_end}")
        self.emit(f"{label_true}:")
        self.visit(node.then_block)
        self.emit(f"{label_end}:")

    def visit_WhileStmt(self, node: WhileStmt):
        label_start = self.new_label()
        label_body = self.new_label()
        label_end = self.new_label()

        self.emit(f"{label_start}:")
        cond = self.visit(node.condition)
        self.emit(f"IF {cond} GOTO {label_body}")
        self.emit(f"GOTO {label_end}")
        self.emit(f"{label_body}:")
        self.visit(node.body)
        self.emit(f"GOTO {label_start}")
        self.emit(f"{label_end}:")

    def visit_Literal(self, node: Literal):
        if node.literal_type == "bool":
            return "true" if node.value else "false"
        return str(node.value)

    def visit_Variable(self, node: Variable):
        return node.name

    def visit_UnaryOp(self, node: UnaryOp):
        operand = self.visit(node.operand)
        temp = self.new_temp()
        self.emit(f"{temp} = {node.op}{operand}")
        return temp

    def visit_BinaryOp(self, node: BinaryOp):
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.new_temp()
        self.emit(f"{temp} = {left} {node.op} {right}")
        return temp