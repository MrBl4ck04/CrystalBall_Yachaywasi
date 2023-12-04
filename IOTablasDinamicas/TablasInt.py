import tkinter as tk
from tkinter import ttk
import pandas as pd
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

        # Button for "Longitud del ciclo"
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, pady=10)

        ciclo_button = ttk.Button(button_frame, text="Longitud del ciclo", command=self.calcular_longitud_del_ciclo)
        ciclo_button.pack(side=tk.LEFT)

        # Button for "Costo de pedir por ciclo"
        costo_button = ttk.Button(button_frame, text="Costo de pedir por ciclo", command=self.calcular_costo_por_ciclo)
        costo_button.pack(side=tk.LEFT)

        # Button for "Nivel promedio de inventario"
        nivel_button = ttk.Button(button_frame, text="Nivel promedio de inventario", command=self.calcular_nivel_promedio_inventario)
        nivel_button.pack(side=tk.LEFT)

        # Button for "Costo por unidad de tiempo"
        costo_unidad_button = ttk.Button(button_frame, text="Costo por unidad de tiempo", command=self.calcular_costo_por_unidad_de_tiempo)
        costo_unidad_button.pack(side=tk.LEFT)

    def calcular_longitud_del_ciclo(self):
        # Leer el archivo Excel
        df = pd.read_excel(self.excel_path)

        # Realizar el cálculo de la "Longitud del ciclo"
        df["Longitud del ciclo"] = df["Cantidad a ordenar Q*"] / df["Ventas en un mes (demanda)"]

        # Actualizar la Treeview con las nuevas columnas y encabezados
        self.update_treeview(df)

    def calcular_costo_por_ciclo(self):
        # Leer el archivo Excel
        df = pd.read_excel(self.excel_path)

        # Realizar el cálculo del "Costo de pedir por ciclo"
        df["Costo de pedir por ciclo"] = (df["Costo preparación 5%"] + df["Costo"]) * df["Cantidad a ordenar Q*"]

        # Actualizar la Treeview con las nuevas columnas y encabezados
        self.update_treeview(df)

    def calcular_nivel_promedio_inventario(self):
        # Leer el archivo Excel
        df = pd.read_excel(self.excel_path)

        # Realizar el cálculo del "Nivel promedio de inventario"
        df["Nivel promedio de inventario"] = (df["Cantidad a ordenar Q*"] / 2)

        # Actualizar la Treeview con las nuevas columnas y encabezados
        self.update_treeview(df)

    def calcular_costo_por_unidad_de_tiempo(self):
        # Leer el archivo Excel
        df = pd.read_excel(self.excel_path)

        # Realizar el cálculo del "Costo por unidad de tiempo"
        df["Costo por unidad de tiempo"] = (df["Mantenimiento 10%"] * df["Cantidad a ordenar Q*"]) / 2

        # Actualizar la Treeview con las nuevas columnas y encabezados
        self.update_treeview(df)

    def update_treeview(self, df):
        # Obtener todas las columnas después de agregar las nuevas
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
        self.tree.update_idletasks()
        self.scrollbar_x.config(command=self.canvas.xview)


if __name__ == "__main__":
    excel_path = "C:/Users/Claudia Teran/Desktop/Universidad/Inv. Operativa II/LIbreria_Prueba2.xlsx"

    root = tk.Tk()
    app = ExcelViewerApp(root, excel_path)
    root.mainloop()
