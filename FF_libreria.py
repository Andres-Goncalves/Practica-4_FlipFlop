class Flipflop:
    def __init__(self, entrada, estado):
        self.entrada = entrada
        self.estado = estado
        self.aux_estado = estado

    def buffer(self):
        self.aux_estado = self.entrada.valor()
        
    def actualizar(self):
        self.estado = self.aux_estado
    
    def valor(self):
        return self.estado
        
class Xor:
    def __init__(self, entradas):
        self.entradas = entradas
        
    def valor(self):
        cont = 0
        for o in self.entradas:
            if o.valor() == 1:
                cont += 1
                if cont > 1:
                    return 0
        return cont
    
class Cable:
    def __init__(self, entradas):
        self.entradas = entradas
    
    def valor(self):
        for i in self.entradas:
            if i.valor() == 1:
                return 1
        return 0
    
class Entrada:
    def __init__(self, cadena):
        self.cadena = cadena
        self.posicion = 0
        
    def valor(self):
        return int(self.cadena[self.posicion])
        
    def siguiente(self):
        if (self.posicion + 1) == len(self.cadena):
            return False
        else:
            self.posicion += 1
            return True
        
class Salida:
    def __init__(self, entrada):
        self.entrada = entrada
        self.salida = ""

    def leer_valor(self):
        self.salida += str(self.entrada.valor())
        
    def get(self):
        return self.salida