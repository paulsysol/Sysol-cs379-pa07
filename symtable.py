"""
PA 4: The USILang Symbol Table -- starter.

Complete Environment and check_program below. See
PA_04_The_USILang_Symbol_Table.md, Part B, for the full requirements.
"""

from typing import Optional

from parser import Assignment, BinOp, Declaration, Number, Program, Variable


class SemanticError(Exception):
    pass


class Environment:
    def __init__(self, parent: Optional["Environment"] = None) -> None:
        self.parent = parent
        self._names: dict = {}  # name -> declaration line, THIS scope only

    def define(self, name: str, line: int) -> None:
        """
        Store name -> line in THIS scope. Raise SemanticError if `name`
        is already defined in THIS scope (not a parent scope --
        shadowing a parent name is allowed).
        """
        if self._names.get(name) is None:
           self._names[name] = line
        else:
           raise SemanticError(f"Duplicate declaration '{name}' at line {line}, previously declared at line {self._names[name]}.")

    def resolve(self, name: str) -> int:
        """
        Look up `name` in this scope, then climb `parent` links.
        Return the declaration line, or raise SemanticError if not
        found anywhere in the chain.
        """
        if self._names.get(name) is None:
            if self.parent is None:
                raise SemanticError(f"Variable '{name}' is undefined.")
            else:
                return self.parent.resolve(name)
        else:
           return self._names[name]

    def check_statement(self, node):
        if isinstance(node, Declaration):
            self.check_statement(node.expr)
            self.define(node.name, node.line)
        elif isinstance(node, Assignment):
            self.resolve(node.name)
            self.check_statement(node.expr)
        elif isinstance(node, Variable):
            self.resolve(node.name)
        elif isinstance(node, BinOp):
            self.check_statement(node.left)
            self.check_statement(node.right)


def check_program(ast: Program) -> Environment:
    """
    Walk `ast.statements` in order, using one top-level Environment.
    For a Declaration: resolve every Variable in its expr BEFORE
    defining the new name (so `let x = x;` fails as use-before-decl).
    For an Assignment: resolve the assigned-to name, then resolve
    every Variable in its expr. Errors must surface at the first
    offending statement, not be collected and reported together.
    """
    env = Environment()
    for statement in ast.statements:
        env.check_statement(statement)
    return env
