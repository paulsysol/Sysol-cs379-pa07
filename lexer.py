"""
PA 2: The USILang Lexer -- starter.

Complete tokenize() below. See the assignment, Part B,
for the full requirements. Must use a single compiled master regex
with named groups -- not a hand-rolled character-by-character loop.
"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    type: str
    lexeme: str
    line: int


class LexError(Exception):
    pass

KEYWORDS = {"let"}

# TODO: build your master regex here, e.g.:
# _MASTER_RE = re.compile(r"(?P<NUMBER>\d+)|(?P<IDENT>[A-Za-z_]\w*)|...")
_MASTER_RE = re.compile(
    r"(?P<NUMBER>[0-9]+(\.[0-9]+)?)"
    r"|(?P<IDENT>[a-zA-Z_][a-zA-Z0-9_]*)"
    r"|(?P<PLUS>\+)|(?P<MINUS>-)|(?P<STAR>\*)|(?P<SLASH>/)"
    r"|(?P<LPAREN>\()|(?P<RPAREN>\))|(?P<ASSIGN>=)|(?P<SEMI>;)"
    r"|(?P<COMMENT>#.*)|(?P<NEWLINE>\n)|(?P<SKIP>[ \t]+)|(?P<MISMATCH>.)"
)

def tokenize(source: str) -> List[Token]:
    """
    Convert `source` into a list of Token objects, ending in an EOF
    token with an empty lexeme. Recognize NUMBER, IDENT, LET, PLUS,
    MINUS, STAR, SLASH, LPAREN, RPAREN, ASSIGN, SEMI. Discard
    whitespace and '#'-prefixed comments without emitting tokens for
    them. Track 1-indexed line numbers. Raise LexError (with the
    offending character and line) on unrecognized input.
    """
    # TODO
def tokenize(source: str) -> list[Token]:
   tokens = []
   line = 1
   pos = 0
   while pos < len(source):
      m = _MASTER_RE.match(source, pos)
      kind, lexeme = m.lastgroup, m.group()
      if kind == "NEWLINE":
         line += 1
      elif kind in ("SKIP", "COMMENT"):
         pass
      elif kind == "MISMATCH":
         raise LexError(f"Unexpected char {lexeme!r} at line {line}")
      elif kind == "IDENT" and lexeme in KEYWORDS:
         tokens.append(Token("LET", lexeme, line))
      else:
         tokens.append(Token(kind, lexeme, line))
      pos = m.end()
   tokens.append(Token("EOF", "", line))
   return tokens
