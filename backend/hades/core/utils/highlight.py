"""Defines string highlighting functions."""

# Third-party libary imports.
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.data import JsonLexer


def highlights(text: str):
    return highlight(
        code=text,
        lexer=JsonLexer(),
        formatter=Terminal256Formatter()
    )