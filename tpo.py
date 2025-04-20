# Hito 1:
# - Matrices: Utilizar matrices para almacenar la información de los libros, donde cada fila representa un libro y 
# cada columna representa un atributo (título, autor, género, etc.). 
# Se pueden implementar funciones para buscar, modificar y eliminar libros de la matriz.
# - Tuplas: Utilizar tuplas para almacenar información inmutable, como los géneros de los libros 
# o las secciones de la biblioteca.
# - Rebanado y comprensión de listas: Utilizar rebanado para obtener subconjuntos de libros (por ejemplo,
# libros de un autor específico) y comprensión de listas para crear listas de libros que cumplan con ciertos criterios.
# - Cadenas de caracteres: Manipular cadenas de texto para validar entradas del usuario, como títulos y autores, 
# y para formatear la salida de los libros.
# - Diccionarios y conjuntos: Utilizar diccionarios para almacenar información de los libros, donde la clave sea el 
# título del libro y el valor sea un diccionario con los demás atributos. Utilizar conjuntos para manejar géneros
# y secciones sin duplicados, permitiendo operaciones como intersección o unión para filtrar libros por género o sección.





from datetime import datetime

def mostrar_menu():
    print("\nBienvenido a la librería")
    print("1. Agregar libro")
    print("2. Modificar libro")
    print("3. Buscar libro")
    print("4. Eliminar libro")
    print("5. Ver libros disponibles")
    print("6. Vender libro")
    print("7. Agregar cliente") 
    print("8. Ver clientes")
    print("9. Ver ventas realizadas")
    print("10. Ver facturas emitidas")
    print("11. Salir")

# Lista de libros como diccionarios
libros = [
    {"nombre": "El Principito", "autor": "Antoine de Saint-Exupéry", "precio": 3500, "stock": 5},
    {"nombre": "Rayuela", "autor": "Cortázar", "precio": 5000, "stock": 0},
    {"nombre": "Cien años de soledad", "autor": "Gabriel García Márquez", "precio": 6000, "stock": 3},
    {"nombre": "El túnel", "autor": "Ernesto Sabato", "precio": 4500, "stock": 4},
    {"nombre": "El Aleph", "autor": "Jorge Luis Borges", "precio": 3800, "stock": 1},
    {"nombre": "La casa de los espíritus", "autor": "Isabel Allende", "precio": 4900, "stock": 2},
]

clientes = [
    {"nombre": "Juan Pérez", "dni": "12345678", "tipo": "recurrente"},
    {"nombre": "María López", "dni": "87654321", "tipo": "nuevo"},
    {"nombre": "Carlos García", "dni": "11223344", "tipo": "recurrente"},
    {"nombre": "Ana Martínez", "dni": "44332211", "tipo": "nuevo"},
    {"nombre": "Pedro Fernández", "dni": "55667788", "tipo": "recurrente"},
    {"nombre": "Lucía González", "dni": "99887766", "tipo": "nuevo"},
]

ventas = []  # Lista de tuplas: (cliente, libro, precio)
facturas = []  # Lista de diccionarios con detalles de la factura
libros_vendidos = []
clientes_recurrentes = []
clientes_nuevos = []

contador_factura = 1  # Número de factura incremental

def agregar_libro():
    libro = input("Ingrese el nombre del libro: ")
    autor = input("Ingrese el autor del libro: ")
    precio = float(input("Ingrese el precio del libro: "))
    # Validación de entrada
    if not libro or not autor or precio <= 0:
        print("Error: Todos los campos son obligatorios y el precio debe ser mayor a 0.")
        return
        
    libros.append({"nombre": libro, "autor": autor, "precio": precio})
    print(f"Libro '{libro}' agregado con éxito.")

def modificar_libro():
    libro = input("Ingrese el nombre del libro a modificar: ")
    for i in range(len(libros)):
        if libros[i]["nombre"] == libro:
            nuevo_nombre = input("Ingrese el nuevo nombre del libro: ")
            nuevo_autor = input("Ingrese el nuevo autor del libro: ")
            nuevo_precio = float(input("Ingrese el nuevo precio del libro: "))
            libros[i] = {"nombre": nuevo_nombre, "autor": nuevo_autor, "precio": nuevo_precio}
            print(f"Libro '{libro}' modificado con éxito.")
            return
    print(f"Libro '{libro}' no encontrado.")

def buscar_libro():
    libro_a_buscar = input("Ingrese el nombre del libro a buscar: ")
    for libro in libros:
        if libro["nombre"].lower() == libro_a_buscar.lower():
            print(f"Libro encontrado: {libro}")
            return
    print(f"Libro '{libro_a_buscar}' no encontrado.")

def eliminar_libro():
    libro = input("Ingrese el nombre del libro a eliminar: ")
    for i in range(len(libros)):
        if libros[i]["nombre"] == libro:
            libros.pop(i)
            print(f"Libro '{libro}' eliminado con éxito.")
            return 
    print(f"Libro '{libro}' no encontrado.")

def ver_libros():
    if not libros:
        print("No hay libros disponibles.")
    else:
        print("Libros disponibles:")
        for libro in libros:
            print(f"Nombre: {libro['nombre']}, Autor: {libro['autor']}, Precio: {libro['precio']}")

def vender_libro():
    global contador_factura
    cliente = input("Ingrese el nombre del cliente: ").strip().capitalize()
    libro_nombre = input("Ingrese el nombre del libro a vender: ").strip()

    for i in range(len(libros)):
        if libros[i]["nombre"].lower() == libro_nombre.lower():
            precio = libros[i]["precio"]
            ventas.append((cliente, libros[i]["nombre"], precio))  # Registro de venta

            # Generamos la factura
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            factura = {
                "nro_factura": contador_factura,
                "cliente": cliente,
                "libro": libros[i]["nombre"],
                "precio": precio,
                "fecha": fecha
            }
            facturas.append(factura)
            contador_factura += 1

            # Actualizamos libros
            libros_vendidos.append(libros[i])
            libros.pop(i)

            print("Venta y factura generadas correctamente.")
            print("------ FACTURA ------")
            print(f"Factura N°: {factura['nro_factura']}")
            print(f"Cliente: {factura['cliente']}")
            print(f"Libro: {factura['libro']}")
            print(f"Precio: {factura['precio']}")
            print(f"Fecha: {factura['fecha']}")
            print("---------------------")
            return
    print("Libro no encontrado.")

def agregar_cliente():
    nombre_cliente = input("Ingrese el nombre del cliente: ").strip().capitalize()
    tipo_cliente = input("Ingrese el tipo de cliente (nuevo/recurrente): ").strip().lower()
    if tipo_cliente == "nuevo":
        clientes_nuevos.append(nombre_cliente)
    elif tipo_cliente == "recurrente":
        clientes_recurrentes.append(nombre_cliente)
    else:
        print("Tipo de cliente no válido.")
        return
    print(f"Cliente '{nombre_cliente}' agregado con éxito.")

def ver_clientes():
    if not clientes:
        print("No hay clientes disponibles.")
    else:
        print("Clientes disponibles:")
        for cliente in clientes:
            print(cliente)

def ver_ventas():
    if not ventas:
        print("No hay ventas registradas.")
    else:
        print("Ventas realizadas:")
        for venta in ventas:
            cliente, libro, precio = venta
            print(f"Cliente: {cliente} - Libro: {libro} - Precio: {precio}")

def ver_facturas():
    if not facturas:
        print("No hay facturas emitidas.")
    else:
        print("Facturas emitidas:")
        for f in facturas:
            print(f"N° {f['nro_factura']} - Cliente: {f['cliente']} - Libro: {f['libro']} - Precio: {f['precio']} - Fecha: {f['fecha']}")

# Bucle del menú principal
while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_libro()
    elif opcion == "2":
        modificar_libro()
    elif opcion == "3":
        buscar_libro()
    elif opcion == "4":
        eliminar_libro()
    elif opcion == "5":
        ver_libros()
    elif opcion == "6":
        vender_libro()
    elif opcion == "7":
        agregar_cliente()
    elif opcion == "8":
        ver_clientes()
    elif opcion == "9":
        ver_ventas()
    elif opcion == "10":
        ver_facturas()
    elif opcion == "11":
        print("Saliendo del programa...")
        break
    else:   
        print("Opción no válida. Intente nuevamente.")
