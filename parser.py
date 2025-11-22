import ply.yacc as yacc
from lexer import tokens
from lexer import lexer
from symbol_table import ScopedSymbolTable, Symbol, SemanticError
from code_gen import Codegenerator

#--- Table Symbols with Scopes ---
symbol_table = ScopedSymbolTable()
#--- Code Generator ---
gen = Codegenerator()

# --- PRECEDENCIA DE OPERADORES ---
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

#--- Grammar Rules and Semantic Actions ---
def p_program(p):
    '''program : statements'''
    print("Analysis sintactic and semantic completed successfully.")

def p_statements(p):
    '''statements : statements statement
                  | empty'''
    pass

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | block'''
    pass

# --- Management of scopes ---
def p_block(p):
    '''block : LBRACE scope_enter statements RBRACE'''
    # SEMANTIC ACTION: Exit scope
    symbol_table.pop_scope()
    print("--- Exited scope ---")

def p_scope_enter(p):
    '''scope_enter :''' # Empty production to semantic action
		# SEMANTIC ACTION: Enter new scope
    symbol_table.push_scope()
    print("--- Entered new scope ---")
    
#--- Declarations ---
def p_declaration(p):
    '''declaration : type ID_list SEMICOLON'''
    var_type = p[1]
    var_list = p[2] # Es una lista de nombres ['x', 'y']
    
    # Registramos cada variable en la tabla de símbolos
    for var_name in var_list:
        try:
            symbol = Symbol(var_name, var_type)
            symbol_table.add(symbol)
        except SemanticError as e:
            print(f"Error en línea {p.lineno(2)}: {e}")

def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1] # 'int' o 'float'
    
def p_ID_list(p):
    '''ID_list : ID_list COMMA ID
               | ID'''
    if len(p) == 2: # ID
        p[0] = [p[1]]
    else: # ID_list, ID
        p[0] = p[1] + [p[3]]

# --- Assignments & Expressions ---
def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    var_name = p[1]
    # p[3] es un diccionario: {'type': 'int', 'place': 't0'}
    expr_info = p[3] 

    try:
        # 1. Verificación Semántica: ¿Existe la variable?
        symbol = symbol_table.lookup(var_name)
        
        # 2. Verificación de Tipos
        if symbol.type == 'int' and expr_info['type'] == 'float':
            print(f"Error Semántico: No se puede asignar FLOAT a la variable INT '{var_name}'")
        
        # 3. Generación de Código: var = temporal
        gen.emit('=', expr_info['place'], None, var_name)
        
    except SemanticError as e:
        print(e)

# --- EXPRESIONES (Operaciones Aritméticas) ---
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    
    left = p[1]  # Diccionario del operando izquierdo
    op = p[2]    # Operador (+, -, *, /)
    right = p[3] # Diccionario del operando derecho

    # A. Lógica de Tipos (Semántica)
    result_type = 'int'
    if left['type'] == 'float' or right['type'] == 'float':
        result_type = 'float'
    
    # B. Generación de Código
    temp = gen.new_temp() # Pedimos un temporal (ej: t1)
    gen.emit(op, left['place'], right['place'], temp) # Emitimos t1 = op1 + op2

    # C. Propagar resultado hacia arriba
    p[0] = {'type': result_type, 'place': temp}

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2] # Simplemente pasamos lo que está dentro del paréntesis

def p_expression_factor(p):
    '''expression : factor'''
    p[0] = p[1] # Propagamos el factor


def p_factor_num(p):
    '''factor : INT_LITERAL
              | FLOAT_LITERAL'''
    if isinstance(p[1], int):
        p[0] = {'type': 'int', 'place': str(p[1])}
    else:
        p[0] = {'type': 'float', 'place': str(p[1])}

def p_factor_id(p):
    '''factor : ID'''
    var_name = p[1]
    try:
        symbol = symbol_table.lookup(var_name)
        p[0] = {'type': symbol.type, 'place': var_name}
    except SemanticError as e:
        print(e)
        # Retornamos un valor dummy para que no falle el compilador
        p[0] = {'type': 'error', 'place': 'ERROR'}

# --- Empty rule to lists of statements ---
def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Sintaxis error in '{p.value}' at line {p.lineno}")
    else:
        print("Syntax error at EOF")


#--- Build the parser ---
parser = yacc.yacc()

# --- Función Principal para Probar ---
if __name__ == '__main__':
    code = """
    int a, b, c;
    float x;
    
    a = 10;
    b = 20;
    
    {
        int temp;
        temp = a + b * 2; 
        x = temp + 0.5;
    }
    
    c = a + b;
    """

    print("--- CÓDIGO FUENTE ---")
    print(code)
    
    print("\n--- INICIO DEL ANÁLISIS ---")
    parser.parse(code, lexer=lexer)
    
    # Imprimir el código intermedio generado
    gen.print_code()
    