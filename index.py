# Autoria: Mario Tapiero
# Programa: Ingenieria de Sistemas
# Semestre: Quinto

import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor, nivel=1):
        if nivel >= 4:
            raise Exception("Error: No se permiten más de 4 niveles en el árbol.")
        if valor < nodo.valor:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar(nodo.izq, valor, nivel + 1)
        elif valor > nodo.valor:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar(nodo.der, valor, nivel + 1)

    def buscar(self, valor):
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        elif valor < nodo.valor:
            return self._buscar(nodo.izq, valor)
        else:
            return self._buscar(nodo.der, valor)

    def preorden(self):
        return self._preorden(self.raiz)

    def _preorden(self, nodo):
        if nodo is None:
            return []
        return [nodo.valor] + self._preorden(nodo.izq) + self._preorden(nodo.der)

    def inorden(self):
        return self._inorden(self.raiz)

    def _inorden(self, nodo):
        if nodo is None:
            return []
        return self._inorden(nodo.izq) + [nodo.valor] + self._inorden(nodo.der)

    def posorden(self):
        return self._posorden(self.raiz)

    def _posorden(self, nodo):
        if nodo is None:
            return []
        return self._posorden(nodo.izq) + self._posorden(nodo.der) + [nodo.valor]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Fase4_MarioTapiero")
        self.arbol = ArbolBinarioBusqueda()
        self._pantalla_login()

    def _pantalla_login(self):
        self.root.title("Fase4_MarioTapiero")
        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack(pady=30)

        tk.Label(self.frame_login, text="Aplicación: Arboles binarios", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(self.frame_login, text="Estudiante: Mario Tapiero", font=("Arial", 11)).pack(pady=5)
        tk.Label(self.frame_login, text="Fecha: 23/11/2025", font=("Arial", 11)).pack(pady=5)

        tk.Label(self.frame_login, text="Contraseña:", font=("Arial", 11)).pack(pady=5)
        self.entry_pass = tk.Entry(self.frame_login, show="*", width=20)
        self.entry_pass.pack(pady=5)

        tk.Button(self.frame_login, text="Ingresar", font=("Arial", 11), command=self._validar_login).pack(pady=10)

    def _validar_login(self):
        if self.entry_pass.get() == "UNAD":
            self.frame_login.destroy()
            self._pantalla_principal()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    def _pantalla_principal(self):
        self.root.title("Árbol Binario de Búsqueda")

        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(fill="both", expand=True)

        top_frame = tk.Frame(self.frame_main)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Ingrese un número entero:", font=("Arial", 11)).pack(side="left", padx=5)
        self.entry_valor = tk.Entry(top_frame, width=10)
        self.entry_valor.pack(side="left", padx=5)

        tk.Button(top_frame, text="Agregar Nodo", width=12, command=self.agregar_nodo).pack(side="left", padx=5)
        tk.Button(top_frame, text="Buscar Nodo", width=12, command=self.buscar_nodo).pack(side="left", padx=5)
        tk.Button(top_frame, text="Limpiar", width=12, command=self.limpiar_arbol).pack(side="left", padx=5)
        tk.Button(top_frame, text="Salir", width=12, command=self.root.quit).pack(side="left", padx=5)

        self.fig = plt.Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_main)
        self.canvas.get_tk_widget().pack(pady=10)

        bottom_frame = tk.Frame(self.frame_main)
        bottom_frame.pack(fill="x", pady=10)

        self.label_pre = tk.Label(bottom_frame, text="Preorden: []", width=40, anchor="w", relief="sunken")
        self.label_pre.pack(side="left", padx=5)

        self.label_in = tk.Label(bottom_frame, text="Inorden: []", width=40, anchor="w", relief="sunken")
        self.label_in.pack(side="left", padx=5)

        self.label_pos = tk.Label(bottom_frame, text="Posorden: []", width=40, anchor="w", relief="sunken")
        self.label_pos.pack(side="left", padx=5)

    def agregar_nodo(self):
        try:
            valor = int(self.entry_valor.get())
            self.arbol.insertar(valor)
            self.actualizar_interfaz()
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar_nodo(self):
        try:
            valor = int(self.entry_valor.get())
            if self.arbol.buscar(valor):
                messagebox.showinfo("Resultado", f"El nodo {valor} existe en el árbol")
            else:
                messagebox.showwarning("Resultado", f"El nodo {valor} NO existe en el árbol")
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero")

    def limpiar_arbol(self):
        self.arbol = ArbolBinarioBusqueda()
        self.actualizar_interfaz()

    def actualizar_interfaz(self):
        self.label_pre.config(text=f"Preorden: {' '.join(map(str, self.arbol.preorden()))}")
        self.label_in.config(text=f"Inorden: {' '.join(map(str, self.arbol.inorden()))}")
        self.label_pos.config(text=f"Posorden: {' '.join(map(str, self.arbol.posorden()))}")

        self.ax.clear()
        self.ax.axis('off')
        G = nx.DiGraph()
        self._agregar_nodos_grafo(self.arbol.raiz, G)
        if self.arbol.raiz:
            pos = self._calcular_posiciones(self.arbol.raiz)
            nx.draw(G, pos, with_labels=True, ax=self.ax, node_color="lightblue", node_size=800, font_size=10)
        self.canvas.draw()

    def _agregar_nodos_grafo(self, nodo, G):
        if nodo:
            G.add_node(nodo.valor)
            if nodo.izq:
                G.add_edge(nodo.valor, nodo.izq.valor)
                self._agregar_nodos_grafo(nodo.izq, G)
            if nodo.der:
                G.add_edge(nodo.valor, nodo.der.valor)
                self._agregar_nodos_grafo(nodo.der, G)

    def _calcular_posiciones(self, nodo, x=0, y=0, nivel=1, posiciones=None):
        if posiciones is None:
            posiciones = {}
        posiciones[nodo.valor] = (x, -y)

        if nodo.izq:
            self._calcular_posiciones(nodo.izq, x - 1/(nivel+1), y + 1, nivel + 1, posiciones)
        if nodo.der:
            self._calcular_posiciones(nodo.der, x + 1/(nivel+1), y + 1, nivel + 1, posiciones)

        return posiciones

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
