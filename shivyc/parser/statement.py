"""Parser logic that parses statement nodes."""

import shivyc.token_kinds as token_kinds
import shivyc.tree.general_nodes as general_nodes
import shivyc.parser.utils as p

from shivyc.parser.declaration import parse_declaration
from shivyc.parser.expression import parse_expression
from shivyc.parser.utils import (add_range, log_error, match_token, token_is,
                                 ParserError)
from shivyc.tree import (Return, Break, Continue, IfStatement, WhileStatement,
                         ForStatement)


@add_range
def parse_statement(index):
    """Parse a statement.

    Try each possible type of statement, catching/logging exceptions upon
    parse failures. On the last try, raise the exception on to the caller.

    """
    for func in (parse_compound_statement, parse_return, parse_break,
                 parse_continue, parse_if_statement, parse_while_statement,
                 parse_for_statement):
        with log_error():
            return func(index)

    return parse_expr_statement(index)


@add_range
def parse_compound_statement(index):
    """Parse a compound statement.

    A compound statement is a collection of several
    statements/declarations, enclosed in braces.

    """
    p.symbols.new_scope()
    index = match_token(index, token_kinds.open_brack, ParserError.GOT)

    # Read block items (statements/declarations) until there are no more.
    items = []
    while True:
        with log_error():
            item, index = parse_statement(index)
            items.append(item)
            continue

        with log_error():
            item, index = parse_declaration(index)
            items.append(item)
            continue

        break

    index = match_token(index, token_kinds.close_brack, ParserError.GOT)
    p.symbols.end_scope()

    return general_nodes.Compound(items), index


@add_range
def parse_return(index):
    """Parse a return statement.

    Ex: return 5;

    """
    pass


@add_range
def parse_break(index):
    """Parse a break statement."""
    pass


@add_range
def parse_continue(index):
    """Parse a continue statement."""
    pass


@add_range
def parse_if_statement(index):
    """Parse an if statement."""
    pass


@add_range
def parse_while_statement(index):
    """Parse a while statement."""
    pass


@add_range
def parse_for_statement(index):
    """Parse a for statement."""
    pass


def _get_for_clauses(index):
    """Get the three clauses of a for-statement.

    index - Index of the beginning of the first clause.

    returns - Tuple (Node, Node, Node, index). Each Node is the corresponding
    clause, or None if that clause is empty The index is that of first token
    after the close paren terminating the for clauses.

    Raises exception on malformed input.
    """
    pass


def _get_first_for_clause(index):
    """Get the first clause of a for-statement.

    index - Index of the beginning of the first clause in the for-statement.
    returns - Tuple. First element is a node if a clause is found and None if
    there is no clause (i.e. semicolon terminating the clause). Second element
    is an integer index where the next token begins.

    If malformed, raises exception.

    """
    pass


@add_range
def parse_expr_statement(index):
    """Parse a statement that is an expression.

    Ex: a = 3 + 4

    """
    if token_is(index, token_kinds.semicolon):
        return general_nodes.EmptyStatement(), index + 1

    node, index = parse_expression(index)
    index = match_token(index, token_kinds.semicolon, ParserError.AFTER)
    return general_nodes.ExprStatement(node), index
