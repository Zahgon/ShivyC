"""Parser logic that parses expression nodes."""

import shivyc.parser.utils as p
import shivyc.token_kinds as token_kinds
import shivyc.tree as tree
import shivyc.tree.decl_nodes as decl_nodes
from shivyc.parser.utils import (add_range, match_token, token_is, ParserError,
                                 raise_error, log_error, token_in)


@add_range
def parse_expression(index):
    """Parse expression."""
    return parse_series(
        index, parse_assignment,
        {token_kinds.comma: tree.MultiExpr})


@add_range
def parse_assignment(index):
    """Parse an assignment expression."""

    # This is a slight departure from the official grammar. The standard
    # specifies that a program is syntactically correct only if the
    # left-hand side of an assignment expression is a unary expression. But,
    # to provide more helpful error messages, we permit the left side to be
    # any non-assignment expression.

    left, index = parse_conditional(index)

    if index < len(p.tokens):
        op = p.tokens[index]
        kind = op.kind
    else:
        op = None
        kind = None

    node_types = {token_kinds.equals: tree.Equals,
                  token_kinds.plusequals: tree.PlusEquals,
                  token_kinds.minusequals: tree.MinusEquals,
                  token_kinds.starequals: tree.StarEquals,
                  token_kinds.divequals: tree.DivEquals,
                  token_kinds.modequals: tree.ModEquals}

    if kind in node_types:
        right, index = parse_assignment(index + 1)
        return node_types[kind](left, right, op), index
    else:
        return left, index


@add_range
def parse_conditional(index):
    """Parse a conditional expression."""
    # TODO: Parse ternary operator
    return parse_logical_or(index)


@add_range
def parse_logical_or(index):
    """Parse logical or expression."""
    return parse_series(
        index, parse_logical_and,
        {token_kinds.bool_or: tree.BoolOr})


@add_range
def parse_logical_and(index):
    """Parse logical and expression."""
    pass


@add_range
def parse_equality(index):
    """Parse equality expression."""
    pass


@add_range
def parse_relational(index):
    """Parse relational expression."""
    pass


@add_range
def parse_bitwise(index):
    pass


@add_range
def parse_additive(index):
    """Parse additive expression."""
    pass


@add_range
def parse_multiplicative(index):
    """Parse multiplicative expression."""
    pass


@add_range
def parse_cast(index):
    """Parse cast expression."""
    pass


@add_range
def parse_unary(index):
    """Parse unary expression."""
    pass


@add_range
def parse_postfix(index):
    """Parse postfix expression."""
    pass


@add_range
def parse_primary(index):
    """Parse primary expression."""
    pass


def parse_series(index, parse_base, separators):
    """Parse a series of symbols joined together with given separator(s).

    index (int) - Index at which to start searching.
    parse_base (function) - A parse_* function that parses the base symbol.
    separators (Dict(TokenKind -> Node)) - The separators that join
    instances of the base symbol. Each separator corresponds to a Node,
    which is the Node produced to join two expressions connected with that
    separator.
    """
    cur, index = parse_base(index)
    while True:
        for s in separators:
            if token_is(index, s):
                break
        else:
            return cur, index

        tok = p.tokens[index]
        new, index = parse_base(index + 1)
        cur = separators[s](cur, new, tok)
