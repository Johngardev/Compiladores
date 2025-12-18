import ply.lex as lex

tokens = (
  'ID', 'INT_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL', 'CHAR_LITERAL',
  'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
  'LPAREN', 'RPAREN', 'SEMICOLON', 'COMMA',
  'LBRACE', 'RBRACE', # Llaves para los ámbitos
  'LBRACKET', 'RBRACKET', # Corchetes para arrays
  # Operadores relacionales
  'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',
  # Operadores lógicos
  'AND', 'OR', 'NOT',
  # Operadores de incremento/decremento
  'PLUSPLUS', 'MINUSMINUS',
  # Operador de dirección y puntero
  'AMPERSAND', 'COLON', 'DOT',
  # Directivas de preprocesador
  'INCLUDE', 'DEFINE',
  # Tipos de datos
  'INT', 'FLOAT', 'CHAR', 'BOOLEAN', 'VOID',
  # Palabras reservadas de control
  'IF', 'ELSE', 'WHILE', 'FOR', 'SWITCH', 'CASE', 'DEFAULT', 'BREAK', 'RETURN',
  # Valores booleanos
  'TRUE', 'FALSE'
)

reserved = {
  'int': 'INT',
  'float': 'FLOAT',
  'char': 'CHAR',
  'boolean': 'BOOLEAN',
  'void': 'VOID',
  'if': 'IF',
  'else': 'ELSE',
  'while': 'WHILE',
  'for': 'FOR',
  'switch': 'SWITCH',
  'case': 'CASE',
  'default': 'DEFAULT',
  'break': 'BREAK',
  'return': 'RETURN',
  'true': 'TRUE',
  'false': 'FALSE'
}

t_ignore = ' \t'

# Comentarios de una línea y multilínea
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass  # Ignorar comentarios

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass  # Ignorar comentarios

# Directivas de preprocesador
def t_INCLUDE(t):
    r'\#include'
    return t

def t_DEFINE(t):
    r'\#define'
    return t

# Operadores relacionales (deben ir antes que los simples)
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'

# Operadores lógicos
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

# Operadores de incremento/decremento
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

# Operadores aritméticos
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='

# Delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_AMPERSAND = r'&'
t_COLON = r':'
t_DOT = r'\.'

# Literales (deben ir antes de ID para que los números no se confundan con identificadores)
def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1]  # Quitar las comillas
    return t

def t_CHAR_LITERAL(t):
    r"'([^'\\\n]|\\.)'"
    t.value = t.value[1:-1]  # Quitar las comillas simples
    return t

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z0-9_]*'
  t.type = reserved.get(t.value, 'ID')  # Check for reserved words
  return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()