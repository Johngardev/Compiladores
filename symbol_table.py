class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class ScopedSymbolTable:
    def __init__(self):
        # Pila de ambitos. El primer elemento es el ambito global
        self.scopes = [{}]
        print("Symbol table initialized with global scope.")

    def push_scope(self):
        """Push a new scope onto the stack."""
        self.scopes.append({})

    def pop_scope(self):
        """Finalize the current scope."""
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise SemanticError("Cannot pop the global scope.")
        
    def add(self, symbol):
        """Add a symbol to the current scope."""
        current_scope = self.scopes[-1]
        if symbol.name in current_scope:
            raise SemanticError(f"Semantic Error: Symbol '{symbol.name}' already declared in the current scope.")
        current_scope[symbol.name] = symbol
        print(f"Added symbol: {symbol.name} of type {symbol.type} to current scope.")
    
    def lookup(self, name):
        """Look up a symbol by name, searching from the current scope to the global scope."""
        for scope in reversed(self.scopes):
            symbol = scope.get(name)
            if symbol:
                return symbol
        raise SemanticError(f"Semantic Error: the Variable '{name}' is not declared.")
    
#Class for our semantic errors
class SemanticError(Exception):
    pass