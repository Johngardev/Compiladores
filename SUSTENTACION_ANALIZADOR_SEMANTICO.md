# Sustentación: Analizador Semántico con PLY

## 1. INTRODUCCIÓN

### ¿Qué es el Análisis Semántico?
El análisis semántico es la fase del compilador que verifica que el programa tenga **sentido** más allá de la sintaxis correcta. Mientras el análisis sintáctico verifica la estructura, el análisis semántico verifica:

- ✅ **Declaración de variables** antes de su uso
- ✅ **Compatibilidad de tipos** en operaciones y asignaciones
- ✅ **Manejo de ámbitos** (scopes)
- ✅ **Detección de errores semánticos**

---

## 2. COMPONENTES PRINCIPALES

### 2.1 Tabla de Símbolos (`symbol_table.py`)

La tabla de símbolos es el **corazón del análisis semántico**. Almacena información sobre las variables declaradas.

#### Clase `Symbol`
```python
class Symbol:
    def __init__(self, name, type):
        self.name = name  # Nombre de la variable
        self.type = type  # Tipo: 'int' o 'float'
```

#### Clase `ScopedSymbolTable`
Maneja múltiples ámbitos usando una **pila de diccionarios**:

```python
self.scopes = [{}]  # Pila: [global, local1, local2, ...]
```

**Operaciones clave:**

1. **`push_scope()`**: Crear nuevo ámbito (al entrar a un bloque `{}`)
2. **`pop_scope()`**: Eliminar ámbito actual (al salir del bloque)
3. **`add(symbol)`**: Agregar variable al ámbito actual
4. **`lookup(name)`**: Buscar variable (desde ámbito actual hasta global)

---

### 2.2 Manejo de Ámbitos en el Parser

#### Ejemplo de código con ámbitos:
```c
int a;          // Ámbito global
{
    int b;      // Ámbito local 1
    a = 5;      // ✅ 'a' existe en global
    b = 10;     // ✅ 'b' existe en local
}
b = 20;         // ❌ ERROR: 'b' no existe aquí
```

#### Implementación en el Parser:
```python
def p_block(p):
    '''block : LBRACE scope_enter statements RBRACE'''
    symbol_table.pop_scope()  # Salir del ámbito

def p_scope_enter(p):
    '''scope_enter :'''  # Producción vacía
    symbol_table.push_scope()  # Entrar a nuevo ámbito
```

**Truco importante:** Usamos una producción vacía (`scope_enter`) para ejecutar la acción semántica **antes** de procesar los statements.

---

## 3. ACCIONES SEMÁNTICAS

### 3.1 Declaración de Variables

```python
def p_declaration(p):
    '''declaration : type ID_list SEMICOLON'''
    var_type = p[1]      # 'int' o 'float'
    var_list = p[2]      # ['x', 'y', 'z']
    
    for var_name in var_list:
        try:
            symbol = Symbol(var_name, var_type)
            symbol_table.add(symbol)  # Agregar a tabla
        except SemanticError as e:
            print(f"Error: {e}")
```

**Ejemplo:**
```c
int x, y, z;  // Declara 3 variables de tipo int
```

**Validación semántica:**
- ❌ No se puede declarar la misma variable dos veces en el mismo ámbito
- ✅ Se pueden declarar variables con el mismo nombre en ámbitos diferentes

---

### 3.2 Asignaciones

```python
def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    var_name = p[1]
    expr_info = p[3]  # {'type': 'float', 'place': 't1'}
    
    try:
        # 1. ¿Existe la variable?
        symbol = symbol_table.lookup(var_name)
        
        # 2. ¿Los tipos son compatibles?
        if symbol.type == 'int' and expr_info['type'] == 'float':
            print(f"Error: No se puede asignar FLOAT a INT '{var_name}'")
        
        # 3. Generar código (lo omitiremos por ahora)
        # gen.emit('=', expr_info['place'], None, var_name)
        
    except SemanticError as e:
        print(e)
```

**Validaciones:**
1. ✅ Variable debe estar declarada antes de usarse
2. ✅ Tipos compatibles: `int = int`, `float = float`, `float = int`
3. ❌ Incompatible: `int = float` (pérdida de precisión)

---

### 3.3 Verificación de Tipos en Expresiones

```python
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    
    left = p[1]   # {'type': 'int', 'place': 'a'}
    op = p[2]     # '+'
    right = p[3]  # {'type': 'float', 'place': 'x'}
    
    # Inferencia de tipos
    result_type = 'int'
    if left['type'] == 'float' or right['type'] == 'float':
        result_type = 'float'  # int + float = float
    
    # Propagamos el tipo hacia arriba
    p[0] = {'type': result_type, 'place': 'temp'}
```

**Reglas de tipos:**
- `int + int = int`
- `int + float = float`
- `float + float = float`

---

### 3.4 Uso de Variables en Expresiones

```python
def p_factor_id(p):
    '''factor : ID'''
    var_name = p[1]
    try:
        symbol = symbol_table.lookup(var_name)  # Buscar variable
        p[0] = {'type': symbol.type, 'place': var_name}
    except SemanticError as e:
        print(e)
        p[0] = {'type': 'error', 'place': 'ERROR'}  # Valor dummy
```

**Validación:** La variable debe estar declarada antes de usarse.

---

## 4. EJEMPLOS DE DETECCIÓN DE ERRORES

### ❌ Error 1: Variable no declarada
```c
a = 10;  // Error: 'a' no está declarada
```
**Salida:**
```
Semantic Error: the Variable 'a' is not declared.
```

---

### ❌ Error 2: Variable duplicada en mismo ámbito
```c
int x;
int x;  // Error: 'x' ya fue declarada
```
**Salida:**
```
Semantic Error: Symbol 'x' already declared in the current scope.
```

---

### ❌ Error 3: Variable fuera de ámbito
```c
{
    int temp;
}
temp = 5;  // Error: 'temp' solo existe dentro del bloque
```

---

### ❌ Error 4: Incompatibilidad de tipos
```c
int a;
a = 3.14;  // Error: No se puede asignar float a int
```
**Salida:**
```
Error Semántico: No se puede asignar FLOAT a la variable INT 'a'
```

---

## 5. EJEMPLO COMPLETO DE EJECUCIÓN

### Código fuente:
```c
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
```

### Salida del compilador:
```
Symbol table initialized with global scope.
--- INICIO DEL ANÁLISIS ---
Added symbol: a of type int to current scope.
Added symbol: b of type int to current scope.
Added symbol: c of type int to current scope.
Added symbol: x of type float to current scope.
--- Entered new scope ---
Added symbol: temp of type int to current scope.
--- Exited scope ---
Analysis sintactic and semantic completed successfully.
```

---

## 6. INTEGRACIÓN CON PLY

### 6.1 Estructura General
```python
import ply.yacc as yacc
from lexer import tokens
from symbol_table import ScopedSymbolTable, Symbol, SemanticError

# Crear tabla de símbolos
symbol_table = ScopedSymbolTable()

# Reglas gramaticales con acciones semánticas
def p_declaration(p):
    '''declaration : type ID_list SEMICOLON'''
    # Acción semántica aquí
    ...

# Construir el parser
parser = yacc.yacc()
```

### 6.2 Ventajas de PLY
- ✅ Fácil integración de acciones semánticas en las reglas
- ✅ Manejo automático de precedencia y asociatividad
- ✅ Excelente para prototipos académicos
- ✅ Sintaxis clara y pythónica

---

## 7. PUNTOS CLAVE PARA LA SUSTENTACIÓN

### 🎯 Conceptos fundamentales:
1. **Diferencia entre sintaxis y semántica**
2. **Tabla de símbolos y su estructura**
3. **Manejo de ámbitos (scoping)**
4. **Verificación de tipos**
5. **Propagación de información (sintetización de atributos)**

### 🎯 Aspectos técnicos:
1. **Pila de ámbitos** para manejar bloques anidados
2. **Diccionarios** para almacenar símbolos en cada ámbito
3. **Búsqueda de símbolos** desde ámbito local al global
4. **Propagación de tipos** en expresiones usando `p[0]`

### 🎯 Decisiones de diseño:
1. **¿Por qué una pila de diccionarios?** → Permite búsqueda eficiente y manejo de ámbitos anidados
2. **¿Por qué producción vacía para scope_enter?** → Para ejecutar la acción semántica en el momento preciso
3. **¿Por qué diccionarios con 'type' y 'place'?** → Para propagar información de tipos y preparar generación de código

---

## 8. DEMOSTRACIÓN PRÁCTICA

### Caso de prueba 1: ✅ Programa correcto
```c
int a, b;
a = 10;
b = a + 5;
```

### Caso de prueba 2: ❌ Variable no declarada
```c
a = 10;  // Error
int a;
```

### Caso de prueba 3: ❌ Tipo incompatible
```c
int x;
x = 3.14;  // Error
```

### Caso de prueba 4: ✅ Ámbitos anidados
```c
int x;
{
    int x;  // ✅ Diferente ámbito
    x = 5;
}
x = 10;
```

---

## 9. CONCLUSIONES

### ✨ Logros del analizador semántico:
- ✅ Detecta errores que el análisis sintáctico no puede capturar
- ✅ Implementa tabla de símbolos con soporte para múltiples ámbitos
- ✅ Verifica compatibilidad de tipos
- ✅ Proporciona mensajes de error claros y útiles

### 🚀 Extensiones futuras:
- Soporte para funciones y parámetros
- Tipos de datos más complejos (arrays, structs)
- Conversiones implícitas de tipos
- Análisis de flujo de control

---

## 10. PREGUNTAS FRECUENTES

**P: ¿Cuál es la diferencia entre error sintáctico y semántico?**
- **Sintáctico:** `int x y;` (falta coma)
- **Semántico:** `x = 5;` (x no declarada)

**P: ¿Por qué usamos una pila de diccionarios?**
- Para manejar ámbitos anidados y permitir redeclaración en diferentes niveles

**P: ¿Qué pasa si no se hace pop_scope?**
- Las variables locales seguirían "vivas" y podrían usarse fuera de su ámbito

**P: ¿Cómo se propagan los tipos en expresiones?**
- Usando `p[0]` para retornar un diccionario con información de tipo

---

## REFERENCIAS

- **PLY Documentation:** https://www.dabeaz.com/ply/
- **Compilers: Principles, Techniques, and Tools** (Dragon Book)
- **Modern Compiler Implementation** (Tiger Book)
