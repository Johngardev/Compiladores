# Ejemplos de Prueba para Sustentación

## EJEMPLO 1: Programa Correcto con Ámbitos
```python
# test_ejemplo1.py
from parser import parser, gen
from lexer import lexer

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

print("=== EJEMPLO 1: PROGRAMA CORRECTO ===")
print(code)
print("\n--- ANÁLISIS ---")
parser.parse(code, lexer=lexer)
```

**Salida esperada:**
```
✅ Todas las variables se declaran antes de usar
✅ Los ámbitos se manejan correctamente
✅ Los tipos son compatibles
```

---

## EJEMPLO 2: Error - Variable no declarada
```python
code = """
a = 10;
int a;
"""

print("=== EJEMPLO 2: VARIABLE NO DECLARADA ===")
print(code)
print("\n--- ANÁLISIS ---")
parser.parse(code, lexer=lexer)
```

**Salida esperada:**
```
❌ Semantic Error: the Variable 'a' is not declared.
```

---

## EJEMPLO 3: Error - Variable duplicada
```python
code = """
int x;
int x;
"""

print("=== EJEMPLO 3: VARIABLE DUPLICADA ===")
print(code)
print("\n--- ANÁLISIS ---")
parser.parse(code, lexer=lexer)
```

**Salida esperada:**
```
❌ Semantic Error: Symbol 'x' already declared in the current scope.
```

---

## EJEMPLO 4: Error - Variable fuera de ámbito
```python
code = """
{
    int temp;
    temp = 5;
}
temp = 10;
"""

print("=== EJEMPLO 4: VARIABLE FUERA DE ÁMBITO ===")
print(code)
print("\n--- ANÁLISIS ---")
parser.parse(code, lexer=lexer)
```

**Salida esperada:**
```
❌ Semantic Error: the Variable 'temp' is not declared.
```

---

## EJEMPLO 5: Error - Incompatibilidad de tipos
```python
code = """
int numero;
numero = 3.14;
"""

print("=== EJEMPLO 5: INCOMPATIBILIDAD DE TIPOS ===")
print(code)
print("\n--- ANÁLISIS ---")
parser.parse(code, lexer=lexer)
```

**Salida esperada:**
```
❌ Error Semántico: No se puede asignar FLOAT a la variable INT 'numero'
```

---

## EJEMPLO 6: Ámbitos anidados correctos
```python
code = """
int x;
x = 10;

{
    int x;
    x = 20;
    {
        int x;
        x = 30;
    }
}
"""

print("=== EJEMPLO 6: ÁMBITOS ANIDADOS ===")
print(code)
print("\n--- ANÁLISIS ---")
parser.parse(code, lexer=lexer)
```

**Salida esperada:**
```
✅ Se permiten variables con el mismo nombre en diferentes ámbitos
✅ Cada declaración es válida en su respectivo ámbito
```

---

## EJEMPLO 7: Expresiones con tipos mixtos
```python
code = """
int a;
float x, y;

a = 10;
x = 3.14;
y = a + x;
"""

print("=== EJEMPLO 7: TIPOS MIXTOS EN EXPRESIONES ===")
print(code)
print("\n--- ANÁLISIS ---")
parser.parse(code, lexer=lexer)
```

**Salida esperada:**
```
✅ int + float = float
✅ Se permite asignar float a variable float
```

---

## EJEMPLO 8: Expresiones aritméticas complejas
```python
code = """
int a, b, c, d;
float resultado;

a = 5;
b = 10;
c = 3;

d = a + b * c;
resultado = (a + b) * c;
"""

print("=== EJEMPLO 8: EXPRESIONES COMPLEJAS ===")
print(code)
print("\n--- ANÁLISIS ---")
parser.parse(code, lexer=lexer)
```

**Salida esperada:**
```
✅ Precedencia de operadores respetada
✅ Propagación correcta de tipos
```

---

## SCRIPT COMPLETO DE DEMOSTRACIÓN

```python
# demo_sustentacion.py
"""
Script para demostrar el analizador semántico durante la sustentación
"""

from parser import parser, gen, symbol_table
from lexer import lexer

def reset_compiler():
    """Reinicia el estado del compilador entre pruebas"""
    global symbol_table, gen
    from symbol_table import ScopedSymbolTable
    from code_gen import Codegenerator
    symbol_table = ScopedSymbolTable()
    gen = Codegenerator()

def run_test(title, code, show_code_gen=False):
    """Ejecuta un caso de prueba"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)
    print("\n--- CÓDIGO FUENTE ---")
    print(code)
    print("\n--- ANÁLISIS ---")
    
    parser.parse(code, lexer=lexer)
    
    if show_code_gen:
        gen.print_code()
    
    print("\n" + "-"*60)
    input("Presiona ENTER para continuar...")
    reset_compiler()

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   DEMOSTRACIÓN: ANALIZADOR SEMÁNTICO CON PLY             ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Test 1: Programa correcto
    run_test(
        "TEST 1: Programa Correcto con Ámbitos",
        """
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
        """,
        show_code_gen=False
    )
    
    # Test 2: Variable no declarada
    run_test(
        "TEST 2: Error - Variable No Declarada",
        """
a = 10;
int a;
        """
    )
    
    # Test 3: Variable duplicada
    run_test(
        "TEST 3: Error - Variable Duplicada",
        """
int x;
int x;
        """
    )
    
    # Test 4: Variable fuera de ámbito
    run_test(
        "TEST 4: Error - Variable Fuera de Ámbito",
        """
{
    int temp;
    temp = 5;
}
temp = 10;
        """
    )
    
    # Test 5: Incompatibilidad de tipos
    run_test(
        "TEST 5: Error - Incompatibilidad de Tipos",
        """
int numero;
numero = 3.14;
        """
    )
    
    # Test 6: Ámbitos anidados
    run_test(
        "TEST 6: Ámbitos Anidados Correctos",
        """
int x;
x = 10;

{
    int x;
    x = 20;
    {
        int x;
        x = 30;
    }
}
        """
    )
    
    # Test 7: Tipos mixtos
    run_test(
        "TEST 7: Tipos Mixtos en Expresiones",
        """
int a;
float x, y;

a = 10;
x = 3.14;
y = a + x;
        """
    )
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              FIN DE LA DEMOSTRACIÓN                      ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
```

---

## CONSEJOS PARA LA SUSTENTACIÓN

### Durante la demostración:
1. **Ejecuta primero un ejemplo correcto** para mostrar que el compilador funciona
2. **Luego muestra los errores semánticos** uno por uno
3. **Explica qué está pasando** en cada línea del análisis
4. **Muestra el estado de la tabla de símbolos** después de cada declaración

### Puntos a enfatizar:
- La **búsqueda de símbolos** va desde el ámbito actual hasta el global
- Los **tipos se propagan** hacia arriba en el árbol de sintaxis
- Los **ámbitos se gestionan** con push/pop en momentos específicos
- Los **errores se reportan** de forma clara y útil

### Preguntas que pueden hacerte:
- **¿Qué pasa si declaras una variable global y luego una local con el mismo nombre?**
  → La local "oculta" (shadowing) a la global en ese ámbito
  
- **¿Cómo manejas las expresiones con tipos diferentes?**
  → Promoción de tipo: int + float = float
  
- **¿Por qué usas una producción vacía para scope_enter?**
  → Para ejecutar la acción semántica antes de procesar los statements

- **¿Qué mejoras harías al analizador?**
  → Funciones, arrays, structs, conversiones implícitas, warnings vs errores
