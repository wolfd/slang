from typing import List

from . import ast
from . import token
from . import scanner


class SlangError(Exception):
    def __init__(self, offset: int, reason: str):
        super().__init__(f"Error at: {offset}: {reason}")


class Parser(object):
    def __init__(self, path: str):
        super().__init__()

        self.scanner = scanner.Scanner(path)
        self.file: token.File = self.scanner.file

        self.pos: int = None
        self.tok: token.Token = None
        self.literal: str = None

        self.expr_level: int = 0  # dream level
        self.top_scope: ast.Scope = None

        self.next()

    def next(self):
        self.pos, self.tok, self.literal = self.scanner.scan()

    def expect(self, tok: token.Token) -> int:
        pos = self.pos
        if self.tok != tok:
            raise SlangError(pos, "expected {}".format(tok.name))
        self.next()
        return pos

    def open_scope(self):
        self.top_scope = ast.Scope(self.top_scope)

    def close_scope(self):
        self.top_scope = self.top_scope.outer

    def parse_ident(self) -> ast.Ident:
        pos = self.pos
        name: str = None
        if self.tok == token.Token.IDENT:
            name = self.literal
            self.next()
        else:
            # TODO: is this reasonable behavior?
            raise SlangError(pos, "tried to parse ident, but didn't find IDENT")

        return ast.Ident(
            name_pos=pos,
            name=name
        )

    def parse_simple_statement(self):
        raise SlangError(self.pos, "not implemented, buddy")

    def parse_print_statement(self) -> ast.PrintStmt:
        raise SlangError(self.pos, "not implemented, buddy")

    def parse_statement(self) -> ast.Stmt:
        if token.starts_expression(self.tok):
            return self.parse_simple_statement()
        elif self.tok == token.Token.P:
            return self.parse_print_statement()  # yeah, screw you python 3
        else:
            raise SlangError(self.pos, "expected statement, found {}".format(self.tok))

    def parse_statement_list(self) -> List[ast.Stmt]:
        statements: List[ast.Stmt] = []
        while self.tok != token.Token.RBRACKET or self.tok != token.Token.EOF:
            statements.append(self.parse_statement())

        return statements

    def parse_body(self) -> ast.BlockStmt:
        lbrace = self.expect(token.Token.LBRACKET)
        self.expect(token.Token.EOL)  # always have to newline after opening a block
        # TODO: any sort of scope stuff
        statements = self.parse_statement_list()
        rbrace = self.expect(token.Token.RBRACKET)

        return ast.BlockStmt(
            lbrace=lbrace,
            statements=statements,
            rbrace=rbrace
        )

    def parse_function_declaration(self) -> ast.FuncDecl:
        f = self.expect(token.Token.F)
        ident = self.parse_ident()

        # TODO: parse as block statement like a normal {}
        if self.tok != token.Token.LBRACKET:  # TODO: rename to LBRACE
            raise SlangError(self.pos, "{ expected after function name")
        block = self.parse_body()

        return ast.FuncDecl(
            f=f,
            name=ident,
            body=block
        )

    def parse_declaration(self) -> ast.Decl:
        # we only support function declarations right now lol
        return self.parse_function_declaration()

    def parse_file(self) -> ast.File:
        self.open_scope()

        declarations: List[ast.Decl] = []
        while self.tok != token.Token.EOF:
            declarations.append(self.parse_declaration())

        self.close_scope()

        # TODO: resolve unresolved objects?

        return ast.File(
            declarations=declarations
        )

if __name__ == "__main__":
    my_parser = Parser("test/main.sl")
    my_parser.parse_file()
