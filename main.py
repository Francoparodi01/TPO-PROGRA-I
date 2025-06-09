from utils import login, mostrar_menu_principal, pedir_opcion, salir
from libros import menu_libros
from clientes import menu_clientes
from ventas import menu_ventas


def main():
    usuarios = {
        "vendedor1": "contra1",
        "vendedor2": "contra2"
    }

    libros = [
        {"id": 1, "titulo": "1984", "autor": "George Orwell", "categoria": "Ficcion", "precio": 4500.0, "stock": 10, "isbn": "", "estado": "disponible"},
        {"id": 2, "titulo": "Rayuela", "autor": "Julio Cortázar", "categoria": "Ficcion", "precio": 5000.0, "stock": 5, "isbn": "", "estado": "disponible"},
        {"id": 3, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "categoria": "Ficcion", "precio": 6000.0, "stock": 7, "isbn": "", "estado": "disponible"},
        {"id": 4, "titulo": "El principito", "autor": "Antoine de Saint-Exupéry", "categoria": "Infantil", "precio": 4000.0, "stock": 8, "isbn": "", "estado": "disponible"},
        {"id": 5, "titulo": "Fahrenheit 451", "autor": "Ray Bradbury", "categoria": "Ciencia", "precio": 4700.0, "stock": 6, "isbn": "", "estado": "disponible"},
        {"id": 6, "titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes", "categoria": "Historia", "precio": 7500.0, "stock": 4, "isbn": "", "estado": "disponible"},
        {"id": 7, "titulo": "Crónica de una muerte anunciada", "autor": "Gabriel García Márquez", "categoria": "Ficcion", "precio": 5000.0, "stock": 5, "isbn": "", "estado": "disponible"},
        {"id": 8, "titulo": "La metamorfosis", "autor": "Franz Kafka", "categoria": "Ficcion", "precio": 4200.0, "stock": 9, "isbn": "", "estado": "disponible"},
        {"id": 9, "titulo": "Orgullo y prejuicio", "autor": "Jane Austen", "categoria": "Ficcion", "precio": 4800.0, "stock": 3, "isbn": "", "estado": "disponible"},
        {"id": 10, "titulo": "El amor en los tiempos del cólera", "autor": "Gabriel García Márquez", "categoria": "Ficcion", "precio": 5900.0, "stock": 6, "isbn": "", "estado": "disponible"}
    ]

    clientes = [
        {"dni": "12345678", "nombre": "Juan", "apellido": "Pérez"},
        {"dni": "87654321", "nombre": "Ana", "apellido": "Gómez"}
    ]

    ventas = []
    facturas = []

    while True:
        usuario = login(usuarios)
        while True:
            mostrar_menu_principal(usuario)
            opcion = pedir_opcion("Seleccione una opción: ", [1, 2, 3, 4])

            if opcion == 1:
                menu_libros(libros, usuario)
            elif opcion == 2:
                menu_ventas(libros, clientes, ventas, facturas, usuario)
            elif opcion == 3:
                menu_clientes(clientes, usuario)
            elif opcion == 4:
                salir()
                break


if __name__ == "__main__":
    main()
