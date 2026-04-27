import re


class CodeGeneratorC:
    def __init__(self, instructions):
        self.instructions = instructions
        self.lines = []
        self.declared_vars = {}  
        self.temp_vars = {}     
        self.label_set = set()

    def generate(self):
        self.lines.append("#include <stdio.h>")
        self.lines.append("#include <stdbool.h>")
        self.lines.append("")
        self.lines.append("int main() {")

        self.collect_info()
        self.emit_declarations()
        self.emit_instructions()

        self.lines.append("    return 0;")
        self.lines.append("}")
        return "\n".join(self.lines)

    def collect_info(self):
        for instr in self.instructions:
            if instr.startswith("DECL "):
                parts = instr.split()
                var_type = parts[1]
                var_name = parts[2]
                self.declared_vars[var_name] = var_type

        for instr in self.instructions:
            if instr.endswith(":"):
                self.label_set.add(instr[:-1])

        binary_pattern = re.compile(
            r"^(t\d+)\s*=\s*(\S+)\s*(\+|\-|\*|\/|%|==|!=|<|>|<=|>=|&&|\|\|)\s*(\S+)$"
        )
        unary_pattern = re.compile(r"^(t\d+)\s*=\s*(!|-)(\S+)$")
        assign_pattern = re.compile(r"^(t\d+)\s*=\s*(\S+)$")

        for instr in self.instructions:
            m = binary_pattern.match(instr)
            if m:
                target, left, op, right = m.groups()
                left_type = self.infer_expr_type(left)
                right_type = self.infer_expr_type(right)

                if op in ["==", "!=", "<", ">", "<=", ">=", "&&", "||"]:
                    self.temp_vars[target] = "bool"
                elif op == "%":
                    self.temp_vars[target] = "int"
                else:
                    if left_type == "float" or right_type == "float":
                        self.temp_vars[target] = "float"
                    elif left_type == "int" and right_type == "int":
                        self.temp_vars[target] = "int"
                    else:
                        self.temp_vars[target] = "float"
                continue

            m = unary_pattern.match(instr)
            if m:
                target, op, operand = m.groups()
                operand_type = self.infer_expr_type(operand)
                if op == "!":
                    self.temp_vars[target] = "bool"
                else:
                    self.temp_vars[target] = operand_type if operand_type in ("int", "float") else "float"
                continue

            m = assign_pattern.match(instr)
            if m:
                target, source = m.groups()
                if target.startswith("t"):
                    self.temp_vars[target] = self.infer_expr_type(source)

    def emit_declarations(self):
        for name, typ in self.declared_vars.items():
            self.lines.append(f"    {self.map_type(typ)} {name};")

        for temp in sorted(self.temp_vars.keys(), key=lambda x: int(x[1:])):
            self.lines.append(f"    {self.map_type(self.temp_vars[temp])} {temp};")

        if self.declared_vars or self.temp_vars:
            self.lines.append("")

    def emit_instructions(self):
        for instr in self.instructions:
            if instr.startswith("DECL "):
                continue

            if instr.endswith(":"):
                self.lines.append(instr)
                continue

            if instr.startswith("IF "):
                parts = instr.split()
                cond = self.convert_expr(parts[1])
                label = parts[3]
                self.lines.append(f"    if ({cond}) goto {label};")
                continue

            if instr.startswith("GOTO "):
                label = instr.split()[1]
                self.lines.append(f"    goto {label};")
                continue

            if instr.startswith("PRINT "):
                value = instr.split(maxsplit=1)[1]
                self.emit_print(value)
                continue

            if "=" in instr:
                left, right = [x.strip() for x in instr.split("=", 1)]
                right = self.convert_expr(right)
                self.lines.append(f"    {left} = {right};")
                continue

    def emit_print(self, value):
        value = self.convert_expr(value)
        val_type = self.infer_expr_type(value)

        if value == "true":
            self.lines.append('    printf("true\\n");')
            return
        if value == "false":
            self.lines.append('    printf("false\\n");')
            return

        if val_type == "bool":
            self.lines.append(f'    printf("%s\\n", ({value}) ? "true" : "false");')
        elif val_type == "int":
            self.lines.append(f'    printf("%d\\n", {value});')
        elif val_type == "float":
            self.lines.append(f'    printf("%g\\n", (double)({value}));')
        else:
            self.lines.append(f'    printf("%g\\n", (double)({value}));')

    def infer_expr_type(self, expr):
        expr = expr.strip()

        if expr == "true" or expr == "false":
            return "bool"

        if expr in self.declared_vars:
            return self.declared_vars[expr]

        if expr in self.temp_vars:
            return self.temp_vars[expr]

        if re.fullmatch(r"-?\d+", expr):
            return "int"

        if re.fullmatch(r"-?\d+\.\d+", expr):
            return "float"

        return "float"

    def map_type(self, var_type):
        if var_type == "int":
            return "int"
        if var_type == "float":
            return "double"
        if var_type == "bool":
            return "bool"
        return "double"

    def convert_expr(self, expr):
        expr = expr.replace("true", "true")
        expr = expr.replace("false", "false")
        return expr