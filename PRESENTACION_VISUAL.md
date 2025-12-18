# Presentación Visual: Analizador Semántico

## 🎯 FLUJO DEL ANÁLISIS SEMÁNTICO

```
┌─────────────────────────────────────────────────────────────────┐
│                     CÓDIGO FUENTE                               │
│                     "int x; x = 5;"                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ANÁLISIS LÉXICO (Lexer)                        │
│    Tokens: [INT, ID('x'), SEMICOLON, ID('x'), ASSIGN, ...]     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│               ANÁLISIS SINTÁCTICO (Parser)                      │
│              Construye árbol de sintaxis                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│         ⭐ ANÁLISIS SEMÁNTICO ⭐                                 │
│  • Verifica declaraciones                                       │
│  • Verifica tipos                                               │
│  • Maneja ámbitos                                               │
│  • Actualiza tabla de símbolos                                  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│            GENERACIÓN DE CÓDIGO (Omitido)                       │
│                    t1 = 5                                       │
│                    x = t1                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 ESTRUCTURA DE LA TABLA DE SÍMBOLOS

### Concepto de Pila de Ámbitos

```
        PILA DE ÁMBITOS
    ┌──────────────────┐
    │  Ámbito Local 2  │  ← Tope (ámbito actual)
    │  {'y': int}      │
    ├──────────────────┤
    │  Ámbito Local 1  │
    │  {'temp': int}   │
    ├──────────────────┤
    │  Ámbito Global   │
    │  {'x': int,      │
    │   'z': float}    │
    └──────────────────┘
```

### Operaciones de la Tabla

```
┌─────────────────────────────────────────────────────────────┐
│  OPERACIÓN         │  ACCIÓN                                │
├─────────────────────────────────────────────────────────────┤
│  push_scope()      │  Agrega nuevo diccionario al tope     │
│  pop_scope()       │  Elimina diccionario del tope         │
│  add(symbol)       │  Agrega símbolo al ámbito actual      │
│  lookup(name)      │  Busca de tope a base (local→global)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 ALGORITMO DE BÚSQUEDA (lookup)

```
def lookup(name):
    for scope in reversed(scopes):  # Del tope a la base
        if name in scope:
            return scope[name]      # ✅ Encontrado
    raise SemanticError             # ❌ No encontrado
```

### Ejemplo Visual de Búsqueda

```
Buscando 'temp':

┌──────────────────┐
│ Local 2: {}      │  ❌ No está aquí
├──────────────────┤
│ Local 1:         │  ✅ ¡Encontrado!
│ {'temp': int}    │     Retorna Symbol('temp', 'int')
├──────────────────┤
│ Global:          │  (No se busca más)
│ {'x': int}       │
└──────────────────┘
```

---

## 🎭 CICLO DE VIDA DE UN ÁMBITO

```
Código:               Estado de la Pila:

int x;                [global: {x: int}]
                            ↓
{                     [global: {x: int}, local1: {}]
                      push_scope() ↑
                            ↓
    int y;            [global: {x: int}, local1: {y: int}]
                            ↓
    y = x + 5;        ✅ Ambos símbolos son accesibles
                            ↓
}                     [global: {x: int}]
                      pop_scope() ↑
                            ↓
y = 10;               ❌ Error: 'y' no está en tabla
```

---

## 🔢 PROPAGACIÓN DE TIPOS

### Árbol de Expresión: `a + b * c`

```
            expression
           /    |    \
          /     +     \
         /             \
    expression      expression
        |           /   |   \
        a          /    *    \
                  /           \
             expression    expression
                 |             |
                 b             c
```

### Propagación Bottom-Up

```
Paso 1: b → {'type': 'int', 'place': 'b'}
Paso 2: c → {'type': 'int', 'place': 'c'}
Paso 3: b * c → {'type': 'int', 'place': 't1'}
Paso 4: a → {'type': 'int', 'place': 'a'}
Paso 5: a + t1 → {'type': 'int', 'place': 't2'}
```

---

## ⚖️ REGLAS DE COMPATIBILIDAD DE TIPOS

```
┌─────────────────────────────────────────────────────────────┐
│           OPERACIÓN          │  RESULTADO                   │
├─────────────────────────────────────────────────────────────┤
│  int OP int                  │  int                         │
│  float OP float              │  float                       │
│  int OP float                │  float (promoción)           │
│  float OP int                │  float (promoción)           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│         ASIGNACIÓN           │  VÁLIDO                      │
├─────────────────────────────────────────────────────────────┤
│  int = int                   │  ✅ Sí                       │
│  float = float               │  ✅ Sí                       │
│  float = int                 │  ✅ Sí (promoción implícita) │
│  int = float                 │  ❌ No (pérdida de precisión)│
└─────────────────────────────────────────────────────────────┘
```

---

## 🎬 SECUENCIA DE ANÁLISIS DETALLADA

### Ejemplo: `int x; x = 5;`

```
FASE 1: DECLARACIÓN
┌──────────────────────────────────────────────────────────────┐
│ Regla: declaration : type ID_list SEMICOLON                 │
│                                                              │
│ p[1] = 'int'                                                 │
│ p[2] = ['x']                                                 │
│                                                              │
│ Acción Semántica:                                           │
│   symbol = Symbol('x', 'int')                               │
│   symbol_table.add(symbol)                                  │
│                                                              │
│ ✅ Tabla: global = {x: Symbol('x', 'int')}                  │
└──────────────────────────────────────────────────────────────┘

FASE 2: ASIGNACIÓN
┌──────────────────────────────────────────────────────────────┐
│ Regla: assignment : ID ASSIGN expression SEMICOLON          │
│                                                              │
│ p[1] = 'x'                                                   │
│ p[3] = {'type': 'int', 'place': '5'}                        │
│                                                              │
│ Acción Semántica:                                           │
│   1. symbol = symbol_table.lookup('x')  ✅ Encontrado       │
│   2. Verificar tipos: int = int  ✅ Compatible              │
│   3. [Generación de código omitida]                         │
│                                                              │
│ ✅ Asignación válida                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚨 TIPOS DE ERRORES SEMÁNTICOS

### 1. Variable No Declarada

```
Código:
  x = 5;  // x no declarada

Detección:
  symbol_table.lookup('x')
  → raise SemanticError("Variable 'x' is not declared")

┌─────────────────────────┐
│ ❌ ERROR SEMÁNTICO      │
│                         │
│ Variable 'x' no está    │
│ declarada               │
└─────────────────────────┘
```

### 2. Variable Duplicada

```
Código:
  int x;
  int x;  // Duplicada

Detección:
  if 'x' in current_scope:
      raise SemanticError("Symbol 'x' already declared")

┌─────────────────────────┐
│ ❌ ERROR SEMÁNTICO      │
│                         │
│ 'x' ya fue declarada    │
│ en este ámbito          │
└─────────────────────────┘
```

### 3. Incompatibilidad de Tipos

```
Código:
  int x;
  x = 3.14;  // float → int

Detección:
  if symbol.type == 'int' and expr_type == 'float':
      print("No se puede asignar FLOAT a INT")

┌─────────────────────────┐
│ ❌ ERROR SEMÁNTICO      │
│                         │
│ Tipos incompatibles:    │
│ int ≠ float             │
└─────────────────────────┘
```

### 4. Variable Fuera de Ámbito

```
Código:
  {
      int temp;
  }
  temp = 5;  // temp ya no existe

Estado después de }:
  [global: {}]  ← temp fue eliminado con pop_scope()

┌─────────────────────────┐
│ ❌ ERROR SEMÁNTICO      │
│                         │
│ Variable 'temp' no      │
│ accesible aquí          │
└─────────────────────────┘
```

---

## 🎯 COMPARACIÓN: SINTAXIS VS SEMÁNTICA

```
┌────────────────────────────────┬────────────────────────────────┐
│     ANÁLISIS SINTÁCTICO        │     ANÁLISIS SEMÁNTICO         │
├────────────────────────────────┼────────────────────────────────┤
│ ¿La estructura es correcta?    │ ¿El programa tiene sentido?    │
│                                │                                │
│ Ejemplo de error:              │ Ejemplo de error:              │
│   int x y;  ❌ (falta ,)       │   x = 5; ❌ (x no declarada)   │
│                                │                                │
│ Usa:                           │ Usa:                           │
│ • Gramática BNF                │ • Tabla de símbolos            │
│ • Árbol de sintaxis            │ • Reglas de tipos              │
│                                │ • Reglas de ámbito             │
│                                │                                │
│ Detecta:                       │ Detecta:                       │
│ • Tokens mal ordenados         │ • Variables no declaradas      │
│ • Paréntesis no balanceados    │ • Tipos incompatibles          │
│ • Sintaxis inválida            │ • Variables duplicadas         │
│                                │ • Acceso fuera de ámbito       │
└────────────────────────────────┴────────────────────────────────┘
```

---

## 🔧 INTEGRACIÓN CON PLY

### Estructura de una Regla con Acción Semántica

```python
def p_declaration(p):
    '''declaration : type ID_list SEMICOLON'''
    #      ↑            ↑     ↑        ↑
    #   Nombre      Gramática BNF
    
    var_type = p[1]  # ← Valor de 'type'
    var_list = p[2]  # ← Valor de 'ID_list'
    
    # ⚙️ ACCIÓN SEMÁNTICA
    for var_name in var_list:
        symbol = Symbol(var_name, var_type)
        symbol_table.add(symbol)  # ← Actualiza tabla
    
    # p[0] = resultado (opcional, si se sintetiza)
```

### Flujo en PLY

```
Entrada: "int x, y;"

       LEXER
         ↓
   [INT, ID, COMMA, ID, SEMICOLON]
         ↓
       PARSER (reconoce regla)
         ↓
   p_declaration() ejecuta
         ↓
   Acción Semántica
   • Crea Symbol('x', 'int')
   • Crea Symbol('y', 'int')
   • Agrega a tabla
         ↓
   ✅ Completado
```

---

## 💡 VENTAJAS DEL DISEÑO

```
┌─────────────────────────────────────────────────────────────┐
│  DECISIÓN                 │  VENTAJA                        │
├─────────────────────────────────────────────────────────────┤
│  Pila de diccionarios     │  • Búsqueda eficiente O(n)      │
│                           │  • Fácil manejo de anidamiento  │
│                           │  • Memoria se libera con pop    │
├─────────────────────────────────────────────────────────────┤
│  Diccionario por ámbito   │  • Detección rápida duplicados  │
│                           │  • Lookup O(1) en cada nivel    │
├─────────────────────────────────────────────────────────────┤
│  Propagación con p[0]     │  • Información fluye naturalmente│
│                           │  • Preparación para codegen     │
├─────────────────────────────────────────────────────────────┤
│  Producción vacía         │  • Control preciso de timing    │
│  (scope_enter)            │  • Acción antes de statements   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 CASOS DE USO AVANZADOS

### Shadowing (Ocultamiento)

```
int x = 10;           [global: {x: int}]
                             ↓
{                     [global: {x: int}, local: {}]
                             ↓
    int x = 20;       [global: {x: int}, local: {x: int}]
                      ↑
                      La 'x' local oculta la global
                             ↓
    x = 30;           Modifica la 'x' local
                             ↓
}                     [global: {x: int}]
                             ↓
print(x);             Imprime 10 (la global no cambió)
```

### Expresión Compleja con Tipos Mixtos

```
Expresión: a + b * 3.14

   a: int         b: int        3.14: float
    ↓             ↓              ↓
    int      +   (int * float)
    ↓             ↓
    int      +   float
    ↓
   float         ← Resultado final
```

---

## 🎓 CONCEPTOS TEÓRICOS

### Atributos Sintetizados

```
Los valores fluyen hacia ARRIBA en el árbol

        ┌─────────────────┐
        │   expression    │  ← Valor sintetizado
        │ {'type': 'float'}│    desde los hijos
        └─────────────────┘
              ↑   ↑
             /     \
    ┌────────┐   ┌────────┐
    │  int   │   │ float  │  ← Hojas
    └────────┘   └────────┘
```

### Gramática Atributada

```
expression → expression + expression
    
    expression₀.type = 
        if expression₁.type = float OR expression₂.type = float
        then float
        else int
```

---

## 🎬 TIMELINE DE EJECUCIÓN

```
t=0   Inicializar symbol_table
      ↓
t=1   Leer: "int x;"
      ↓
t=2   Lexer: [INT, ID('x'), SEMICOLON]
      ↓
t=3   Parser reconoce: declaration
      ↓
t=4   p_declaration() ejecuta
      ├─ Crear Symbol('x', 'int')
      ├─ symbol_table.add(symbol)
      └─ ✅ x agregada al ámbito global
      ↓
t=5   Leer: "x = 5;"
      ↓
t=6   Parser reconoce: assignment
      ↓
t=7   p_assignment() ejecuta
      ├─ symbol_table.lookup('x')  ✅ Existe
      ├─ Verificar tipos: int = int  ✅
      └─ [Código intermedio: x = 5]
      ↓
t=8   ✅ Análisis completado exitosamente
```

---

## 🎯 PUNTOS CLAVE PARA SUSTENTAR

### 1. ¿Por qué una pila?
- Modelo natural para ámbitos anidados
- LIFO matching con entrada/salida de bloques
- Eficiente para shadowing

### 2. ¿Cómo se garantiza el orden?
- Producción vacía ejecuta push ANTES
- Acción pop DESPUÉS de procesar statements
- Timing preciso garantizado por gramática

### 3. ¿Por qué diccionarios?
- Búsqueda rápida O(1)
- Detección inmediata de duplicados
- Estructura natural para key-value

### 4. ¿Cómo se propagan tipos?
- Atributos sintetizados
- Bottom-up en árbol de sintaxis
- Información empaquetada en diccionarios

---

## 📝 CHECKLIST PARA LA SUSTENTACIÓN

```
✅ Explicar diferencia sintaxis/semántica
✅ Mostrar estructura de tabla de símbolos
✅ Demostrar push_scope / pop_scope
✅ Ejecutar ejemplo correcto
✅ Ejecutar 3-4 ejemplos con errores
✅ Explicar propagación de tipos
✅ Mostrar código de una regla clave
✅ Responder preguntas sobre decisiones de diseño
✅ Mencionar posibles extensiones
```

---

**¡Buena suerte en tu sustentación! 🚀**
