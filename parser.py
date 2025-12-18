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
    '''program : declarations_and_functions'''
    print("Analysis sintactic and semantic completed successfully.")

def p_declarations_and_functions(p):
    '''declarations_and_functions : declarations_and_functions declaration_or_function
                                  | declaration_or_function
                                  | empty'''
    pass

def p_declaration_or_function(p):
    '''declaration_or_function : preprocessor
                                | function_definition
                                | declaration
                                | statement'''
    pass

# Directivas de preprocesador
def p_preprocessor(p):
    '''preprocessor : INCLUDE ID DOT ID
                    | INCLUDE ID
                    | INCLUDE LT ID DOT ID GT
                    | INCLUDE LT ID GT
                    | DEFINE ID INT_LITERAL
                    | DEFINE ID FLOAT_LITERAL'''
    print(f"Directiva de preprocesador: {p[1]}")

# Funciones
def p_function_definition(p):
    '''function_definition : type ID LPAREN parameter_list RPAREN compound_statement
                           | type ID LPAREN RPAREN compound_statement'''
    func_name = p[2]
    func_type = p[1]
    print(f"Definición de función: {func_name} de tipo {func_type}")
    symbol_table.pop_scope()  # Salir del ámbito de la función

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA parameter
                      | parameter'''
    pass

def p_parameter(p):
    '''parameter : type pointer_declarator ID
                 | type ID'''
    param_type = p[1]
    if len(p) == 3:
        param_name = p[2]
    else:
        param_name = p[3]
        param_type = p[1] + p[2]  # tipo + asteriscos
    
    try:
        symbol = Symbol(param_name, param_type)
        symbol_table.add(symbol)
    except SemanticError as e:
        print(f"Error: {e}")

def p_compound_statement(p):
    '''compound_statement : LBRACE scope_enter statements RBRACE'''
    pass

def p_statements(p):
    '''statements : statements statement
                  | empty'''
    pass

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | block
                 | if_statement
                 | while_statement
                 | for_statement
                 | switch_statement
                 | return_statement
                 | break_statement
                 | expression_statement'''
    pass

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON
                            | SEMICOLON'''
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
    for var_name, pointer_level, init_value in var_list:
        actual_type = var_type + pointer_level
        try:
            symbol = Symbol(var_name, actual_type)
            symbol_table.add(symbol)
        except SemanticError as e:
            print(f"Error: {e}")

# Estructuras de control
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    print("Estructura IF detectada")

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement
                       | WHILE LPAREN expression RPAREN compound_statement'''
    print("Estructura WHILE detectada")

def p_for_statement(p):
    '''for_statement : FOR LPAREN for_init SEMICOLON expression_opt SEMICOLON for_update RPAREN statement
                     | FOR LPAREN for_init SEMICOLON expression_opt SEMICOLON for_update RPAREN compound_statement'''
    print("Estructura FOR detectada")

def p_for_init(p):
    '''for_init : assignment_expr
                | empty'''
    pass

def p_for_update(p):
    '''for_update : assignment_expr
                  | unary_expr
                  | empty'''
    pass

def p_assignment_expr(p):
    '''assignment_expr : ID ASSIGN expression'''
    var_name = p[1]
    expr_info = p[3]
    try:
        symbol = symbol_table.lookup(var_name)
        if symbol.type == 'int' and expr_info['type'] == 'float':
            print(f"Error Semántico: No se puede asignar FLOAT a la variable INT '{var_name}'")
        gen.emit('=', expr_info['place'], None, var_name)
    except SemanticError as e:
        print(e)
    p[0] = expr_info

def p_unary_expr(p):
    '''unary_expr : ID PLUSPLUS
                  | ID MINUSMINUS
                  | PLUSPLUS ID
                  | MINUSMINUS ID'''
    p[0] = {'type': 'int', 'place': p[1] if p[1] in ['++', '--'] else p[2]}

def p_expression_opt(p):
    '''expression_opt : expression
                      | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None

def p_switch_statement(p):
    '''switch_statement : SWITCH LPAREN expression RPAREN LBRACE case_list RBRACE'''
    print("Estructura SWITCH detectada")

def p_case_list(p):
    '''case_list : case_list case_clause
                 | case_clause
                 | empty'''
    pass

def p_case_clause(p):
    '''case_clause : CASE INT_LITERAL COLON statements
                   | DEFAULT COLON statements'''
    pass

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    print("Sentencia RETURN detectada")

def p_break_statement(p):
    '''break_statement : BREAK SEMICOLON'''
    print("Sentencia BREAK detectada")

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | BOOLEAN
            | VOID'''
    p[0] = p[1] # 'int', 'float', 'char', 'boolean' o 'void'
    
def p_pointer_declarator(p):
    '''pointer_declarator : TIMES pointer_declarator
                          | TIMES'''
    if len(p) == 2:
        p[0] = '*'
    else:
        p[0] = '*' + p[2]
    
def p_ID_list(p):
    '''ID_list : ID_list COMMA declarator
               | declarator'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_declarator(p):
    '''declarator : pointer_declarator ID ASSIGN expression
                  | pointer_declarator ID
                  | ID ASSIGN expression
                  | ID'''
    if len(p) == 2:  # Solo ID
        p[0] = (p[1], '', None)
    elif len(p) == 3:  # pointer + ID
        p[0] = (p[2], p[1], None)
    elif len(p) == 4:  # ID = expr
        p[0] = (p[1], '', p[3])
    else:  # pointer + ID = expr
        p[0] = (p[2], p[1], p[4])

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
                  | expression DIVIDE expression
                  | expression LT expression
                  | expression GT expression
                  | expression LE expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NE expression
                  | expression AND expression
                  | expression OR expression'''
    
    left = p[1]  # Diccionario del operando izquierdo
    op = p[2]    # Operador (+, -, *, /, <, >, etc.)
    right = p[3] # Diccionario del operando derecho

    # A. Lógica de Tipos (Semántica)
    result_type = 'int'
    if op in ['<', '>', '<=', '>=', '==', '!=', '&&', '||']:
        result_type = 'boolean'  # Las comparaciones devuelven boolean
    elif left['type'] == 'float' or right['type'] == 'float':
        result_type = 'float'
    
    # B. Generación de Código
    temp = gen.new_temp() # Pedimos un temporal (ej: t1)
    gen.emit(op, left['place'], right['place'], temp) # Emitimos t1 = op1 + op2

    # C. Propagar resultado hacia arriba
    p[0] = {'type': result_type, 'place': temp}

def p_expression_unary(p):
    '''expression : MINUS expression
                  | NOT expression
                  | AMPERSAND ID
                  | TIMES ID
                  | PLUSPLUS ID
                  | MINUSMINUS ID
                  | ID PLUSPLUS
                  | ID MINUSMINUS'''
    if len(p) == 3:
        if p[1] == '-':
            temp = gen.new_temp()
            gen.emit('-', p[2]['place'], None, temp)
            p[0] = {'type': p[2]['type'], 'place': temp}
        elif p[1] == '!':
            temp = gen.new_temp()
            gen.emit('!', p[2]['place'], None, temp)
            p[0] = {'type': 'boolean', 'place': temp}
        elif p[1] == '&':
            p[0] = {'type': 'pointer', 'place': '&' + p[2]}
        elif p[1] == '*':
            try:
                symbol = symbol_table.lookup(p[2])
                p[0] = {'type': 'int', 'place': '*' + p[2]}
            except SemanticError as e:
                print(e)
                p[0] = {'type': 'error', 'place': 'ERROR'}
        elif p[1] in ['++', '--']:
            p[0] = {'type': 'int', 'place': p[2]}
        else:  # p[2] es ++ o --
            p[0] = {'type': 'int', 'place': p[1]}

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2] # Simplemente pasamos lo que está dentro del paréntesis

def p_expression_factor(p):
    '''expression : factor'''
    p[0] = p[1] # Propagamos el factor


def p_factor_num(p):
    '''factor : INT_LITERAL
              | FLOAT_LITERAL
              | CHAR_LITERAL
              | STRING_LITERAL
              | TRUE
              | FALSE'''
    if isinstance(p[1], int):
        p[0] = {'type': 'int', 'place': str(p[1])}
    elif isinstance(p[1], float):
        p[0] = {'type': 'float', 'place': str(p[1])}
    elif p[1] == 'true' or p[1] == 'false':
        p[0] = {'type': 'boolean', 'place': p[1]}
    else:
        p[0] = {'type': 'char', 'place': str(p[1])}

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

def p_factor_function_call(p):
    '''factor : ID LPAREN argument_list RPAREN
              | ID LPAREN RPAREN'''
    func_name = p[1]
    print(f"Llamada a función: {func_name}")
    p[0] = {'type': 'int', 'place': func_name}  # Asumimos retorno int por defecto

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    pass

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
    