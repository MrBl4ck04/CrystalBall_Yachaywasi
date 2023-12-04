import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import plotly.express as px
import numpy as np

class ExcelViewerApp:
    def __init__(self, root, excel_path):
        self.root = root
        self.root.title("Excel")

        self.excel_path = excel_path

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas = tk.Canvas(self.frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.tree_frame = ttk.Frame(self.canvas)
        self.tree_frame.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.canvas.create_window((0, 0), window=self.tree_frame, anchor="nw")
        self.tree_frame.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure(canvas))

        self.create_widgets()

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def create_widgets(self):
        df = pd.read_excel(self.excel_path)

        # Configurar columnas
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree["columns"] = tuple(df.columns)
        for column in df.columns:
            self.tree.column(column, anchor="center", width=100)
            self.tree.heading(column, text=column)

        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar datos a Treeview
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=tuple(row))

        # Button to calculate and show "Punto de Reorden"
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)

        calculate_button = ttk.Button(button_frame, text="Calcular Punto de Reorden", command=self.calculate_punto_de_reorden)
        calculate_button.pack()

        # Button for "Calculo Provisional"
        provisional_button = ttk.Button(button_frame, text="Cantidad a Ordenar Q*", command=self.cantidad_a_ordenar)
        provisional_button.pack(side=tk.LEFT)

    def calculate_punto_de_reorden(self):
        # Leer el archivo Excel
        df = pd.read_excel(self.excel_path)

        # Realizar el cálculo y agregar la nueva columna "Punto de Reorden"
        df["Punto de Reorden"] = df["Ventas en un mes (demanda)"] * 1

        # Obtener todas las columnas después de agregar "Punto de Reorden"
        all_columns = df.columns

        # Actualizar la Treeview con las nuevas columnas y encabezados
        self.tree["columns"] = tuple(all_columns)
        for column in all_columns:
            # Establecer un ancho más angosto para las columnas
            self.tree.column(column, anchor="center", width=50)
            self.tree.heading(column, text=column)

        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar datos a Treeview
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=tuple(row))

        # Ajustar la barra de desplazamiento horizontal
        self.tree.update_idletasks()  # Asegurar que la Treeview se actualiza antes de configurar la barra de desplazamiento
        self.scrollbar_x.config(command=self.canvas.xview)

    def show_bar_settings(self):
        # Aquí puedes implementar la lógica para mostrar configuraciones adicionales antes de trazar el gráfico de barras
        pass

    def cantidad_a_ordenar(self):
        # Leer el archivo Excel
        df = pd.read_excel(self.excel_path)

        # Realizar el cálculo provisional y agregar la nueva columna "Calculo Provisional"
        # Calcula la parte interna de la fórmula
        internal_calculation = 2 * df["Ventas en un mes (demanda)"] * df["Costo preparación 5% (k)"] / df[
            "Mantenimiento 10% (h)"]

        # Aplica la raíz cuadrada solo a los valores no negativos usando una función lambda
        df["Cantidad a ordenar Q*"] = internal_calculation.apply(lambda x: np.sqrt(max(0, x)) if pd.notnull(x) else 0)

        # Obtener todas las columnas después de agregar "Calculo Provisional"
        all_columns = df.columns

        # Actualizar la Treeview con las nuevas columnas y encabezados
        self.tree["columns"] = tuple(all_columns)
        for column in all_columns:
            # Establecer un ancho más angosto para las columnas
            self.tree.column(column, anchor="center", width=50)
            self.tree.heading(column, text=column)

        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar datos a Treeview
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=tuple(row))

        # Ajustar la barra de desplazamiento horizontal
        self.tree.update_idletasks()  # Asegurar que la Treeview se actualiza antes de configurar la barra de desplazamiento
        self.scrollbar_x.config(command=self.canvas.xview)


if __name__ == "__main__":
    excel_path = "C:/Users/Claudia Teran/Desktop/Universidad/Inv. Operativa II/LIbreria_Prueba.xlsx"

    root = tk.Tk()
    app = ExcelViewerApp(root, excel_path)
    root.mainloop()