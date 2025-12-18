"""
Script de demostración para la sustentación del analizador semántico
Ejecuta múltiples casos de prueba mostrando diferentes aspectos del análisis semántico
"""

import sys
import os

# Asegurar que se puedan importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def reset_compiler():
    """Reinicia el compilador para cada prueba"""
    # Reimportar módulos para reiniciar estado
    import importlib
    global parser, lexer, symbol_table, gen
    
    import symbol_table as st_module
    import code_gen as cg_module
    import parser as parser_module
    import lexer as lexer_module
    
    importlib.reload(st_module)
    importlib.reload(cg_module)
    importlib.reload(lexer_module)
    importlib.reload(parser_module)
    
    from parser import parser, gen, symbol_table
    from lexer import lexer
    
    return parser, lexer, symbol_table, gen

def print_header(title):
    """Imprime un encabezado bonito"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_separator():
    """Imprime una línea separadora"""
    print("-"*70)

def run_test(test_num, title, code, description="", pause=True):
    """Ejecuta un caso de prueba"""
    print_header(f"TEST {test_num}: {title}")
    
    if description:
        print(f"\n📋 {description}")
    
    print("\n--- CÓDIGO FUENTE ---")
    print(code)
    
    print("\n--- INICIANDO ANÁLISIS ---")
    parser, lexer, symbol_table, gen = reset_compiler()
    
    try:
        parser.parse(code, lexer=lexer)
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
    
    print_separator()
    
    if pause:
        input("\n⏸️  Presiona ENTER para continuar...")

def main():
    """Función principal de demostración"""
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║       DEMOSTRACIÓN: ANALIZADOR SEMÁNTICO CON PLY                  ║
║                                                                    ║
║  Este script demuestra las capacidades del analizador semántico   ║
║  implementado con Python Lex-Yacc (PLY)                          ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    input("Presiona ENTER para comenzar...")
    
    # ========== TEST 1: Programa correcto ==========
    run_test(
        1,
        "Programa Correcto con Ámbitos",
        """int a, b, c;
float x;

a = 10;
b = 20;

{
    int temp;
    temp = a + b * 2;
    x = temp + 0.5;
}

c = a + b;""",
        description="Ejemplo de un programa válido con declaraciones, asignaciones y ámbitos"
    )
    
    # ========== TEST 2: Variable no declarada ==========
    run_test(
        2,
        "Error - Variable No Declarada",
        """a = 10;
int a;""",
        description="Intento de usar una variable antes de declararla"
    )
    
    # ========== TEST 3: Variable duplicada ==========
    run_test(
        3,
        "Error - Variable Duplicada en Mismo Ámbito",
        """int x;
int x;""",
        description="Intento de declarar la misma variable dos veces en el mismo ámbito"
    )
    
    # ========== TEST 4: Variable fuera de ámbito ==========
    run_test(
        4,
        "Error - Variable Fuera de Ámbito",
        """{
    int temp;
    temp = 5;
}
temp = 10;""",
        description="Intento de acceder a una variable fuera de su ámbito"
    )
    
    # ========== TEST 5: Incompatibilidad de tipos ==========
    run_test(
        5,
        "Error - Incompatibilidad de Tipos",
        """int numero;
numero = 3.14;""",
        description="Intento de asignar un float a una variable int"
    )
    
    # ========== TEST 6: Ámbitos anidados correctos ==========
    run_test(
        6,
        "Ámbitos Anidados Correctos",
        """int x;
x = 10;

{
    int x;
    x = 20;
    {
        int x;
        x = 30;
    }
}""",
        description="Variables con el mismo nombre en diferentes ámbitos (shadowing)"
    )
    
    # ========== TEST 7: Tipos mixtos en expresiones ==========
    run_test(
        7,
        "Tipos Mixtos en Expresiones",
        """int a;
float x, y;

a = 10;
x = 3.14;
y = a + x;""",
        description="Operaciones entre int y float (promoción de tipo)"
    )
    
    # ========== TEST 8: Expresiones complejas ==========
    run_test(
        8,
        "Expresiones Aritméticas Complejas",
        """int a, b, c, d;

a = 5;
b = 10;
c = 3;

d = a + b * c;""",
        description="Expresiones con múltiples operadores y precedencia",
        pause=False
    )
    
    # ========== RESUMEN FINAL ==========
    print_header("RESUMEN DE LA DEMOSTRACIÓN")
    
    print("""
✅ CAPACIDADES DEMOSTRADAS:

1. 📝 Declaración de variables (int y float)
2. 🔍 Verificación de existencia de variables
3. 🎯 Detección de variables duplicadas
4. 📦 Manejo de ámbitos (scopes) anidados
5. 🔒 Control de visibilidad de variables
6. 🔢 Verificación de compatibilidad de tipos
7. ➕ Propagación de tipos en expresiones
8. ⚠️  Reportes de errores semánticos claros

🎯 CONCEPTOS CLAVE:

• Tabla de símbolos con pila de ámbitos
• Búsqueda de símbolos desde local hasta global
• Shadowing (ocultamiento) de variables
• Promoción de tipos (int + float = float)
• Validación en tiempo de compilación

📚 HERRAMIENTAS UTILIZADAS:

• PLY (Python Lex-Yacc)
• Análisis sintáctico dirigido por sintaxis
• Acciones semánticas integradas en las reglas gramaticales
    """)
    
    print_separator()
    print("\n✨ Fin de la demostración ✨\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demostración interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
