class Codegenerator:
    def __init__(self):
        self.code = [] #Lista para guardar las instrucciones
        self.temp_count = 0 #Contador para variables temporales
    
    def new_temp(self):
        temp_name = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_name
    
    def emit(self, op, arg1, arg2, result):
        """
        Genera una instrucción de 3 direcciones (Cuádruplo).
        Formato: (operador, operando1, operando2, resultado)
        Ejemplo: ('+', 'x', '5', 't1') -> t1 = x + 5
        """
        instruction = (op, arg1, arg2, result)
        self.code.append(instruction)

    def print_code(self):
        """Imprime el código generado en formato legible."""
        print("\n--- CODIGO INTERMEDIO GENERADO (3AC) ---")
        for op, arg1, arg2, res in self.code:
            if op == '=':
                print(f"{res} = {arg1}")
            else:
                print(f"{res} = {arg1} {op} {arg2}")
        print("--- FIN DEL CODIGO INTERMEDIO ---\n")
        