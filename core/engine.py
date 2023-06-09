import logging

from core.runtime import Runtime

tokens = ("NAME", "NUMBER", "OR", "AND")

literals = ["=", "+", "-", "*", "/", "(", ")", ","]
t_NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

t_OR = r"\|\|"  # ||
t_AND = r"\&\&"


def t_error(t):
    error_msg = f"Illegal character {t.value[0]} at line {t.lineno} pos {t.lexpos}"
    logging.error(error_msg)
    raise SyntaxErrorException(error_msg)


# Build the lexer
import ply.lex as lex

lexer = lex.lex()


class SyntaxErrorException(Exception):
    pass


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


# Build the lexer
import ply.lex as lex  # noqa: E402

lexer = lex.lex()

# Parsing rules

precedence = (
    ("left", "+", "-"),
    ("left", "*", "/"),
)


def p_expression_binop(p):
    """expression : expression '+' expression
    | expression '-' expression
    | expression '*' expression
    | expression '/' expression
    """
    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]


def p_expression_group(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_logic_analiser(p):
    """expression : expression OR expression
    | expression AND expression"""
    if p[2] == "||":
        p[0] = bool(p[1]) or bool(p[3])
    elif p[2] == "&&":
        p[0] = bool(p[1]) and bool(p[3])


def p_create_variable(p):
    """
    expression : NAME '=' expression
    """
    names[p[1]] = p[3]
    p[0] = p[3]


def p_get_value_from_variable(p):
    """
    expression : NAME
    """
    p[0] = names[p[1]]


def p_call_function(p):
    """
    expression : NAME '(' expression ')'
    """
    foo = runtime.get_function(p[1])
    p[0] = foo(p[3])


def p_error(p):
    msg = f"Syntax error at <{p.value}> pos: {p.lexer.lexpos}" if p else "Syntax error at EOF"

    logging.error(msg)
    raise SyntaxErrorException(msg)


import ply.yacc as yacc

parser = yacc.yacc()
runtime = Runtime()
names = {}
