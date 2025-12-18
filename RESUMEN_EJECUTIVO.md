# 📋 Resumen Ejecutivo - Sustentación Analizador Semántico

## 🎯 PUNTOS CLAVE (1 minuto)

- **Qué es:** Analizador semántico implementado con PLY (Python Lex-Yacc)
- **Qué hace:** Verifica que el programa tenga sentido (no solo sintaxis correcta)
- **Características principales:**
  - ✅ Tabla de símbolos con múltiples ámbitos
  - ✅ Verificación de tipos (int, float)
  - ✅ Detección de 4 tipos de errores semánticos
  - ✅ Soporte para bloques anidados

---

## 📊 ESTRUCTURA DEL PROYECTO

```
lexer.py           → Análisis léxico (tokens)
parser.py          → Análisis sintáctico + semántico
symbol_table.py    → Tabla de símbolos con ámbitos
code_gen.py        → Generación código (omitido en sustentación)
```

---

## 🔑 CONCEPTOS FUNDAMENTALES

### 1. Tabla de Símbolos
```python
Estructura: Pila de diccionarios
[{global symbols}, {local symbols}, ...]
```

### 2. Operaciones Principales
- `push_scope()` - Entrar a nuevo bloque
- `pop_scope()` - Salir de bloque
- `add(symbol)` - Agregar variable
- `lookup(name)` - Buscar variable

### 3. Tipos de Errores Detectados
1. Variable no declarada
2. Variable duplicada
3. Incompatibilidad de tipos
4. Variable fuera de ámbito

---

## 💻 CÓDIGO CLAVE PARA EXPLICAR

### Declaración de Variables
```python
def p_declaration(p):
    '''declaration : type ID_list SEMICOLON'''
    var_type = p[1]
    for var_name in p[2]:
        symbol = Symbol(var_name, var_type)
        symbol_table.add(symbol)
```

### Verificación de Tipos
```python
def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    symbol = symbol_table.lookup(p[1])  # ¿Existe?
    if symbol.type == 'int' and expr['type'] == 'float':
        print("Error: int = float")  # Incompatible
```

### Manejo de Ámbitos
```python
def p_block(p):
    '''block : LBRACE scope_enter statements RBRACE'''
    symbol_table.pop_scope()

def p_scope_enter(p):
    '''scope_enter :'''
    symbol_table.push_scope()
```

---

## 🎬 SECUENCIA DE DEMOSTRACIÓN

### 1. Introducción (2 min)
- Explicar diferencia sintaxis vs semántica
- Mostrar estructura de tabla de símbolos
- Mencionar herramientas (PLY)

### 2. Demo Programa Correcto (3 min)
```c
int a, b;
float x;
a = 10;
{
    int temp;
    temp = a + b;
}
```
- Mostrar salida con mensajes de ámbitos
- Explicar push/pop scope

### 3. Demo Errores (5 min)
**Error 1:** Variable no declarada
```c
a = 10;  // Error
```

**Error 2:** Variable duplicada
```c
int x;
int x;  // Error
```

**Error 3:** Tipo incompatible
```c
int x;
x = 3.14;  // Error
```

**Error 4:** Fuera de ámbito
```c
{ int temp; }
temp = 5;  // Error
```

### 4. Explicación Técnica (5 min)
- Mostrar código de `symbol_table.py`
- Explicar algoritmo de lookup
- Mostrar propagación de tipos
- Explicar producción vacía

### 5. Preguntas (5 min)

---

## 🎯 RESPUESTAS RÁPIDAS A PREGUNTAS COMUNES

**Q: ¿Diferencia sintaxis vs semántica?**
A: Sintaxis = estructura correcta. Semántica = tiene sentido.

**Q: ¿Por qué pila de diccionarios?**
A: Pila = ámbitos anidados. Diccionarios = búsqueda O(1).

**Q: ¿Cómo funciona lookup?**
A: Busca desde ámbito actual hasta global, primera coincidencia gana.

**Q: ¿Por qué producción vacía?**
A: Para ejecutar push_scope ANTES de procesar statements.

**Q: ¿Cómo se propagan tipos?**
A: Bottom-up, usando p[0] para retornar {'type': ..., 'place': ...}.

**Q: ¿Qué mejorarías?**
A: Funciones, arrays, más tipos, conversiones explícitas.

---

## 📝 CHECKLIST ANTES DE PRESENTAR

- [ ] Probar `python parser.py` (ejemplo por defecto)
- [ ] Probar `python demo_sustentacion.py` (todos los casos)
- [ ] Revisar `SUSTENTACION_ANALIZADOR_SEMANTICO.md`
- [ ] Repasar `PREGUNTAS_RESPUESTAS.md`
- [ ] Preparar editor con archivos clave abiertos
- [ ] Tener ejemplos de código listos para mostrar

---

## 🎓 ESTRUCTURA DE PRESENTACIÓN (20 min)

### Slide 1: Título (30 seg)
- Analizador Semántico con PLY
- Tu nombre

### Slide 2: Objetivos (1 min)
- Implementar análisis semántico
- Detectar errores más allá de sintaxis
- Usar PLY para integración

### Slide 3: Conceptos (2 min)
- ¿Qué es análisis semántico?
- Tabla de símbolos
- Ámbitos

### Slide 4: Arquitectura (2 min)
- Diagrama de flujo
- Componentes principales
- Decisiones de diseño

### Slide 5-8: Demostración en Vivo (10 min)
- Programa correcto
- 4 tipos de errores
- Explicar salida

### Slide 9: Aspectos Técnicos (3 min)
- Código key
- Algoritmos principales
- Integración con PLY

### Slide 10: Conclusiones (1 min)
- Logros
- Limitaciones
- Extensiones futuras

### Q&A (5 min)

---

## 💡 TIPS PARA LA PRESENTACIÓN

### Durante la Demo:
1. **Ejecuta código en vivo** - muestra que funciona
2. **Explica cada error** - no solo muestres, interpreta
3. **Usa el debugger mental** - "¿qué está pasando aquí?"
4. **Señala los mensajes** - haz que el público vea lo importante

### Al Explicar Código:
1. **Empieza simple** - una función a la vez
2. **Usa analogías** - "como una pila de platos"
3. **Dibuja diagramas** - visualiza la pila de ámbitos
4. **Da ejemplos concretos** - no solo teoría

### Si te hacen una pregunta difícil:
1. **Respira** - tómate un momento
2. **Reformula** - "Si entiendo bien, preguntas sobre..."
3. **Responde lo que sepas** - sé honesto sobre límites
4. **Relaciona con lo implementado** - vuelve a terreno conocido

---

## 🚀 SCRIPT DE INICIO

> "Buenos días/tardes. Hoy voy a presentar un **analizador semántico** implementado con PLY, una herramienta de Python para construcción de compiladores.
>
> El análisis semántico es la fase del compilador que verifica que el programa tenga **sentido**, más allá de tener la sintaxis correcta. Por ejemplo, detecta cuando intentamos usar una variable que no hemos declarado, o cuando asignamos un tipo incompatible.
>
> Mi implementación tiene tres componentes principales:
> 1. Una **tabla de símbolos** con soporte para múltiples ámbitos
> 2. Un **verificador de tipos** para operaciones y asignaciones
> 3. Un **manejador de errores** que reporta problemas de forma clara
>
> Comencemos con una demostración en vivo..."

---

## 🎬 COMANDOS PARA EJECUTAR

### Demo Básica
```powershell
python parser.py
```

### Demo Completa Interactiva
```powershell
python demo_sustentacion.py
```

### Tests Individuales
```powershell
python -c "from parser import parser; from lexer import lexer; parser.parse('int x; x = 5;', lexer=lexer)"
```

---

## 📚 ARCHIVOS DE REFERENCIA

Durante la sustentación, ten estos archivos abiertos en tabs:

1. **parser.py** - Líneas clave:
   - L47: `p_declaration` - Declaración de variables
   - L81: `p_assignment` - Asignaciones con verificación
   - L105: `p_expression_binop` - Propagación de tipos
   - L38: `p_block` / `p_scope_enter` - Manejo ámbitos

2. **symbol_table.py** - Todo el archivo (pequeño)
   - L3: Clase `Symbol`
   - L7: Clase `ScopedSymbolTable`
   - L30: Método `lookup` (algoritmo clave)

3. **demo_sustentacion.py** - Para ejecutar

---

## 🎯 OBJETIVOS DE APRENDIZAJE DEMOSTRADOS

Al final de tu sustentación, debes haber demostrado que:

✅ Entiendes la diferencia entre análisis sintáctico y semántico
✅ Puedes implementar una tabla de símbolos con ámbitos
✅ Sabes verificar compatibilidad de tipos
✅ Comprendes el modelo de pila para ámbitos anidados
✅ Puedes integrar acciones semánticas en PLY
✅ Detectas y reportas errores semánticos claramente
✅ Entiendes conceptos como shadowing y propagación de tipos
✅ Puedes extender el sistema con nuevas características

---

## 📞 RECURSOS DE EMERGENCIA

**Si algo falla durante la demo:**

1. **Python no encuentra módulos:**
   ```powershell
   cd d:\John\Dev\Compiladores\Compiladores
   python parser.py
   ```

2. **Error de importación:**
   - Verificar que todos los archivos estén en el mismo directorio
   - Verificar que PLY esté instalado: `pip install ply`

3. **Demo no funciona:**
   - Tener screenshots de salida esperada
   - Explicar qué debería pasar
   - Mostrar el código en su lugar

---

## ⏱️ TIMING SUGERIDO

```
00:00 - 02:00  Introducción y conceptos
02:00 - 05:00  Demo programa correcto
05:00 - 10:00  Demo de errores (4 casos)
10:00 - 15:00  Explicación técnica (código)
15:00 - 17:00  Conclusiones y extensiones
17:00 - 20:00  Preguntas y respuestas
```

---

## ✨ CIERRE SUGERIDO

> "En resumen, he implementado un analizador semántico funcional que:
> - Detecta variables no declaradas y duplicadas
> - Verifica compatibilidad de tipos
> - Maneja ámbitos anidados correctamente
> - Se integra naturalmente con PLY
>
> Las extensiones naturales serían agregar soporte para funciones, arrays, y tipos más complejos. Pero este prototipo demuestra los conceptos fundamentales del análisis semántico.
>
> ¿Tienen alguna pregunta?"

---

## 🎉 MENSAJE FINAL

**Respira, has hecho un buen trabajo.**

Tu implementación es sólida, los conceptos están claros, y tienes ejemplos preparados.

Confía en tu conocimiento y en tu código. Si te hacen una pregunta que no esperabas, está bien decir "no implementé eso aquí, pero una forma de hacerlo sería..."

**¡Mucha suerte! 🚀**

---

**Última revisión antes de empezar:**
- [ ] ¿Funciona el código? ✅
- [ ] ¿Entiendo cada parte? ✅
- [ ] ¿Tengo ejemplos preparados? ✅
- [ ] ¿Puedo responder preguntas básicas? ✅
- [ ] ¿Estoy listo? ✅

**¡Adelante! Vas a hacerlo genial.** 💪
