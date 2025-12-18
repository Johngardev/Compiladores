# ✅ Lista de Verificación - Código del Profesor

## Elementos del Código a Evaluar

### Directivas de Preprocesador
- [x] `#include stdio.h` → **Reconocido correctamente** 
- [x] `#define aktura 67.8` → **Reconocido correctamente**

### Comentarios
- [x] `// este es un comentario` → **Ignorado correctamente**
- [x] `/* comentario multilínea */` → **Ignorado correctamente**

### Función evaluar
- [x] `int evaluar(int a, int b, float c)` → **Función definida**
- [x] Parámetros: `int a, int b, float c` → **Agregados a tabla de símbolos**

### Declaraciones de Variables
- [x] `int p,q,*q, r=100, **u;` → **Reconocido** (detecta error de redeclaración de 'q')
- [x] `float r;` → **Reconocido** (detecta error de redeclaración de 'r')  
- [x] `char *z;` → **Puntero a char reconocido**
- [x] `boolean val=true;` → **Tipo boolean y literal true reconocidos**

### Operadores de Punteros
- [x] `q=&p;` → **Operador de dirección (&) reconocido**

### Estructura IF-ELSE
- [x] `if (a>0) p=a+1;` → **IF reconocido**
- [x] `else q=b;` → **ELSE reconocido**
- [x] Operador `>` → **Reconocido**

### Estructura IF anidada
- [x] `if (b>0) { ... }` → **IF con bloque reconocido**

### Estructura WHILE
- [x] `while(p<=100) { ... }` → **WHILE detectado**
- [x] Operador `<=` → **Reconocido**
- [x] `q=q+1;` → **Asignación dentro del while**
- [x] `r--;` → **Operador decremento reconocido**

### Estructura FOR
- [x] `for(p=0;p<100; p++) { ... }` → **FOR detectado**
- [x] Inicialización: `p=0` → **Reconocida**
- [x] Condición: `p<100` → **Reconocida**
- [x] Actualización: `p++` → **Operador incremento reconocido**
- [x] `c=c+1;` → **Cuerpo del for**

### Estructura SWITCH-CASE
- [x] `switch(a) { ... }` → **SWITCH detectado**
- [x] `case 1: a=b; break;` → **CASE y BREAK reconocidos**
- [x] `case 2: a=c; break;` → **Detecta error de tipos (float a int)**
- [x] `case 3: c=a+b; break;` → **Reconocido**
- [x] `default: a=0; break;` → **DEFAULT reconocido**

### Sentencia RETURN
- [x] `return (a+1);` → **RETURN con expresión reconocido**

### Función fibonacci
- [x] `int fibonaci(int i)` → **Definición de función**
- [x] `if(i == 0) { return 0; }` → **IF con operador == reconocido**
- [x] `if(i == 1) { return 1; }` → **Segunda condición**
- [x] `return fibonaci(i-1) + fibonaci(i-2);` → **Llamadas recursivas reconocidas**

---

## Resumen de Resultados

### ✅ Análisis Léxico
- **Total de tokens:** ~300 tokens reconocidos
- **Comentarios:** Correctamente ignorados
- **Sin errores léxicos significativos**

### ✅ Análisis Sintáctico
- **Todas las estructuras reconocidas**
- **Gramática correcta**
- **Compilación exitosa**

### ⚠️ Análisis Semántico
Detectó 3 errores (correcto):
1. Redeclaración de 'q'
2. Redeclaración de 'r'
3. Asignación de float a int en `case 2: a=c;`

---

## 🎯 Resultado Final

### **✓ COMPILACIÓN EXITOSA**

El compilador acepta el código correctamente y realiza:
- ✅ Análisis léxico completo
- ✅ Análisis sintáctico completo
- ✅ Análisis semántico básico con detección de errores
- ✅ Reconocimiento de todas las estructuras de C
