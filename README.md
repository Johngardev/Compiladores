# Analizador Semántico para un Lenguaje tipo C con PLY

El objetivo de este proyecto es el diseño, desarrollo e implementación de un **analizador semántico** para un subconjunto del lenguaje de programación C. Este analizador se integra con un analizador léxico y sintáctico previamente construido, formando las primeras fases de un compilador funcional. El sistema es capaz de validar la correctitud semántica del código fuente, incluyendo la gestión de variables, la comprobación de tipos y el manejo de ámbitos (scopes).

### Herramientas y lenguajes
   -   Lenguaje de implementacion: Python 3.
   -   Libreria principal: PLY (Python Lex-Yacc), una biblioteca fundamental para la construccion de analizadores lexicos y sintacticos en Python.

### Alcance del lenguaje soportado
El análizador procesa un lenguaje tipo C con las siguientes caracteristicas:

  - **Declaracion de variables**: Soporta la declaracion de variables de tipo `int` y `float`, permite declaraciones multiples en una misma linea (ej: `int a, b;`).
  - **Asignacion**: Permite la asignacion de valores a variables declaradas.
  - **Expresiones Aritmeticas**: Soporta operaciones de suma (`+`) y resta (`-`).
  - **Ambitos Anidados**: Gestiona correctamente los ambitos locales definidos por llaves `{...}`, permitiendo el shadowing de variables (declaracion de una variable desde un ambito interno con el mismo nombre que una en un ambito externo).

## Arquitectura del Análizador

El proyecto está estructurado en tres módulos de Python interconectados que representan las fases clásicas de un compilador:

  1. `lexer.py` **(Análizador Léxico)**: Recibe el código fuente como una cadena de texto y lo descompone en una secuencia de unidades mínimas con significado, llamadas tokens.
  2. `symbol_table.py` **(Tabla de Símbolos)**: Es el componente central del análisis semántico. Actúa como una base de datos que almacena información sobre los identificadores (variables) y gestiona su visibilidad según el ámbito.
  3. `parser.py` **(Análizador Sintáctico y Semántico)**: Recibe la secuencia de tokens del lexer. Su doble función es:
        - **Análisis Sintáctico**: Verificar que la secuencia de tokens siga las reglas gramaticales del lenguaje.
        - **Análisis Semántico**: Realizar las validaciones de significado utilizando la Tabla de Símbolos.

El flujo de trabajo es el siguiente: 
#### `Código Fuente` -> `lexer.py` -> `Stream de Tokens` -> `parser.py` <-> `symbol_table.py` -> `Validación Semántica / Mensajes de Error`

## Descripcion de Módulos
### `lexer.py`
Responsable de la tokenizacion. Define todos los componentes léxicos del lenguaje.
   - `tokens`: Una tupla que enumera todos los posibles tokens (ej: `ID`, `INT_LITERAL`, `PLUS`).
   - `reserved`: Un diccionario que mapea palabras clave del lenguaje (como int y float) a sus tipos de token correspondientes, àra diferenciarlas de los identificadores (`ID`).
   - **Reglas (funciones `t_...`)**: Expresiones regulares y funciones que definen como reconocer cada token en el texto de entrada.

**Ejemplo de tokenización:**
La linea de código `float pi = 3.14;` se convierte en la secuencia de tokens:
`FLOAT`, `ID('pi')`, `ASSIGN`, `FLOAT_LITERAL(3.14)`, `SEMICOLON`

### `symbol_table.py`
Sera la estructura de datos clave para la validación semántica.
   - Estrucutra: Se implementó como una pila de diccionarios (`list[dict]`). Esta estructura es ideal para modelar los ámbitos anidados de C:
        - El primer diccionario en la lista es el **ámbito global**.
        - Cada vez que se entra en un bloque `{...}`, se añade un nuevo diccionario a la pila.
        - Al salir de un bloque, se elimina el último diccionario de la pila.
   - **Métodos Principales**
     - `push_scope()`: Crea un nuevo ámbito (añade un diccionario a la pila).
     - `pop_scope()`: Destruye el ámbito actual (elimina el último diccionario).
     - `add(symbol)`: Añade un símbolo (variable y su tipo) al ámbito actual. Verifica que no haya re-declaraciones en el mismo ámbito.
     - `lookup(name)`: Busca un símbolo empezando por el ámbito actual y continuando hacia los ámbitos externos (hacia el global). Esto simula correctamente la regla de resolución de nombres de C.
       
### `parser.py`
Este módulo define la gramática del lenguaje y, lo más importante, integra las acciones semánticas.
   - **Reglas Gramaticales (funciones `p_...`)**: Definen la sintaxis del lenguaje usando la notación Forma Backus-Naur (BNF) es una notación formal que define la sintaxis de los lenguajes de programación y otros lenguajes formales. Consta de metasímbolos como `'::='`, `'|'` y `'< >'`, y se usa comúnmente para describir gramáticas independientes del contexto.
   - **Acciones Semánticas Integradas:**
        - Gestión de Ámbitos:
             - Se utiliza una producción vacía `scope_enter :` para ejecutar `symbol_table.push_scope()` justo después de que el parser lee una llave de apertura `{`.
             - La regla `block` ejecuta `symbol_table.pop_scope()` después de que el bloque completo ha sido analizado.
        -  Análisis de Declaraciones:
             - En la regla `p_declaration`, se recorre la lista de identificadores declarados y se invoca a `symbol_table.add()` para registrarlos en el ámbito actual.
        -  Validación de Variables y Tipos:
             - En reglas que usan variables (como `p_assignment` o `p_factor_id`), se llama a `symbol_table.lookup()` para verificar que la variable haya sido declarada.
             - Una vez obtenido el tipo de las variables, se realizan las comprobaciones de compatibilidad. Por ejemplo, en `p_assignment`, se verifica que el tipo de la expresión a la derecha sea compatible con el tipo de la variable a la izquierda.

## Módulo de Generacion de Código Intermedio (3AC)
   1. La última fase implementada en el compilador es la generacion de Código de Tres Direcciones (Three-Address Code o 3AC). Esta es una representación intermedia del cídgo fuente que linealiza las estructuras    jerárquicas (árboles de expresiones) en una secuencia de instrucciones simples.
      
   El objetivo es transformar expresiones complejas como `x = a + b * c` en una serie de pasos atómicos que una maquina pueda procesar fácilmente.
   2. Arquitectura del componente se desarrollo un móulo dedicado (`code_gen.py`) que trabaja en conjunto con el analizador sintáctico.
      - Clase `CodeGenerator`: Actúa como un buffer de instrucciones.
         - Gestión de Temporales (`new_temp`): Genera variables automáticas secuenciales (`t0`, `t1`, `t2`...) para almacenar resultados parciales de operaciones aritmémticas.
         - Emision de Inatrucciones (`emit`): Almacena las operaciones en formato "cuádruplos":`operador, operando1, operando2, destino `.
         
   3. Estrategia de Traducci+on se utiliza un Traducción Dirigida por la Sintaxis. A medida qu el parser reduce las reglas gramaticales, se ejecutan las siguientes acciones:
      1. Atributos Sintetizados: La variable `p[0]` de PLY ahora transporta un diccionario con dos metadatos:
            - `type`: El tipo de dato (para validación semántica).
            - `place`: El nombre de la variable o temporal donde reside el valor (para generación de código).
      2. Descomposición de Expresiones:
            - Al encontrar una operación (ej. suma), se solicitan los lugares (`place`) de los operandos izquierdo y derecho.
            - Se genera un nuevo temporal (ej. `t5`).
            - Se emite la instrucción `t5 = lugar_izq + lugar_der`.

   4. Ejemplo de Transformación
      Código fuente (Entrada)
      ```
       val = 10 + 20 * 3;
       ```
      Lógica del Generador:
         1. Parser detecta `20 * 3`. Genera `t0`. Emite `t0 = 20 * 3`.
         2. Parser detecta `10 + t0`. Genera `t1`. Emite `t1 = 10 + t0`.
         3. Parser detecta asignacion a `val`. Emite `val = t1`
      Código Intermedio Generado (Salida):
       ```
       t0 = 20 * 3
       t1 = 10 + t0
       val = t1
       ```

## Guía de Uso y Pruebas
**Requisitos e Instalación**
 1. Tener **Python 3.x** instalado.
 2. Instalar libreria PLY a través de pip, preferiblemente en un entorno virtual:
    ```
    pip install ply
    ```

**Ejecución del Analizador**
El proyecto se ejecuta directamente desde el archivo `parser.py`, que contiene un bloque `if __name__ == '__main__':` con código de prueba.
Para ejecutarlo, navegue a la carpeta del proyecto en una terminal y ejecute:
   ```
   python parser.py
   ```

**Código de Prueba y Salida Esperada**
El script ejecuta dos pruebas automáticamente: una con código semánticamente correcto y otra diseñada para fallar.

   - **Prueba Exitosa**: El código de prueba demuestra la correcta gestión de variables globales, variables locales en ámbitos anidados y el shadowing. La salida esperada es una traza de cómo se crean y destruyen los ámbitos y se añaden los símbolos, terminando con el          mensaje "Análisis sintáctico y semántico completado exitosamente."
   - **Prueba con Error**:  El segundo bloque de código intenta usar una variable fuera del ámbito donde fue declarada.

     El analizador debe detectar este error y mostrar el siguiente mensaje en la consola:
           	```
             Error  Semántico: La variable 'b' no ha sido declarada.
            ```
     Esto demuestra que el analizador semántico es capaz de identificar errores de ámbito correctamente.



## Conclusiones y Posibles Mejoras

**Conclusión**
Se ha desarrollado con éxito un analizador semántico funcional para un subconjunto del lenguaje C. El sistema valida eficazmente las declaraciones de variables, la compatibilidad de tipos en asignaciones y la correcta utilización de ámbitos, sentando una base sólida para las fases posteriores de un compilador, como la generación de código intermedio.

**Trabajo Futuro**
El proyecto puede ser extendido para incluir características más avanzadas del lenguaje C:
   - Soporte para más tipos de datos (`char`, `void`).
   - Implementación de declaraciones y llamadas a **funciones**, incluyendo la validación de parámetros.
   - Análisis semántico para estructuras de control (`if-else`, `while`, `for`).
   - Soporte para **arreglos** y **punteros**.
   
