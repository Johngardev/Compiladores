import ply.lex as lex

tokens = (
  'ID', 'INT_LITERAL', 'FLOAT_LITERAL',
  'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
  'LPAREN', 'RPAREN', 'SEMICOLON', 'COMMA',
  'LBRACE', 'RBRACE', # Llaves para los ámbitos
  # Tipos de datos
  'INT', 'FLOAT'
)

reserved = {
  'int': 'INT',
  'float': 'FLOAT'
}

t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_LBRACE = r'\{'
t_RBRACE = r'\}'

def t_ID(t):
  r'[a-zA-Z_][a-zA-Z0-9_]*'
  t.type = reserved.get(t.value, 'ID')  # Check for reserved words
  return t

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()