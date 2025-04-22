from datetime import datetime

# Tupla para géneros inmutables
generos_disponibles = ("Ficción", "Drama", "Romance", "Ciencia Ficción", "Terror", "Fantasía")
secciones_biblioteca = ("Literatura", "Ciencias", "Historia", "Infantil")

# Conjunto para evitar géneros duplicados (si se usan más adelante)
generos = set(generos_disponibles)

# Diccionario de libros (clave = título, valor = dict de atributos)
libros = {
    "El Principito": {"autor": "Antoine de Saint-Exupéry", "precio": 3500, "stock": 5},
    "Rayuela": {"autor": "Cortázar", "precio": 5000, "stock": 0},
    "Cien años de soledad": {"autor": "Gabriel García Márquez", "precio": 6000, "stock": 3},
    "El túnel": {"autor": "Ernesto Sabato", "precio": 4500, "stock": 4},
    "El Aleph": {"autor": "Jorge Luis Borges", "precio": 3800, "stock": 1},
    "La casa de los espíritus": {"autor": "Isabel Allende", "precio": 4900, "stock": 2},
}

clientes = {
    "12345678": {"nombre": "Juan Pérez", "tipo": "recurrente"},
    "87654321": {"nombre": "María López", "tipo": "nuevo"},
    "11223344": {"nombre": "Carlos García", "tipo": "recurrente"},
    "44332211": {"nombre": "Ana Martínez", "tipo": "nuevo"},
    "55667788": {"nombre": "Pedro Fernández", "tipo": "recurrente"},
    "99887766": {"nombre": "Lucía González", "tipo": "nuevo"},
}

ventas = []  # Lista de tuplas: (cliente, libro, precio)
facturas = []  # Lista de diccionarios
contador_factura = 1


def mostrar_menu():
    print("\n--- Librería ---")
    print("1. Agregar libro")
    print("2. Modificar libro")
    print("3. Buscar libro")
    print("4. Eliminar libro")
    print("5. Ver libros disponibles")
    print("6. Vender libro")
    print("7. Ver clientes")
    print("8. Ver ventas realizadas")
    print("9. Ver facturas emitidas")
    print("10. Buscar libro por autor")
    print("11. Filtrar por precio")
    print("12. Salir")

def agregar_libro():
    titulo = input("Ingrese el nombre del libro: ").strip().title()
    if titulo in libros:
        print("Ese libro ya existe.")
        return
    autor = input("Ingrese el autor: ").strip().title()
    precio = float(input("Ingrese el precio: "))
    stock = int(input("Ingrese el stock: "))
    libros[titulo] = {"autor": autor, "precio": precio, "stock": stock}
    print(f"Libro '{titulo}' agregado correctamente.")

def modificar_libro():
    titulo = input("Libro a modificar: ").strip().title()
    if titulo not in libros:
        print("Libro no encontrado.")
        return
    autor = input("Nuevo autor: ").strip().title()
    precio = float(input("Nuevo precio: "))
    stock = int(input("Nuevo stock: "))
    libros[titulo] = {"autor": autor, "precio": precio, "stock": stock}
    print("Libro modificado con éxito.")

def buscar_libro():
    titulo = input("Buscar libro: ").strip().title()
    libro = libros.get(titulo)
    if libro:
        print(f"{titulo}: {libro}")
    else:
        print("Libro no encontrado.")

def eliminar_libro():
    titulo = input("Eliminar libro: ").strip().title()
    if titulo in libros:
        del libros[titulo]
        print("Libro eliminado.")
    else:
        print("Libro no encontrado.")

def ver_libros():
    if libros:
        print("Libros disponibles:")
        for titulo, datos in libros.items():
            print(f"{titulo} - Autor: {datos['autor']}, Precio: ${datos['precio']}, Stock: {datos['stock']}")
    else:
        print("No hay libros cargados.")

def vender_libro():
    global contador_factura
    dni = input("Ingrese DNI del cliente: ").strip()
    cliente = clientes.get(dni)

    if not cliente:
        print("Cliente no registrado. Completando formulario...")
        dni, nombre = formulario_cliente()
        guardar_cliente(dni, nombre)
        cliente = clientes[dni]

    titulo = input("Nombre del libro: ").strip().title()

    if titulo in libros:
        libro = libros[titulo]
        stock_disponible = libro["stock"]
        precio_unitario = libro["precio"]

        print(f"Stock disponible: {stock_disponible}")
        try:
            cantidad = int(input("¿Cuántos ejemplares desea llevar?: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            return

        if cantidad <= 0:
            print("La cantidad debe ser mayor a cero.")
            return

        if cantidad <= stock_disponible:
            total_precio = precio_unitario * cantidad
            libro["stock"] -= cantidad

            # Actualizar contador de compras
            cliente.setdefault("compras", 0)
            cliente["compras"] += cantidad

            if cliente["compras"] > 3:
                cliente["tipo"] = "recurrente"

            factura = {
                "nro_factura": contador_factura,
                "cliente": cliente["nombre"],
                "libro": titulo,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "total": total_precio,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            facturas.append(factura)
            contador_factura += 1

            print("-------------------------")
            print("Factura generada:")
            for clave, valor in factura.items():
                print(f"{clave}: {valor}")
        else:
            print("No hay suficiente stock para completar la venta.")
    else:
        print("Libro no disponible.")



def buscar_por_autor():
    autor = input("Buscar por autor: ").strip().title()
    resultados = [titulo for titulo, datos in libros.items() if datos["autor"] == autor]
    if resultados:
        print("Libros del autor:")
        for t in resultados:
            print(t)
    else:
        print("No se encontraron libros de ese autor.")

def libros_baratos():
    limite = float(input("Mostrar libros con precio menor a: $"))
    encontrados = [f"{titulo} (${datos['precio']})" for titulo, datos in libros.items() if datos["precio"] < limite]
    print("\n".join(encontrados) if encontrados else "No hay libros en ese rango.")

def formulario_cliente():
    dni = input("DNI del cliente: ").strip()
    nombre = input("Nombre del cliente: ").strip().title()
    return dni, nombre

def guardar_cliente(dni, nombre):
    clientes[dni] = {"nombre": nombre, "tipo": "nuevo", "compras": 0}
    print(f"Cliente '{nombre}' registrado como nuevo.")


def ver_clientes():
    if not clientes:
        print("No hay clientes.")
    else:
        print("Clientes registrados:")
        for dni, data in clientes.items():
            print(f"{data['nombre']} (DNI: {dni}, Tipo: {data['tipo']})")

def ver_ventas():
    if not ventas:
        print("No hay ventas.")
    else:
        for cliente, libro, precio in ventas:
            print(f"{cliente} compró '{libro}' por ${precio}")

def ver_facturas():
    if not facturas:
        print("No hay facturas.")
    else:
        for f in facturas[-10:]:  # Últimas 10 facturas (rebanado)
            print(f"Factura #{f['nro_factura']}: {f['cliente']} compró '{f['libro']}' por ${f['precio']} el {f['fecha']}")

#Bucle principal del programa
salir = False
while not salir:
    mostrar_menu()
    opcion = input("Opción: ").strip()

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
        ver_clientes()
    elif opcion == "8":
        ver_ventas()
    elif opcion == "9":
        ver_facturas()
    elif opcion == "10":
        buscar_por_autor()
    elif opcion == "11":
        libros_baratos()
    elif opcion == "12": 
        # Salir del programa
        print("Saliendo...")
        salir = True
    else:
        print("Opción inválida.")
