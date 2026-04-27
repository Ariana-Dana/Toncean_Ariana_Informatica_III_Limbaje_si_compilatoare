import sys
import os
import subprocess

from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from ir import IRGenerator
from optimizer import Optimizer
from codegen import CodeGeneratorC


def ast_to_string(node, indent=0):
    lines = []
    prefix = "  " * indent

    if node is None:
        lines.append(prefix + "None")
        return "\n".join(lines)

    if isinstance(node, list):
        for item in node:
            lines.append(ast_to_string(item, indent))
        return "\n".join(lines)

    lines.append(prefix + node.__class__.__name__)

    for key, value in vars(node).items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            lines.append("  " * (indent + 1) + f"{key}: {value}")
        elif isinstance(value, list):
            lines.append("  " * (indent + 1) + f"{key}:")
            for item in value:
                lines.append(ast_to_string(item, indent + 2))
        else:
            lines.append("  " * (indent + 1) + f"{key}:")
            lines.append(ast_to_string(value, indent + 2))

    return "\n".join(lines)


def save_lines(path, items):
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(str(item) + "\n")


def try_build_executable(c_file, exe_file):
    try:
        result = subprocess.run(
            ["gcc", c_file, "-o", exe_file],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return None, "", "gcc nu a fost gasit in PATH."


def compile_file(source_file):
    if not os.path.exists(source_file):
        print(f"Eroare: fisierul '{source_file}' nu exista.")
        return

    with open(source_file, "r", encoding="utf-8") as f:
        code = f.read()

    os.makedirs("output", exist_ok=True)

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    ir_generator = IRGenerator()
    ir_code = ir_generator.generate(ast)

    optimizer = Optimizer(ir_code)
    optimized_code = optimizer.optimize()

    codegen = CodeGeneratorC(optimized_code)
    c_code = codegen.generate()

    save_lines("output/tokens.txt", tokens)

    with open("output/ast.txt", "w", encoding="utf-8") as f:
        f.write(ast_to_string(ast))

    save_lines("output/tac.txt", ir_code)
    save_lines("output/tac_optimized.txt", optimized_code)

    c_path = "output/output.c"
    with open(c_path, "w", encoding="utf-8") as f:
        f.write(c_code)

    print("Compilare MiniLang finalizata cu succes.")
    print(f"Fisier sursa: {source_file}")
    print("Fisiere generate:")
    print(" - output/tokens.txt")
    print(" - output/ast.txt")
    print(" - output/tac.txt")
    print(" - output/tac_optimized.txt")
    print(" - output/output.c")

    exe_name = "output/program.exe" if os.name == "nt" else "output/program"
    rc, out, err = try_build_executable(c_path, exe_name)

    print("\n[Build executabil]")
    if rc is None:
        print("Poti compila manual:")
        print(f"gcc {c_path} -o {exe_name}")
    elif rc == 0:
        print(f"Executabil generat cu succes: {exe_name}")
    else:
        print("Compilarea C a esuat.")
        if out.strip():
            print("\n[stdout]")
            print(out)
        if err.strip():
            print("\n[stderr]")
            print(err)


if __name__ == "__main__":
    source = "program.min"
    if len(sys.argv) > 1:
        source = sys.argv[1]

    try:
        compile_file(source)

    except LexerError as e:
        print(f"Eroare lexicala: {e}")
    except ParserError as e:
        print(f"Eroare sintactica: {e}")
    except SemanticError as e:
        print(f"Eroare semantica: {e}")
    except Exception as e:
        print(f"Eroare generala: {e}")