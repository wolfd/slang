from typing import List, Mapping

from . import parser
from . import ast
from . import token

class Interpreter:
    def __init__(self, path):
        super().__init__()
        self.path = path

        self.parser = parser.Parser(path)

        self.func_declarations: Mapping[str, ast.FuncDecl] = {}

    def eval_expr(self, expr):
        if isinstance(expr, ast.BasicLiteral):
            basic: ast.BasicLiteral = expr
            if basic.kind == token.Token.STRING:
                return basic.value[1:-1]  # get rid of quotes around string
            # other conditions go here, but we only have string literals now
        raise RuntimeError("Don't know how to evaluate {}".format(expr))

    def eval_print_stmt(self, stmt: ast.PrintStmt):
        print(self.eval_expr(stmt.expr))

    def eval_statement(self, stmt: ast.Stmt):
        if isinstance(stmt, ast.PrintStmt):
            print_stmt: ast.PrintStmt = stmt
            self.eval_print_stmt(print_stmt)

    def run_func(self, name: str):
        func = self.func_declarations[name]
        for statement in func.body.statements:
            self.eval_statement(statement)

    def run(self):
        file: ast.File = self.parser.parse_file()

        for declaration in file.declarations:
            if isinstance(declaration, ast.FuncDecl):
                func: ast.FuncDecl = declaration
                if func.name.name in self.func_declarations:
                    raise RuntimeError("Repeat declaration of {}".format(func.name.name))
                self.func_declarations[func.name.name] = func

        if "main" in self.func_declarations:
            self.run_func("main")

if __name__ == "__main__":
    import os.path
    my_interpreter = Interpreter(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test/main.sl"
    ))
    my_interpreter.run()
