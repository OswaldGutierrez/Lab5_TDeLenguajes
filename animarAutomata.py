import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnimadorAutomata:
    def __init__(self, transiciones, n, m):
        self.transiciones = transiciones
        self.pasoActual = 0
        self.n = n
        self.m = m

        self.estados = ['q0', 'q1', 'q2', 'q3']
        self.grafo = nx.DiGraph()
        for i in range(len(self.estados) - 1):
            self.grafo.add_edge(self.estados[i], self.estados[i + 1])
        self.grafo.add_edge('q2', 'q3')

        self.pos = nx.spring_layout(self.grafo, seed=42)

        self.ventana = tk.Tk()
        self.ventana.title("Simulación de Autómata de Pila")
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.ventana)
        self.canvas.get_tk_widget().pack()

        self.btn = tk.Button(self.ventana, text="Siguiente paso", command=self.siguientePaso)
        self.btn.pack()

        self.textoEstado = tk.Label(self.ventana, text="", font=("Courier", 14))
        self.textoEstado.pack()

        # Mostrar los valores de n y m
        self.textoNM = tk.Label(self.ventana, text=f"n: {self.n} | m: {self.m}", font=("Courier", 12))
        self.textoNM.pack()

        self.textoPila = tk.Label(self.ventana, text="Pila:\n[vacío]", font=("Courier", 12))
        self.textoPila.pack()

        self.dibujarPaso()
        self.ventana.mainloop()

    def dibujarPaso(self):
        self.ax.clear()

        
        estadoActivo = None
        if self.pasoActual < len(self.transiciones):
            _, _, _, estadoActivo, _ = self.transiciones[self.pasoActual]

        # Colores
        coloresNodos = []
        for estado in self.estados:
            if estado == estadoActivo:
                coloresNodos.append('orange')
            else:
                coloresNodos.append('lightblue')

        nx.draw(self.grafo, self.pos, with_labels=True, node_color=coloresNodos, node_size=1000, ax=self.ax)

        if self.pasoActual < len(self.transiciones):
            estadoAntes, simbolo, pilaAntes, estadoDespues, pilaDespues = self.transiciones[self.pasoActual]
            pilaTexto = ''.join(pilaDespues)
            self.textoEstado.config(
                text=f"Estado: {estadoAntes} → {estadoDespues}\nSímbolo: '{simbolo}'\nPila: {''.join(pilaAntes)} → {pilaTexto}"
            )
        else:
            ultima = self.transiciones[-1]
            estadoAntes, simbolo, pilaAntes, estadoFinal, pilaFinal = ultima
            colorFinal = 'green' if estadoFinal == 'ACEPTADA' else 'red'
            self.ax.text(0.5, -0.1, f"Resultado: {estadoFinal}", fontsize=14, color=colorFinal, ha='center', transform=self.ax.transAxes)
            self.textoEstado.config(
                text=f"Estado final: {estadoAntes} → {estadoFinal}\nPila final: {''.join(pilaFinal)}"
            )
            self.btn.config(state="disabled")

            pilaDespues = pilaFinal


        # valores de n y m en la interfaz
        self.textoNM.config(text=f"n: {self.n} | m: {self.m}")

        # Mostrar la pila en formato texto
        self.dibujarPila(pilaDespues)
        self.canvas.draw()

    def dibujarPila(self, pila):
        # Crear la visualización de la pila en formato de texto
        pilaTexto = "\n".join([f"[{elem}]" for elem in reversed(pila)]) if pila else "[vacío]"

        # Actualizar la etiqueta de la pila en la interfaz
        self.textoPila.config(text=f"Pila:\n{pilaTexto}")

    def siguientePaso(self):
        if self.pasoActual < len(self.transiciones):
            self.pasoActual += 1
            self.dibujarPaso()
