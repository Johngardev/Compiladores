# Modificaciones al Compilador para Soportar Código C Completo

## Resumen

Se realizaron modificaciones significativas al compilador para soportar código C con características avanzadas incluyendo:
- Directivas de preprocesador
- Comentarios
- Estructuras de control
- Funciones
- Punteros
- Tipos de datos adicionales

---

## 1. Modificaciones en el Lexer (lexer.py)

### Tokens Agregados:

#### Literales adicionales:
- `STRING_LITERAL`: Para cadenas de texto entre comillas dobles
- `CHAR_LITERAL`: Para caracteres entre comillas simples

#### Operadores relacionales y lógicos:
- `LT`, `GT`: Menor que, mayor que (`<`, `>`)
- `LE`, `GE`: Menor o igual, mayor o igual (`<=`, `>=`)
- `EQ`, `NE`: Igualdad, desigualdad (`==`, `!=`)
- `AND`, `OR`, `NOT`: Operadores lógicos (`&&`, `||`, `!`)

#### Operadores de incremento/decremento:
- `PLUSPLUS`, `MINUSMINUS`: Incremento y decremento (`++`, `--`)

#### Operadores de punteros:
- `AMPERSAND`: Operador de dirección (`&`)
- `TIMES`: Ya existía para multiplicación, ahora también sirve para punteros (`*`)

#### Delimitadores adicionales:
- `DOT`: Punto (`.`) para extensiones de archivo (ej: `stdio.h`)
- `COLON`: Dos puntos (`:`) para casos en switch
- `LBRACKET`, `RBRACKET`: Corchetes para arrays (definidos pero no usados aún)

#### Tipos de datos nuevos:
- `CHAR`: Para tipo char
- `BOOLEAN`: Para tipo boolean
- `VOID`: Para funciones sin retorno

#### Palabras reservadas de control de flujo:
- `IF`, `ELSE`: Condicionales
- `WHILE`: Bucle while
- `FOR`: Bucle for
- `SWITCH`, `CASE`, `DEFAULT`: Switch-case
- `BREAK`: Salir de bucle o switch
- `RETURN`: Retornar de función

#### Valores booleanos:
- `TRUE`, `FALSE`: Literales booleanos

#### Directivas de preprocesador:
- `INCLUDE`: Para `#include`
- `DEFINE`: Para `#define`

### Reglas Léxicas Importantes:

```python
# Comentarios (se ignoran)
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass
```

---

## 2. Modificaciones en el Parser (parser.py)

### Nuevas Reglas Gramaticales:

#### 2.1 Estructura del Programa
```python
program : declarations_and_functions
```
Ahora el programa puede contener declaraciones, funciones y directivas de preprocesador.

#### 2.2 Directivas de Preprocesador
```python
preprocessor : INCLUDE ID DOT ID      # #include stdio.h
             | INCLUDE ID             # #include stdio
             | DEFINE ID INT_LITERAL  # #define MAX 100
             | DEFINE ID FLOAT_LITERAL
```

#### 2.3 Definición de Funciones
```python
function_definition : type ID LPAREN parameter_list RPAREN compound_statement
                    | type ID LPAREN RPAREN compound_statement
```

Soporta funciones con y sin parámetros, con declaraciones de punteros en parámetros.

#### 2.4 Estructuras de Control

**IF-ELSE:**
```python
if_statement : IF LPAREN expression RPAREN statement
             | IF LPAREN expression RPAREN statement ELSE statement
```

**WHILE:**
```python
while_statement : WHILE LPAREN expression RPAREN statement
                | WHILE LPAREN expression RPAREN compound_statement
```

**FOR:**
```python
for_statement : FOR LPAREN for_init SEMICOLON expression_opt SEMICOLON for_update RPAREN statement
```

**SWITCH-CASE:**
```python
switch_statement : SWITCH LPAREN expression RPAREN LBRACE case_list RBRACE

case_clause : CASE INT_LITERAL COLON statements
            | DEFAULT COLON statements
```

**RETURN y BREAK:**
```python
return_statement : RETURN expression SEMICOLON
                 | RETURN SEMICOLON

break_statement : BREAK SEMICOLON
```

#### 2.5 Expresiones Mejoradas

**Operadores relacionales y lógicos:**
```python
expression : expression LT expression    # a < b
           | expression GT expression    # a > b
           | expression LE expression    # a <= b
           | expression GE expression    # a >= b
           | expression EQ expression    # a == b
           | expression NE expression    # a != b
           | expression AND expression   # a && b
           | expression OR expression    # a || b
```

**Operadores unarios:**
```python
expression : MINUS expression           # -a
           | NOT expression             # !a
           | AMPERSAND ID               # &p (dirección)
           | TIMES ID                   # *p (desreferencia)
           | PLUSPLUS ID                # ++a
           | MINUSMINUS ID              # --a
           | ID PLUSPLUS                # a++
           | ID MINUSMINUS              # a--
```

**Llamadas a funciones:**
```python
factor : ID LPAREN argument_list RPAREN    # func(a, b, c)
       | ID LPAREN RPAREN                  # func()
```

#### 2.6 Declaraciones con Punteros

```python
declarator : pointer_declarator ID ASSIGN expression    # *p = 10
           | pointer_declarator ID                      # *p
           | ID ASSIGN expression                       # x = 10
           | ID                                         # x

pointer_declarator : TIMES pointer_declarator           # **
                   | TIMES                              # *
```

Permite declaraciones como:
- `int *p` - puntero simple
- `int **u` - puntero doble
- `int *p, q, *r` - múltiples declaraciones

---

## 3. Análisis Semántico Implementado

### 3.1 Detección de Errores

El compilador detecta los siguientes errores semánticos:

1. **Redeclaración de variables:**
   ```
   Error: Semantic Error: Symbol 'q' already declared in the current scope.
   ```

2. **Variable no declarada:**
   ```
   Semantic Error: the Variable 'x' is not declared.
   ```

3. **Incompatibilidad de tipos:**
   ```
   Error Semántico: No se puede asignar FLOAT a la variable INT 'a'
   ```

### 3.2 Gestión de Ámbitos

- Ámbito global para variables y funciones globales
- Ámbito local para parámetros de funciones
- Ámbito de bloque para variables dentro de `{}`

---

## 4. Características Detectadas en el Código del Profesor

### ✅ Soportadas:

1. **Directivas de preprocesador:**
   - `#include stdio.h` ✓
   - `#define aktura 67.8` ✓

2. **Comentarios:**
   - `// este es un comentario` ✓
   - `/* comentario multilínea */` ✓

3. **Tipos de datos:**
   - `int`, `float`, `char`, `boolean` ✓

4. **Punteros:**
   - `int *p, **u` ✓
   - `char *z` ✓
   - `q=&p` (operador de dirección) ✓

5. **Estructuras de control:**
   - `if-else` ✓
   - `while` ✓
   - `for` ✓
   - `switch-case-default` ✓
   - `break` ✓
   - `return` ✓

6. **Funciones:**
   - Definición con parámetros ✓
   - Recursividad ✓
   - Llamadas a funciones ✓

7. **Operadores:**
   - Aritméticos: `+`, `-`, `*`, `/` ✓
   - Relacionales: `<`, `>`, `<=`, `>=`, `==`, `!=` ✓
   - Incremento/decremento: `++`, `--` ✓
   - Dirección: `&` ✓

### ⚠️ Errores Semánticos Detectados (normales en el código):

1. **Redeclaración de `q`:**
   ```c
   int p,q,*q, r=100, **u;  // 'q' se declara dos veces
   ```

2. **Redeclaración de `r`:**
   ```c
   int p,q,*q, r=100, **u;
   float r;  // 'r' ya fue declarado como int
   ```

3. **Incompatibilidad de tipos:**
   ```c
   case 2: a=c;  // 'a' es int, 'c' es float
   ```

---

## 5. Ejecución y Prueba

### Archivo de Prueba: `test_codigo_profesor.py`

```python
from lexer import lexer
from parser import parser

# Código del profesor...

parser.parse(codigo_profesor, lexer=lexer)
```

### Resultado:
```
✓ COMPILACIÓN EXITOSA
Analysis sintactic and semantic completed successfully.
```

### Salida del Análisis:

El compilador muestra:
- Todos los tokens reconocidos
- Directivas de preprocesador detectadas
- Estructuras de control identificadas
- Variables agregadas a la tabla de símbolos
- Errores semánticos encontrados
- Funciones definidas

---

## 6. Limitaciones Actuales

Aunque el compilador acepta el código, algunas características no están completamente implementadas:

1. **Arrays**: Tokens definidos pero no usados (`LBRACKET`, `RBRACKET`)
2. **Inicialización de variables**: Solo se reconoce sintácticamente
3. **Generación de código**: Básica, no genera código completo para todas las estructuras
4. **Validación de tipos completa**: No valida todos los casos de conversión de tipos
5. **Múltiples archivos**: No soporta compilación de múltiples archivos

---

## 7. Recomendaciones de Mejora

1. **Eliminar conflictos shift/reduce**: Mejorar la gramática para resolver ambigüedades
2. **Implementar arrays**: Agregar soporte completo para arreglos
3. **Mejorar análisis de tipos**: Implementar conversiones implícitas seguras
4. **Generación de código**: Completar la generación para todas las estructuras
5. **Optimización**: Agregar fase de optimización de código intermedio

---

## 8. Conclusión

El compilador ahora acepta correctamente el código C proporcionado por el profesor, reconociendo:
- ✅ Directivas de preprocesador
- ✅ Comentarios de una línea y multilínea
- ✅ Funciones con parámetros y recursividad
- ✅ Estructuras de control (if, while, for, switch)
- ✅ Punteros y operador de dirección
- ✅ Tipos de datos: int, float, char, boolean
- ✅ Operadores: aritméticos, relacionales, lógicos, incremento/decremento

El análisis semántico detecta correctamente errores como redeclaración de variables e incompatibilidad de tipos.
