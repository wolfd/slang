from __future__ import annotations
from typing import List, Mapping

class Decl:
    pass

class Ident:
    def __init__(self, name_pos: int, name: str):
        super().__init__()
        self.name_pos = name_pos
        self.name = name

class Stmt:
    def __init__(self):
        super().__init__()

class BlockStmt:
    def __init__(self, lbrace: int, statements: List[Stmt], rbrace: int):
        super().__init__()
        self.lbrace = lbrace
        self.statements = statements
        self.rbrace = rbrace

class PrintStmt:
    def __init__(self, p: int, expr: Expr, eol: int):
        super().__init__()
        self.p = p
        self.expr = expr
        self.eol = eol

class Node(object):
    def __init__(self):
        pass

    def pos(self):
        raise NotImplementedError("Must define a pos")

    def end(self):
        raise NotImplementedError("Must define an end")

class Expr:
    def __init__(self):
        super().__init__()

class FuncDecl:
    def __init__(self, pos: int, name: Ident, body: BlockStmt):
        super().__init__()
        self.pos = pos
        self.name = name
        self.body = body

    def pos(self):
        return self.pos

class Scope:
    def __init__(self, outer: Scope):
        self.outer = outer
        self.objects: Mapping[string, Object] = {}

    def lookup(self, name: str) -> Object:
        return self.objects.get(name)

    def insert(self, obj: Object) -> Object:
        """
        tries to insert an object into a scope, if scope already
        has an object with the same name, it returns the already
        existing one, else None
        """
        if obj.name in self.objects:
            return self.objects[obj.name]
        self.objects[obj.name] = obj
        return None

class Object:
    def __init__(self, name: str):
        self.name: str = name

class File:
    def __init__(self, declarations: List[Decl]):
        self.declarations = declarations
