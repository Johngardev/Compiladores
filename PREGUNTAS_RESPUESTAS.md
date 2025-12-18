# Preguntas y Respuestas Frecuentes - Sustentación

## 📚 PREGUNTAS CONCEPTUALES

### P1: ¿Cuál es la diferencia entre análisis sintáctico y semántico?

**R:** El análisis sintáctico verifica que el programa tenga la **estructura correcta** según la gramática (como verificar que una oración tenga sujeto y predicado). El análisis semántico verifica que el programa tenga **sentido lógico** (como verificar que el sujeto concuerde en número con el verbo).

**Ejemplo:**
- **Sintáctico:** `int x y;` ❌ (falta coma - error de estructura)
- **Semántico:** `int x; y = 5;` ❌ (`y` no está declarada - error de lógica)

---

### P2: ¿Por qué es necesaria una tabla de símbolos?

**R:** La tabla de símbolos es necesaria porque:
1. **Almacena información** sobre las variables declaradas (nombre, tipo)
2. **Permite verificar** si una variable existe antes de usarla
3. **Mantiene el contexto** de ámbitos (global, local)
4. **Facilita la generación de código** al tener toda la información en un lugar

Sin ella, no podríamos detectar errores como usar variables no declaradas.

---

### P3: ¿Qué son los ámbitos (scopes) y por qué son importantes?

**R:** Un ámbito define la **región del código donde una variable es visible y accesible**. Son importantes porque:

1. **Encapsulación:** Variables locales no contaminan el espacio global
2. **Reutilización de nombres:** Puedes usar el mismo nombre en diferentes bloques
3. **Control de acceso:** Variables temporales solo existen donde se necesitan
4. **Gestión de memoria:** Variables locales se liberan al salir del ámbito

**Ejemplo:**
```c
int x = 10;        // x global
{
    int x = 20;    // x local (diferente de la global)
    // Aquí x = 20
}
// Aquí x = 10
```

---

### P4: ¿Cómo funciona el shadowing (ocultamiento)?

**R:** El shadowing ocurre cuando una variable local **oculta temporalmente** una variable con el mismo nombre en un ámbito exterior. La búsqueda va desde el ámbito más interno hacia afuera, por lo que la primera coincidencia "gana".

```c
int x = 10;
{
    int x = 20;    // Esta x oculta la global
    print(x);      // Imprime 20
}
print(x);          // Imprime 10 (la global nunca cambió)
```

---

## 🔧 PREGUNTAS TÉCNICAS DE IMPLEMENTACIÓN

### P5: ¿Por qué usas una pila de diccionarios para la tabla de símbolos?

**R:** La pila de diccionarios es ideal porque:

1. **Pila:** Modelo natural para ámbitos anidados
   - `push_scope()` al entrar a un bloque
   - `pop_scope()` al salir
   - LIFO (Last In First Out) coincide con la estructura de bloques

2. **Diccionarios en cada nivel:**
   - Búsqueda rápida O(1) en cada ámbito
   - Detección inmediata de duplicados en el mismo nivel
   - Fácil agregar/eliminar símbolos

**Estructura:**
```python
scopes = [
    {x: Symbol, z: Symbol},    # Global
    {temp: Symbol},            # Local 1
    {y: Symbol}                # Local 2 (actual)
]
```

---

### P6: ¿Cómo implementas la búsqueda de símbolos (lookup)?

**R:** La búsqueda va desde el ámbito actual hasta el global:

```python
def lookup(self, name):
    # Recorrer desde el final (actual) hasta el inicio (global)
    for scope in reversed(self.scopes):
        if name in scope:
            return scope[name]  # Encontrado
    # Si llegamos aquí, no existe
    raise SemanticError(f"Variable '{name}' is not declared")
```

**Ventaja:** Implementa naturalmente el shadowing - la primera coincidencia es la del ámbito más cercano.

---

### P7: ¿Por qué usas una producción vacía para `scope_enter`?

**R:** Necesitamos ejecutar `push_scope()` **ANTES** de procesar los statements del bloque, pero **DESPUÉS** de leer la llave `{`.

```python
def p_block(p):
    '''block : LBRACE scope_enter statements RBRACE'''
    symbol_table.pop_scope()  # Después de statements

def p_scope_enter(p):
    '''scope_enter :'''  # Producción vacía
    symbol_table.push_scope()  # Antes de statements
```

**Timeline:**
1. Parser lee `LBRACE`
2. Parser reduce `scope_enter` → ejecuta `push_scope()`
3. Parser procesa `statements`
4. Parser lee `RBRACE` → ejecuta `pop_scope()`

Sin la producción vacía, no podríamos controlar el timing exacto.

---

### P8: ¿Cómo propagas la información de tipos en expresiones?

**R:** Uso **atributos sintetizados** - los valores fluyen de abajo hacia arriba en el árbol:

```python
def p_expression_binop(p):
    '''expression : expression PLUS expression'''
    left = p[1]   # {'type': 'int', 'place': 'a'}
    right = p[3]  # {'type': 'float', 'place': 'b'}
    
    # Inferir tipo del resultado
    result_type = 'float' if ('float' in [left['type'], right['type']]) else 'int'
    
    # Propagar hacia arriba
    p[0] = {'type': result_type, 'place': 'temp'}
```

**Ventaja:** Cada nodo calcula su tipo basándose en sus hijos, y lo propaga hacia arriba automáticamente.

---

## 🎯 PREGUNTAS SOBRE VERIFICACIÓN DE TIPOS

### P9: ¿Cuáles son las reglas de compatibilidad de tipos?

**R:** Las reglas implementadas son:

**En operaciones:**
- `int OP int = int`
- `float OP float = float`
- `int OP float = float` (promoción)
- `float OP int = float` (promoción)

**En asignaciones:**
- `int = int` ✅
- `float = float` ✅
- `float = int` ✅ (promoción implícita segura)
- `int = float` ❌ (pérdida de precisión)

---

### P10: ¿Por qué no permites asignar float a int?

**R:** Porque habría **pérdida de información**:

```c
int x;
x = 3.14;  // ¿x = 3? ¿x = 3.14? ← Ambiguo y peligroso
```

En lenguajes reales:
- **C/Java:** Requieren cast explícito `x = (int)3.14;`
- **Python:** Permite pero el usuario debe ser consciente
- **Rust:** No permite, requiere conversión explícita

Nuestra decisión: **Rechazar** para evitar errores sutiles.

---

### P11: ¿Cómo manejas expresiones con tipos mixtos?

**R:** Aplicamos **promoción de tipos** - el tipo "más grande" prevalece:

```c
int a = 5;
float x = 3.14;
float result = a + x;  // int promovido a float
```

**Algoritmo:**
```python
if left_type == 'float' OR right_type == 'float':
    result_type = 'float'
else:
    result_type = 'int'
```

Esto es seguro porque:
- `int → float`: No hay pérdida de información
- El resultado se almacena en una variable del tipo correcto

---

## 🚨 PREGUNTAS SOBRE MANEJO DE ERRORES

### P12: ¿Qué tipos de errores semánticos detecta tu analizador?

**R:** Detecta 4 tipos principales:

1. **Variable no declarada**
   ```c
   x = 5;  // x no existe
   ```

2. **Variable duplicada en mismo ámbito**
   ```c
   int x;
   int x;  // Error
   ```

3. **Incompatibilidad de tipos**
   ```c
   int x;
   x = 3.14;  // float → int
   ```

4. **Variable fuera de ámbito**
   ```c
   { int temp; }
   temp = 5;  // temp ya no existe
   ```

---

### P13: ¿Por qué lanzas excepciones vs retornar códigos de error?

**R:** Uso `SemanticError` (excepción personalizada) porque:

**Ventajas:**
- ✅ Más limpio - no contamina el flujo normal
- ✅ Fácil propagar - no necesito verificar cada operación
- ✅ Centralizado - manejo en un solo lugar con `try/except`
- ✅ Pythónico - idiomático en Python

**Ejemplo:**
```python
try:
    symbol = symbol_table.lookup('x')
except SemanticError as e:
    print(f"Error: {e}")
    # Continuar con análisis o abortar según necesidad
```

---

### P14: ¿Qué pasa si hay un error semántico? ¿Se detiene el compilador?

**R:** En la implementación actual, se **reporta el error pero continúa el análisis**:

```python
try:
    symbol_table.add(symbol)
except SemanticError as e:
    print(f"Error: {e}")  # Reportar
    # Continuar analizando
```

**Ventajas:**
- Encuentra múltiples errores en una sola pasada
- Usuario ve todos los problemas, no solo el primero

**Mejora posible:**
- Modo "strict" que aborta al primer error
- Contador de errores para decidir si generar código o no

---

## 🔄 PREGUNTAS SOBRE INTEGRACIÓN CON PLY

### P15: ¿Cómo se integra el análisis semántico con PLY?

**R:** PLY permite ejecutar **acciones semánticas** dentro de las reglas gramaticales:

```python
def p_declaration(p):
    '''declaration : type ID_list SEMICOLON'''
    # ↓ Acción semántica ejecutada automáticamente
    var_type = p[1]
    for var_name in p[2]:
        symbol_table.add(Symbol(var_name, var_type))
```

**Flujo:**
1. Parser reconoce patrón gramatical
2. Ejecuta función asociada (`p_declaration`)
3. Acción semántica se ejecuta en contexto
4. Valores accesibles vía `p[1]`, `p[2]`, etc.

---

### P16: ¿Qué es `p[0]` y para qué sirve?

**R:** `p[0]` es el **valor de retorno** de la regla - lo que esta producción "sintetiza" hacia arriba:

```python
def p_expression_binop(p):
    '''expression : expression PLUS expression'''
    result = compute(p[1], p[3])
    p[0] = result  # Este valor estará disponible en p[1] o p[3] de la regla padre
```

**Uso:** Propagar información (tipos, valores temporales, etc.) hacia reglas superiores.

---

## 🚀 PREGUNTAS SOBRE EXTENSIONES Y MEJORAS

### P17: ¿Qué funcionalidades adicionales podrías agregar?

**R:** Extensiones naturales:

1. **Funciones:**
   - Tabla de símbolos para funciones
   - Verificación de parámetros
   - Tipos de retorno

2. **Arrays:**
   - Verificación de índices
   - Tipos de elementos

3. **Estructuras (structs):**
   - Verificación de campos
   - Acceso a miembros

4. **Conversiones explícitas:**
   - Casts: `(int)3.14`
   - Validación de conversiones permitidas

5. **Constantes:**
   - Verificar que no se modifiquen
   - `const int x = 10;`

---

### P18: ¿Cómo agregarías soporte para funciones?

**R:** Necesitaría:

1. **Nueva clase `FunctionSymbol`:**
   ```python
   class FunctionSymbol:
       def __init__(self, name, return_type, parameters):
           self.name = name
           self.return_type = return_type
           self.parameters = parameters  # Lista de tipos
   ```

2. **Tabla de funciones separada:**
   - Funciones son globales (o usar ámbitos especiales)

3. **Verificación de llamadas:**
   ```python
   def p_function_call(p):
       func = function_table.lookup(p[1])
       verify_arguments(func.parameters, p[3])
       p[0] = {'type': func.return_type}
   ```

---

### P19: ¿Qué optimizaciones podrías hacer?

**R:**

1. **Tabla de símbolos:**
   - Hash table para búsqueda O(1) global
   - Cache de últimas búsquedas

2. **Verificación de tipos:**
   - Pre-computar tabla de compatibilidad
   - Evitar verificaciones redundantes

3. **Manejo de errores:**
   - Recovery: seguir analizando después de error
   - Sugerir correcciones automáticas

---

## 💡 PREGUNTAS SOBRE DECISIONES DE DISEÑO

### P20: ¿Por qué no implementaste el generador de código completo?

**R:** Razones pedagógicas:

1. **Enfoque:** La sustentación es sobre análisis **semántico**
2. **Separación de conceptos:** Cada fase debe entenderse independientemente
3. **Complejidad:** Generación de código es un tema completo en sí mismo
4. **Preparación:** Las estructuras (`{'type': ..., 'place': ...}`) ya preparan para codegen

**Nota:** La parte de generación ya está parcialmente implementada, solo la estamos omitiendo en la demostración.

---

### P21: ¿Por qué solo soportas int y float?

**R:** Decisión práctica para el prototipo:

**Ventajas:**
- ✅ Suficiente para demostrar conceptos
- ✅ Permite mostrar promoción de tipos
- ✅ Simplifica la implementación inicial

**En producción agregaría:**
- `bool`, `char`, `string`
- Arrays y punteros
- Tipos definidos por usuario

---

### P22: ¿Cómo manejarías referencias circulares?

**R:** En este compilador simple no tenemos estructuras que puedan crear referencias circulares, pero si las hubiera:

```python
class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.visited = False  # Flag para detección de ciclos

def check_circular(symbol, path=[]):
    if symbol.visited:
        raise SemanticError(f"Circular reference: {' -> '.join(path)}")
    symbol.visited = True
    # Procesar
    symbol.visited = False
```

---

## 🎓 PREGUNTAS TEÓRICAS AVANZADAS

### P23: ¿Qué son los atributos heredados vs sintetizados?

**R:**

**Atributos Sintetizados:** Fluyen hacia **ARRIBA** (bottom-up)
```
    expr₀
    ↑ type='float'
   / \
expr₁ expr₂
int   float
```
**Uso:** Propagación de tipos, valores calculados

**Atributos Heredados:** Fluyen hacia **ABAJO** (top-down)
```
declaration
type='int' ↓
   / | \
  x  y  z
```
**Uso:** Contexto desde padre, tipos esperados

**En este proyecto:** Solo usamos sintetizados porque PLY favorece bottom-up (LALR parser).

---

### P24: ¿Cuál es la complejidad computacional de tu analizador?

**R:**

- **lookup:** O(n) donde n = número de ámbitos (típicamente pequeño)
- **add:** O(1) - inserción en diccionario
- **push_scope/pop_scope:** O(1) - operaciones de lista
- **Análisis completo:** O(m) donde m = tamaño del programa

**Optimización posible:** Hash table global con prefijos de ámbito para O(1) global.

---

### P25: ¿Cómo se relaciona con la teoría de compiladores?

**R:** Este analizador implementa conceptos clave:

1. **Traducción dirigida por sintaxis (Syntax-Directed Translation)**
   - Acciones semánticas en reglas gramaticales

2. **Gramática atributada**
   - Atributos (tipos) asociados a símbolos gramaticales

3. **Tabla de símbolos clásica**
   - Estructura de datos fundamental en compiladores

4. **Análisis contextual**
   - Verificaciones que requieren contexto (declaraciones previas)

5. **Sistema de tipos simple**
   - Verificación estática de tipos

---

## 🎯 CONSEJOS PARA RESPONDER

### Estrategia general:

1. **Entender la pregunta:** Tómate un momento antes de responder
2. **Respuesta directa primero:** Da la respuesta concisa
3. **Explicación con ejemplo:** Ilustra con código
4. **Conexión teórica:** Si aplica, menciona el concepto teórico
5. **Admite limitaciones:** Si algo no está implementado, explica por qué

### Frases útiles:

- "En este prototipo implementé... pero en producción agregaría..."
- "La ventaja de este enfoque es... aunque también se podría..."
- "Esta decisión se basa en... del libro Dragon/Tiger/Purple Dragon"
- "PLY facilita esto porque..."

### Si no sabes algo:

- ✅ "No implementé eso en este proyecto, pero se podría hacer con..."
- ✅ "Esa es una buena pregunta, una forma sería..."
- ❌ NO inventes o improvises respuestas técnicas incorrectas

---

## 📚 RECURSOS PARA PROFUNDIZAR

- **Libro:** "Compilers: Principles, Techniques, and Tools" (Dragon Book)
- **PLY:** https://www.dabeaz.com/ply/
- **Teoría de tipos:** Type systems, type inference
- **Ámbitos:** Lexical vs dynamic scoping

---

**¡Prepárate bien y confía en tu trabajo! Has implementado un analizador semántico funcional.** 🎓✨
