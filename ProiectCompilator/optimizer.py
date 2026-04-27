import re


class Optimizer:
    def __init__(self, instructions):
        self.instructions = instructions

    def optimize(self):
        optimized = self.constant_folding(self.instructions)
        optimized = self.remove_redundant_assignments(optimized)
        return optimized

    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def is_bool(self, value):
        return value in ("true", "false")

    def parse_literal(self, value):
        if value == "true":
            return True
        if value == "false":
            return False
        if "." in value:
            return float(value)
        return int(value)

    def format_literal(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return str(value)
        return str(value)

    def eval_binary(self, left, op, right):
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        elif op == "%":
            return left % right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "<":
            return left < right
        elif op == ">":
            return left > right
        elif op == "<=":
            return left <= right
        elif op == ">=":
            return left >= right
        elif op == "&&":
            return left and right
        elif op == "||":
            return left or right
        else:
            raise ValueError(f"Operator necunoscut: {op}")

    def constant_folding(self, instructions):
        optimized = []

        binary_pattern = re.compile(
            r"^(t\d+)\s*=\s*(\S+)\s*(\+|\-|\*|\/|%|==|!=|<|>|<=|>=|&&|\|\|)\s*(\S+)$"
        )
        unary_pattern = re.compile(r"^(t\d+)\s*=\s*(!|-)(\S+)$")

        for instr in instructions:
            m = binary_pattern.match(instr)
            if m:
                target, left, op, right = m.groups()

                if (self.is_number(left) or self.is_bool(left)) and (self.is_number(right) or self.is_bool(right)):
                    left_val = self.parse_literal(left)
                    right_val = self.parse_literal(right)

                    try:
                        result = self.eval_binary(left_val, op, right_val)
                        optimized.append(f"{target} = {self.format_literal(result)}")
                        continue
                    except Exception:
                        pass

            m = unary_pattern.match(instr)
            if m:
                target, op, operand = m.groups()

                if self.is_number(operand) or self.is_bool(operand):
                    val = self.parse_literal(operand)

                    try:
                        if op == "!":
                            result = not val
                        elif op == "-":
                            result = -val
                        else:
                            raise ValueError()

                        optimized.append(f"{target} = {self.format_literal(result)}")
                        continue
                    except Exception:
                        pass

            optimized.append(instr)

        return optimized

    def remove_redundant_assignments(self, instructions):
        optimized = []
        previous = None

        for instr in instructions:
            if instr == previous:
                continue
            optimized.append(instr)
            previous = instr

        return optimized