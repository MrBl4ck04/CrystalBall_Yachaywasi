import simpy
import random

class Libro:
    def __init__(self, titulo, autor, editorial, precio, isbn, stock_inicial, demanda, punto_reorden, cantidad_ordenar):
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.precio = precio
        self.isbn = isbn
        self.stock = stock_inicial
        self.demanda = demanda
        self.punto_reorden = punto_reorden
        self.cantidad_ordenar = cantidad_ordenar

def simulacion_libreria(env, libros):
    for libro in libros:
        yield env.process(ventas_libreria(env, libro))  # Agregar 'yield'

def ventas_libreria(env, libro):
    while True:
        yield env.timeout(1)  # Simula el tiempo entre ventas
        venta = random.randint(1, libro.demanda)
        if venta > libro.stock:
            venta = libro.stock
        libro.stock -= venta
        print(f"Venta de '{libro.titulo}': {venta}, Stock Actual: {libro.stock}")

        # Reordenar si es necesario
        if libro.stock <= libro.punto_reorden:
            ordenar = libro.cantidad_ordenar
            libro.stock += ordenar
            print(f"Reordenar '{libro.titulo}': {ordenar}, Stock Actual: {libro.stock}")

# Definir los datos para los 5 libros
libros_data = [
    {"titulo": "PEDRO PARAMO", "autor": "JUAN RULFO", "editorial": "CATEDRA", "precio": 95.00, "isbn": "9788437604183", "stock_inicial": 80, "demanda": 48, "punto_reorden": 6, "cantidad_ordenar": 12.649},
    {"titulo": "LEER PARA INVESTIGAR", "autor": "LUIS ROBERTO AMUSQUIVAR FERNANDEZ", "editorial": "CATACORA", "precio": 23.00, "isbn": "4-1-3762-15", "stock_inicial": 49, "demanda": 48, "punto_reorden": 6, "cantidad_ordenar": 12.649},
    {"titulo": "REBELION EN LA GRANJA", "autor": "GEORGE ORWELL", "editorial": "EDICIONES AMERICANAS", "precio": 65.00, "isbn": "9789962904915", "stock_inicial": 55, "demanda": 32, "punto_reorden": 4, "cantidad_ordenar": 10.328},
    {"titulo": "GENERACION IDIOTA", "autor": "AGUSTIN LAJE", "editorial": "HOJAS DEL SUR", "precio": 195.00, "isbn": "9789878916347", "stock_inicial": 43, "demanda": 30, "punto_reorden": 3.75, "cantidad_ordenar": 10.000},
    {"titulo": "48 LEYES DEL PODER, LAS", "autor": "ROBERT GREENE", "editorial": "OCEANO", "precio": 228.00, "isbn": "9786075276915", "stock_inicial": 36, "demanda": 28, "punto_reorden": 3.5, "cantidad_ordenar": 9.661}
]

# Configurar la simulación
env = simpy.Environment()
libros = [Libro(**data) for data in libros_data]

# Iniciar la simulación
env.process(simulacion_libreria(env, libros))
env.run(until=50)  # Establecer un límite de tiempo para la simulación
