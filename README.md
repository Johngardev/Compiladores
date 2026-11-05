<div align="center">

# Compiladores

### Analizador y compilador educativo para un subconjunto de C

Implementado en Python con PLY. Explora análisis léxico y sintáctico, comprobaciones semánticas básicas y generación de código intermedio de tres direcciones.

</div>

---

## Descripción

**Compiladores** es un proyecto académico que construye un compilador didáctico para un dialecto reducido inspirado en C. Su objetivo es mostrar cómo se conectan las etapas iniciales de un compilador: convertir texto fuente en tokens, reconocer su estructura, consultar una tabla de símbolos y generar una representación intermedia para ciertas expresiones.

> **Alcance:** no es un compilador de C estándar ni está pensado para compilar programas de producción. Algunas construcciones están reconocidas por la gramática, pero su análisis semántico o su generación de código todavía son parciales.

## Características

La gramática y el lexer contemplan, entre otras, las siguientes construcciones:

- Tipos `int`, `float`, `char`, `boolean` y `void`.
- Identificadores, literales numéricos, caracteres y cadenas.
- Declaraciones, asignaciones y bloques delimitados por llaves.
- Operadores aritméticos, relacionales, lógicos, unarios e incremento/decremento.
- Directivas sencillas `#include` y `#define`.
- Definiciones y llamadas a funciones, parámetros y `return`.
- Estructuras `if`/`else`, `while`, `for` y `switch`/`case`, además de `break`.
- Comentarios de una línea (`//`) y multilínea (`/* ... */`).
- Tabla de símbolos con ámbitos anidados y búsqueda desde el ámbito actual hacia los externos.
- Generación de código intermedio de tres direcciones (3AC) para expresiones y asignaciones compatibles con el generador actual.

### Estado de implementación

| Componente | Estado |
| --- | --- |
| Análisis léxico | Reconoce los tokens definidos en `lexer.py`; los caracteres ilegales se notifican en consola. |
| Análisis sintáctico | Gramática educativa definida con PLY en `parser.py`. |
| Análisis semántico | Parcial: tabla de símbolos, ámbitos y algunas comprobaciones de declaración y tipos. |
| Código intermedio | Emite instrucciones 3AC para operaciones y asignaciones; no traduce el flujo de control a saltos. |
| Compilación a código ejecutable | No implementada. |

## Arquitectura

```text
Código fuente
     │
     ▼
 lexer.py ──► secuencia de tokens
                    │
                    ▼
              parser.py ◄────► symbol_table.py
                    │           símbolos y ámbitos
                    ▼
               code_gen.py
                    │
                    ▼
          instrucciones 3AC
```

| Archivo | Responsabilidad |
| --- | --- |
| [`lexer.py`](lexer.py) | Define tokens, palabras reservadas y reglas léxicas con `ply.lex`. |
| [`parser.py`](parser.py) | Define la gramática, coordina el análisis y contiene acciones semánticas. También incluye un programa de ejemplo ejecutable. |
| [`symbol_table.py`](symbol_table.py) | Implementa símbolos, ámbitos anidados y errores semánticos. |
| [`code_gen.py`](code_gen.py) | Almacena cuádruplos y los presenta en formato legible como código de tres direcciones. |
| [`test_codigo_profesor.py`](test_codigo_profesor.py) | Ejecuta un ejemplo de análisis léxico y sintáctico con un programa de muestra. |

## Requisitos

- Python 3.
- [PLY](https://www.dabeaz.com/ply/), la biblioteca Python Lex-Yacc.

## Instalación

Clona el repositorio y entra en su directorio:

```bash
git clone https://github.com/Johngardev/Compiladores.git
cd Compiladores
```

Se recomienda utilizar un entorno virtual:

```bash
python -m venv .venv
```

Actívalo según tu sistema:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instala la dependencia:

```bash
python -m pip install ply
```

## Uso

Ejecuta el ejemplo incluido en el parser:

```bash
python parser.py
```

El programa muestra el código fuente de ejemplo, ejecuta el análisis y presenta las instrucciones intermedias generadas.

También puedes ejecutar el ejemplo de prueba:

```bash
python test_codigo_profesor.py
```

Este script imprime los tokens reconocidos y ejecuta el parser sobre un programa de muestra. La salida puede incluir avisos o errores semánticos: el ejemplo contiene casos de redeclaración e incompatibilidad de tipos intencionales, y el analizador todavía no convierte todos los errores en un resultado de compilación fallido.

## Ejemplo de código intermedio

Para una expresión como:

```c
c = a + b * 2;
```

el generador representa primero la operación de mayor precedencia y después la suma:

```text
t0 = b * 2
t1 = a + t0
c = t1
```

Los temporales (`t0`, `t1`, ...) permiten descomponer expresiones en instrucciones sencillas. La salida es una representación intermedia; no es código máquina ni un ejecutable.

## Limitaciones conocidas

Este proyecto es un trabajo en evolución. Entre las limitaciones actuales se encuentran:

- La cobertura semántica es incompleta: no todas las construcciones gramaticales tienen validación de tipos o de contexto.
- La generación 3AC no implementa etiquetas ni saltos para `if`, bucles o `switch`.
- No se genera ensamblador ni código ejecutable.
- La gramática no pretende cubrir el estándar C; arrays, estructuras y muchas otras características no están implementados de forma completa.
- Los inicializadores, parámetros, funciones y punteros no deben considerarse plenamente validados solo porque algunas formas aparecen en la gramática.
- No hay actualmente una suite automatizada de pruebas con un framework de testing.

## Posibles mejoras

- Separar la interfaz de ejecución del parser y aceptar archivos fuente desde la línea de comandos.
- Centralizar errores léxicos, sintácticos y semánticos con número de línea y contexto.
- Completar la validación de tipos, declaraciones, funciones y ámbitos.
- Implementar generación de flujo de control en 3AC mediante etiquetas y saltos.
- Añadir pruebas automatizadas para casos válidos, errores y regresiones.
- Documentar formalmente la gramática del subconjunto soportado.

## Tecnologías

- **Python** — implementación.
- **PLY (Python Lex-Yacc)** — análisis léxico y sintáctico.

## Contribuciones

Las mejoras y correcciones son bienvenidas. Para proponer cambios, abre un *issue* con el contexto del problema o envía un *pull request* con una descripción clara y pruebas o ejemplos cuando corresponda.

## Licencia

No se especifica una licencia en este repositorio. Antes de reutilizar, modificar o distribuir el código, consulta con el autor o añade una licencia apropiada.
