"""
PA 3: The USILang Parser -- starter.

Complete the parsing functions below. AST node types are already
defined -- do not modify them. See the assignment,
Part B, for the full requirements.
"""

from dataclasses import dataclass, field
from typing import List

from lexer import Token, tokenize


@dataclass
class Program:
    statements: list


@dataclass
class Declaration:
    name: str
    expr: object
    line: int


@dataclass
class Assignment:
    name: str
    expr: object
    line: int


@dataclass
class BinOp:
    op: str
    left: object
    right: object
    line: int


@dataclass
class Number:
    value: int
    line: int


@dataclass
class Variable:
    name: str
    line: int


class ParseError(Exception):
    pass


class _ParserState:
    """Given: a small cursor wrapper over the token list. Not required to use, but handy."""

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_: str) -> Token:
        tok = self.peek()
        if tok.type != type_:
            raise ParseError(f"Line {tok.line}: expected {type_}, found {tok.type} ({tok.lexeme!r}).")
        return self.advance()

def parse_factor(state: _ParserState):
    # TODO
    if state.peek().type == "LPAREN":
        state.advance()
        node = parse_expr(state)
        state.expect("RPAREN")
        return node
    elif state.peek().type == "MINUS":
        node = BinOp(op_tok.lexeme, Number(0,op_tok.line), parse_expr(state), op_tok.line)
        return node
    elif state.peek().type == "NUMBER":
        op_tok = state.advance()
        return Number(int(op_tok.lexeme), op_tok.line)
    elif state.peek().type == "IDENT":
        op_tok = state.advance()
        return Variable(op_tok.lexeme, op_tok.line)
    elif state.peek().type == "SEMI":
        op_tok = state.advance()
        raise ParseError(f"Missing semicolon on Line {op_tok.line}.")

    raise NotImplementedError

def parse_term(state: _ParserState):
    # TODO
    node = parse_factor(state)
    while state.peek().type in ("STAR", "SLASH"):
        op_tok = state.advance()
        right = parse_factor(state)
        node = BinOp(op_tok.lexeme, node, right, op_tok.line)
    return node

def parse_expr(state: _ParserState):
    # TODO
    node = parse_term(state)
    while state.peek().type in ("PLUS", "MINUS"):
        op_tok = state.advance()
        right = parse_term(state)
        node = BinOp(op_tok.lexeme, node, right, op_tok.line)
    return node

def parse_declaration(state: _ParserState) -> Declaration:
    # TODO
    op_tok = state.expect("IDENT")
    state.expect("ASSIGN")
    return Declaration(op_tok.lexeme, parse_expr(state), op_tok.line)

def parse_assignment(state: _ParserState) -> Assignment:
    # TODO
    op_tok = state.expect("IDENT")
    state.expect("ASSIGN")
    return Assignment(op_tok.lexeme, parse_expr(state), op_tok.line)

def parse_statement(state: _ParserState):
    # TODO: peek at state.peek().type to choose declaration vs. assignment
    if state.peek().type == "LET":
        state.advance()
        node = parse_declaration(state)
    else:
        node = parse_assignment(state)
    state.expect("SEMI")
    return node

def parse_program(state: _ParserState) -> Program:
    # TODO: loop parse_statement() until EOF
    program = Program(statements=[])
    while state.peek().type != "EOF":
        program.statements.append(parse_statement(state))
    return program

def parse(tokens: List[Token]) -> Program:
    state = _ParserState(tokens)
    return parse_program(state)
