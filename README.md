# Analizador Semántico para un Lenguaje tipo C con PLY
El objetivo de este proyecto es el diseño, desarrollo e implementación de un analizador semántico para un subconjunto del lenguaje de programación C. Este analizador se integra con un analizador léxico y sintáctico previamente construido, formando las primeras fases de un compilador funcional. El sistema es capaz de validar la correctitud semántica del código fuente, incluyendo la gestión de variables, la comprobación de tipos y el manejo de ámbitos (scopes).

### Herramientas y lenguajes
   -   Lenguaje de implementacion: Python 3.
   -   Libreria principal: PLY (Python Lex-Yacc), una bibiloteca fundamental para la construccion de analizadores lexicos y sintacticos en Python.

### Alcance del lenguaje soportado
El analizador procesa un lenguaje tipo C con las siguientes caracteristicas:

  - Declaracion de variables: Soporta la declaracion de variables de tipo int y float, permite declaraciones multiples en una misma linea (ej: int a, b;).
  - Asignacion: Permite la asignacion de valores a variables declaradas.
  - Expresiones Aritmeticas: Soporta operaciones de suma (+) y resta (-).
  - Ambitos Anidados: Gestiona correctamente los ambitos locales definidos por llaves {...}, permitiendo el shadowing de variables (declaracion de una variable desde un ambito interno con el mismo nombre que una en un ambito externo).

## Arquitectura del Analizador

El proyecto está estructurado en tres módulos de Python interconectados que representan las fases clásicas de un compilador:

  1. lexer.py (Analizador Léxico): Recibe el código fuente como una cadena de texto y lo descompone en una secuencia de unidades mínimas con significado, llamadas tokens.

  2. symbol_table.py (Tabla de Símbolos): Es el componente central del análisis semántico. Actúa como una base de datos que almacena información sobre los identificadores (variables) y gestiona su visibilidad según el ámbito.

  3. parser.py (Analizador Sintáctico y Semántico): Recibe la secuencia de tokens del lexer. Su doble función es:
     - Análisis Sintáctico: Verificar que la secuencia de tokens siga las reglas gramaticales del lenguaje.
     - Análisis Semántico: Realizar las validaciones de significado utilizando la Tabla de Símbolos.

El flujo de trabajo es el siguiente:
Código Fuente -> lexer.py -> Stream de Tokens -> parser.py <-> symbol_table.py -> Validación Semántica / Mensajes de Error
