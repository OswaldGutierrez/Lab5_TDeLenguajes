# Lab5_Teoría de Lenguajes  
**Autores:** Oswald David Gutiérrez & Jhomar Farid Arrieta  
[Repositorio en GitHub](https://github.com/OswaldGutierrez/Lab5_TDeLenguajes.git)  

---

## Introducción

Los **autómatas de pila (AP)** son máquinas teóricas fundamentales para el estudio de los lenguajes libres de contexto. Incorporan una pila que les permite reconocer estructuras más complejas que los autómatas finitos, como expresiones balanceadas o palíndromos.  

En esta práctica se implementó un autómata de pila determinista que procesa cadenas de entrada según reglas específicas, incluyendo una simulación gráfica interactiva que permite observar el comportamiento del autómata paso a paso.  

El objetivo principal es entender visualmente cómo el autómata manipula su pila y cambia de estado con cada símbolo leído, reforzando así los conceptos teóricos mediante una herramienta práctica e intuitiva.  

---

## Abstract

This project presents the implementation of a **Pushdown Automaton (PDA)** in Python, including a graphical and step-by-step simulation of its transitions. The PDA validates strings of a context-free language that follows a specific structure where the central part is balanced by symbols pushed and popped from a stack.  

The simulation highlights each state transition and stack operation, allowing the user to advance interactively. This helps understand the internal behavior of a PDA and clarifies why certain strings are accepted or rejected.  

---

## Objetivos

- Implementar un autómata de pila determinista en Python.  
- Simular visualmente el comportamiento del autómata durante el procesamiento de una cadena.  
- Permitir una exploración paso a paso mediante una interfaz gráfica interactiva.  
- Visualizar en qué punto una cadena es aceptada o rechazada, y entender por qué.  
- Validar el diseño del AP permitiendo cadenas con y sin entrada previa a la sección balanceada.  

---

## Estructura del Proyecto

El código se divide en tres archivos principales:

| Archivo           | Descripción                                                                                  |
|-------------------|----------------------------------------------------------------------------------------------|
| `automataPila.py` | Implementa la clase del autómata, procesando la cadena y registrando todas las transiciones. |
| `animarAutomata.py` | Genera la interfaz gráfica, visualiza estados y permite avanzar manualmente cada transición.  |
| `main.py`         | Solicita la cadena al usuario, ejecuta la simulación y muestra el resultado final.            |

---

## Funcionamiento de la Simulación Paso a Paso

- Por cada símbolo leído:  
  - Se actualiza el estado según el símbolo y el contenido actual de la pila.  
  - Se registra la transición completa (estado previo, símbolo leído, pila antes y después, estado siguiente).  
  - En la interfaz gráfica, el estado actual se resalta en naranja y se muestra el contenido de la pila en cada paso.  
- Si la cadena es rechazada, el autómata llega a un nodo especial `RECHAZADA` que permite ver el estado y contenido de pila al finalizar.  

---

## Conclusiones

La implementación de un autómata de pila en Python junto con su simulación gráfica paso a paso permitió una comprensión profunda del procesamiento de cadenas de lenguajes libres de contexto.  

La interfaz gráfica facilita el seguimiento visual de cada transición y operación sobre la pila, demostrando ser una herramienta didáctica valiosa para detectar errores en la lógica de aceptación o rechazo.  

Gracias a esta práctica, se reforzó la importancia de un diseño correcto de las transiciones y del análisis exhaustivo de casos particulares. Este proyecto contribuyó al desarrollo de habilidades prácticas en el modelado de autómatas y fortaleció la comprensión teórica de los lenguajes formales.  

---

## Código Principal: `automataPila.py`

```python
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
