from automataPila import AutomataPila
from animarAutomata import AnimadorAutomata


cadena = input("Cadena: ")
automata = AutomataPila()
resultado = automata.procesarCadena(cadena)

print("Cadena aceptada" if resultado else "Cadena rechazada")
animador = AnimadorAutomata(automata.transiciones, automata.n, automata.m)
