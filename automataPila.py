from collections import deque

class AutomataPila:
    def __init__(self):
        self.pila = deque()
        self.estado = 'q0'
        self.simboloInicialPila = 'Z'
        self.pila.append(self.simboloInicialPila)
        self.wPila = deque()
        self.transiciones = []
        self.m = 0
        self.n = 0

    def procesarCadena(self, cadena):
        i = 0
        longitud = len(cadena)
        while i < longitud:
            simbolo = cadena[i]
            pilaAntes = list(self.pila)
            estadoAntes = self.estado

            if self.estado == 'q0':
                if simbolo in ['b', 'c']:
                    self.pila.append(simbolo)
                    self.wPila.append(simbolo)
                    self.m += 1
                elif simbolo == 'a' and self.wPila:
                    self.estado = 'q1'
                    self.pila.append('A')
                    self.n += 1
                else:
                    break
            elif self.estado == 'q1':
                if simbolo == 'a':
                    self.pila.append('A')
                    self.n += 1
                elif simbolo == 'd':
                    self.estado = 'q2'
                    if not self.popPilaEsperado('A'):
                        break
                else:
                    break
            elif self.estado == 'q2':
                if simbolo == 'd':
                    if not self.popPilaEsperado('A'):
                        break
                elif simbolo in ['b', 'c']:
                    self.estado = 'q3'
                    esperado = self.wPila.pop() if self.wPila else None
                    if not self.popPilaEsperado(esperado) or simbolo != esperado:
                        break
                else:
                    break
            elif self.estado == 'q3':
                esperado = self.wPila.pop() if self.wPila else None
                if not self.popPilaEsperado(esperado) or simbolo != esperado:
                    break

            self.transiciones.append((estadoAntes, simbolo, list(pilaAntes), self.estado, list(self.pila)))
            i += 1

        self.transiciones.append(('FIN', '', list(self.pila), self.estado, list(self.pila)))
        esAceptada = self.estado == 'q3' and len(self.pila) == 1 and self.pila[-1] == self.simboloInicialPila
        if not esAceptada:
            self.transiciones.append((
                self.estado,
                '⛔',
                list(self.pila),
                'RECHAZADA',
                list(self.pila)
            ))
        else:
            self.transiciones.append((
                self.estado,
                '✔',
                list(self.pila),
                'ACEPTADA',
                list(self.pila)
            ))
        return esAceptada

    def popPilaEsperado(self, esperado):
        if not self.pila:
            return False
        tope = self.pila.pop()
        return tope == esperado
