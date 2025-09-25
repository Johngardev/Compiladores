import ply.yacc as yacc
from lexer import tokens
from lexer import lexer
from symbol_table import ScopedSymbolTable, Symbol, SemanticError

#--- Table Symbols with Scopes ---
symbol_table = ScopedSymbolTable()

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
    # ACCIÓN SEMÁNTICA: Añadir todas las variables de la lista a la tabla
    var_type = p[1]
    var_list = p[2]
    try:
        for var_name in var_list:
            symbol = Symbol(var_name, var_type)
            symbol_table.add(symbol)
    except SemanticError as e:
        print(e)

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
    expr_type = p[3]
    try:
        symbol = symbol_table.lookup(var_name)
        if symbol.type == 'int' and expr_type == 'float':
            raise SemanticError(f"Error Semántico: No se puede asignar un valor float a la variable int '{var_name}'.")
        print(f"Asignación válida a '{var_name}'")
    except SemanticError as e:
        print(e)

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''
    if len(p) == 2: # expression : term
        p[0] = p[1]
    else: # expression : expression OP term
        left_type = p[1]
        right_type = p[3]
        if left_type == 'float' or right_type == 'float':
            p[0] = 'float'
        else:
            p[0] = 'int'

def p_term(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor(p):
    '''factor : INT_LITERAL'''
    p[0] = 'int'
    
def p_factor_float(p):
    '''factor : FLOAT_LITERAL'''
    p[0] = 'float'

def p_factor_id(p):
    '''factor : ID'''
    try:
        symbol = symbol_table.lookup(p[1])
        p[0] = symbol.type
    except SemanticError as e:
        print(e)
        p[0] = 'error_type'

# --- Empty rule to lists of statements ---
def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Sintaxis error in '{p.value}' at line {p.lineno}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

# --- Función Principal para Probar ---
if __name__ == '__main__':
    code = """
    int x, global_var;
    float y;

    x = 10;
    
    {
        int y, z;
        float w;

        y = 5;
        global_var = 20;
        
        {
            int x;
            x = 99;
        }
        
        w = 1.1;
        // z = w;
    }

    // z = 15;
    y = 3.14;
    """

    parser.parse(code, lexer=lexer) # type: ignore
    
    print("\n--- PRUEBA CON ERROR SEMÁNTICO (VARIABLE NO DECLARADA) ---")
    symbol_table = ScopedSymbolTable() # Reiniciamos la tabla
    error_code = """
    int a;
    {
        int b;
        b = 1;
    }
    a = b;
    """
    parser.parse(error_code, lexer=lexer)