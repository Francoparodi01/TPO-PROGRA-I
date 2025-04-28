import random
from datetime import datetime

CATEGORIAS = ("Ficcion", "Ciencia", "Historia", "Infantil")

# ──────────────────── Funciones auxiliares ────────────────────
# Función de login: valida usuario y contraseña
def login(usuarios):
    print("=" * 60)
    print("SISTEMA DE LIBRERÍA")
    print("=" * 60)
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    # Bucle hasta que las credenciales sean correctas
    while usuario not in usuarios or usuarios[usuario] != contrasena:
        print("\nUsuario o contraseña incorrectos. Intente nuevamente.\n")
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")
    return usuario  # Devuelve el usuario autenticado

# Muestra el menú principal con opciones básicas
def mostrar_menu_principal(usuario):
    print("\n" + "-" * 60)
    print(f"Bienvenido, {usuario}")
    print("-" * 60)
    print("1) Libros")
    print("2) Ventas")
    print("3) Clientes")
    print("4) Salir")
    print("-" * 60)

# ──────────────────── Menús secundarios ────────────────────
# Menú para operaciones sobre libros
# Menú para operaciones sobre libros
def menu_libros(libros):
    while True:
        print("\n" + "*" * 60)
        print("MENÚ LIBROS")
        print("*" * 60)
        print("1) Agregar libro")
        print("2) Buscar libro por ID")
        print("3) Modificar libro")
        print("4) Ver stock total")
        print("5) Eliminar libro")
        print("6) Mostrar últimos libros agregados")
        print("7) Mostrar libros baratos (<$5000)")  # Nueva opción
        print("8) Volver")
        print("-" * 60)
        opcion = input("Seleccione una opción: ")
        # Lógica de selección según la opción ingresada
        if opcion == "1":
            agregar_libro(libros)
        elif opcion == "2":
            buscar_libro_ui(libros)
        elif opcion == "3":
            modificar_libro(libros)
        elif opcion == "4":
            ver_stock_total(libros)
        elif opcion == "5":
            eliminar_libro(libros)
        elif opcion == "6":
            mostrar_ultimos_libros(libros)
        elif opcion == "7":
            libros_baratos(libros)  
        elif opcion == "8":
            break  # Salir del menú libros
        else:
            print("Opción inválida.")


# Menú para ventas y facturas
def menu_ventas(libros, clientes, ventas, facturas):
    while True:
        print("\n" + "*" * 60)
        print("MENÚ VENTAS")
        print("*" * 60)
        print("1) Vender libro")
        print("2) Ver ventas realizadas")
        print("3) Ver facturas emitidas")
        print("4) Volver")
        print("-" * 60)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            vender_libro(libros, clientes, ventas, facturas)
        elif opcion == "2":
            ver_ventas_realizadas(ventas)
        elif opcion == "3":
            ver_facturas_emitidas(facturas)
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")

# Menú para gestión de clientes
def menu_clientes(clientes):
    while True:
        print("\n" + "*" * 60)
        print("MENÚ CLIENTES")
        print("*" * 60)
        print("1) Agregar cliente")
        print("2) Eliminar cliente")
        print("3) Ver clientes")
        print("4) Volver")
        print("-" * 60)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_cliente(clientes)
        elif opcion == "2":
            eliminar_cliente(clientes)
        elif opcion == "3":
            ver_clientes(clientes)
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")

# ──────────────────── Funciones de Libros ────────────────────
# Agrega un libro con validación de categoría y duplicados
def agregar_libro(libros):
    print("\n" + "-" * 60)
    # Bucle para permitir agregar múltiples libros hasta escribir 'salir'
    titulo = input("Título (o 'salir' para terminar): ").title()
    while titulo.lower() != "salir":
        autor = input("Autor: ").title()
        # Control de duplicados usando for
        existe = False
        for libro in libros:
            if libro["titulo"] == titulo and libro["autor"] == autor:
                existe = True
                break
        if existe:
            print("✖ Ya existe ese libro.")
        else:
            # Pedir categoría usando la tupla CATEGORIAS
            categoria = input(f"Categoría {CATEGORIAS}: ").title()
            while categoria not in CATEGORIAS:
                print("✖ Categoría inválida.")
                categoria = input(f"Categoría {CATEGORIAS}: ").title()
            # Solicitar precio y stock
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))
            # Generar ID único evitando colisiones
            nuevo_id = generar_id_unico(libros)
            # Agregar el diccionario del libro
            libros.append({
                "id": nuevo_id,
                "titulo": titulo,
                "autor": autor,
                "categoria": categoria,
                "precio": precio,
                "stock": stock,
                "isbn": ""
            })
            print(f"✔ Libro agregado con ID {nuevo_id}.")
        print("-" * 60)
        titulo = input("Otro título (o 'salir'): ").title()

# Genera un ID único revisando un set de IDs existentes
def generar_id_unico(libros):
    ids = set() # Usamos un set para evitar duplicados
    for libro in libros:
        ids.add(libro["id"])
    nuevo = random.randint(10000, 99999)
    while nuevo in ids:
        nuevo = random.randint(10000, 99999)
    return nuevo

# Busca un libro por ID y lo devuelve o None si no existe
def buscar_libro(libros, id_libro):
    for libro in libros:
        if libro["id"] == id_libro:
            return libro
    return None

# Interfaz de búsqueda de libro
def buscar_libro_ui(libros): #user interface
    id_lib = int(input("ID a buscar: "))
    libro = buscar_libro(libros, id_lib)
    print(libro if libro else "No encontrado.") 

# Permite modificar atributos del libro seleccionado
def modificar_libro(libros):
    id_lib = int(input("ID a modificar: "))
    libro = buscar_libro(libros, id_lib)
    if not libro:
        print("No existe.")
        return
    print("1) Título\n2) Autor\n3) Categoría\n4) Precio\n5) Stock")
    op = input("Opción: ")
    if op == "1":
        libro["titulo"] = input("Nuevo título: ").title()
    elif op == "2":
        libro["autor"] = input("Nuevo autor: ").title()
    elif op == "3":
        cat = input(f"Categoría {CATEGORIAS}: ").title()
        if cat in CATEGORIAS:
            libro["categoria"] = cat
        else:
            print("Categoría inválida.")
    elif op == "4":
        libro["precio"] = float(input("Nuevo precio: "))
    elif op == "5":
        libro["stock"] = int(input("Nuevo stock: "))
    else:
        print("Opción inválida.")

# Elimina un libro de la lista si existe
def eliminar_libro(libros):
    id_lib = int(input("ID a eliminar: "))
    libro = buscar_libro(libros, id_lib)
    if libro:
        libros.remove(libro)
        print("✔ Eliminado.")
    else:
        print("No encontrado.")

# Imprime el stock completo de libros con sus categorías
def ver_stock_total(libros):
    print("\n" + "-" * 60)
    print(" STOCK TOTAL ")
    print("-" * 60)
    for libro in libros:
        # Usamos el método get para evitar KeyError si la clave no existe
        categoria = libro.get("categoria", "Sin categoría")
        print(
            f"ID:{libro['id']:>5} | "
            f"{libro['titulo']:<30} | "
            f"Categoría:{categoria:<15} | "
            f"Stock:{libro['stock']:>3}"
        )
    print("-" * 60)


# Muestra los últimos N libros usando slicing
def mostrar_ultimos_libros(libros):
    if not libros:
        print("No hay libros.")
        return
    n = int(input("¿Cuántos últimos mostrar? "))
    n = max(1, min(n, len(libros)))  # Asegura al menos 1 y como máximo la longitud
    print("\n" + "-" * 60)
    print(f"Últimos {n} libros")
    # Rebanado para obtener últimos n elementos
    for libro in libros[-n:]:
        print(f"ID:{libro['id']:>5} | {libro['titulo']} ({libro['categoria']})")
    print("-" * 60)

# Muestra libros con precio menor a $5000 usando comprensión de listas
def libros_baratos(libros):
    baratos = [libro for libro in libros if libro["precio"] < 5000]  # Usamos comprensión de listas
    print("\n" + "-" * 60)
    print(" LIBROS BARATOS (<$5000) ")
    print("-" * 60)
    if baratos:
        for libro in baratos:
            print(f"{libro['titulo']} - ${libro['precio']}")
    else:
        print("No hay libros baratos.")
    print("-" * 60)


# ──────────────────── Funciones de Clientes ────────────────────
# Busca cliente por DNI utilizando for
def buscar_cliente(clientes, dni):
    for cli in clientes:
        if cli["dni"] == dni:
            return cli
    return None

# Agrega cliente
def agregar_cliente(clientes, dni=None):
    print("\n" + "-" * 60)
    print(" AGREGAR CLIENTE ")
    print("-" * 60)

    if dni is None or not (dni.isdigit() and len(dni) == 8):
        dni = input("DNI (8 dígitos): ").strip()
        while not (dni.isdigit() and len(dni) == 8):
            print("✖ DNI inválido. Debe ser numérico y tener 8 dígitos.")
            dni = input("DNI (8 dígitos): ").strip()

    if buscar_cliente(clientes, dni):
        print("✖ DNI ya existente en el sistema.")
        return

    nombre = input("Nombre: ").strip().title()
    while nombre == "":
        print("✖ Nombre no puede ser vacío.")
        nombre = input("Nombre: ").strip().title()

    apellido = input("Apellido: ").strip().title()
    while apellido == "":
        print("✖ Apellido no puede ser vacío.")
        apellido = input("Apellido: ").strip().title()

    clientes.append({"dni": dni, "nombre": nombre, "apellido": apellido})

    print("-" * 60)
    print(f"Cliente agregado: DNI:{dni} | {nombre} {apellido}")
    print("-" * 60)


# Elimina cliente por DNI si existe
def eliminar_cliente(clientes):
    dni = input("DNI a eliminar: ")
    cli = buscar_cliente(clientes, dni)
    if cli:
        clientes.remove(cli)
        print("✔ Cliente eliminado.")
    else:
        print("No encontrado.")

# Muestra todos los clientes
def ver_clientes(clientes):
    print("\n" + "-" * 60)
    print(" CLIENTES ")
    print("-" * 60)
    for c in clientes:
        print(f"DNI:{c['dni']:>10} | {c['nombre']} {c['apellido']}")
    print("-" * 60)

# ──────────────────── Funciones de Ventas ────────────────────
# Registra venta múltiple y genera factura estructurada
def vender_libro(libros, clientes, ventas, facturas):
    dni_cliente = input("DNI del cliente: ")
    cliente = buscar_cliente(clientes, dni_cliente)
    
    if not cliente:
        print("Cliente no encontrado. Agregando nuevo cliente.")
        agregar_cliente(clientes, dni_cliente)
        cliente = buscar_cliente(clientes, dni_cliente)
    
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    factura = {"Factura": len(facturas) + 1, "Fecha": fecha, "DNI": dni_cliente, "Libros": {}, "Total": 0}
    total = 0

    venta_parcial_matriz = [["Título", "Cantidad", "Precio Unitario"]]
    
    while True:
        try:
            id_lib = int(input("ID del libro a vender (0 salir): "))
            if id_lib == 0:
                break
            
            libro = buscar_libro(libros, id_lib)
            if libro and libro["stock"] > 0: #si existe y hay stock
                cant = int(input("Cantidad: "))
                if 0 < cant <= libro["stock"]:
                    p = libro["precio"] * cant
                    ventas.append({"dni": dni_cliente, "id_libro": id_lib, "cantidad": cant, "precio_total": p})
                    factura["Libros"][id_lib] = {"Cantidad": cant, "Precio": p}
                    total += p
                    libro["stock"] -= cant
                    venta_parcial_matriz.append([libro["titulo"], cant, f"${libro['precio']}"])
                    print("\nTicket parcial:")
                    for fila in venta_parcial_matriz:
                        print(f"{str(fila[0]):<30} {str(fila[1]):<10} {str(fila[2]):<10}")
                else:
                    print("Cantidad inválida o sin stock suficiente.")
            else:
                print("ID inválido o libro fuera de stock.")
        
        except ValueError:
            print("Por favor, ingrese un número válido para el ID o cantidad.")

    if factura["Libros"]:  # si hay libros vendidos, se genera la factura
        factura["Total"] = total
        facturas.append(factura)

        print("\n" + "-" * 60)
        print(" FACTURA EMITIDA ")
        print(f"N°:{factura['Factura']}  Fecha:{factura['Fecha']}  DNI:{factura['DNI']}")
        print("Libro/s:")
        for libroid, dato in factura["Libros"].items(): 
            titulo_lib = buscar_libro(libros, libroid)["titulo"]
            print(f"- {titulo_lib} (ID {libroid}) | Cant: {dato['Cantidad']} | Precio: ${dato['Precio']:.2f}")
        print(f"TOTAL: ${factura['Total']:.2f}")
        print("-" * 60)
    else: #sino se imprime un mensaje de error
        print("\n No se realizó ninguna venta.")

# Mostrar ventas pasadas
def ver_ventas_realizadas(ventas):
    print("\n" + "-" * 60)
    print(" VENTAS REALIZADAS ")
    print("-" * 60)
    for v in ventas:
        print(v)
    print("-" * 60)

# Mostrar todas las facturas
def ver_facturas_emitidas(facturas):
    print("\n" + "-" * 60)
    print(" FACTURAS EMITIDAS ")
    print("-" * 60)
    for f in facturas:
        print(f)
        print("-" * 60)

# Sale del programa
def salir():
    print("Saliendo...")
    exit()

# ──────────────────── Programa principal ────────────────────
def main():
    usuarios = {"vendedor1": "contra1", "vendedor2": "contra2"}
    libros = [
    {"id": 1, "titulo": "1984","autor": "George Orwell","categoria": "Ficcion","precio": 4500.0, "stock": 10, "isbn": ""},
    {"id": 2, "titulo": "Rayuela","autor": "Julio Cortázar","categoria": "Ficcion","precio": 5000.0, "stock": 5,"isbn": ""},
    {"id": 3, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez",  "categoria": "Ficcion","precio": 6000.0, "stock": 7,  "isbn": ""},
    {"id": 4, "titulo": "El principito","autor": "Antoine de Saint-Exupéry","categoria": "Infantil","precio": 4000.0, "stock": 8,  "isbn": ""},
    {"id": 5, "titulo": "Fahrenheit 451","autor": "Ray Bradbury","categoria": "Ciencia","precio": 4700.0,"stock": 6,"isbn": ""},
    {"id": 6, "titulo": "Don Quijote de la Mancha","autor": "Miguel de Cervantes","categoria": "Historia","precio": 7500.0, "stock": 4,  "isbn": ""},
    {"id": 7, "titulo": "Crónica de una muerte anunciada","autor": "Gabriel García Márquez","categoria": "Ficcion","precio": 5000.0, "stock": 5,  "isbn": ""},
    {"id": 8, "titulo": "La metamorfosis","autor": "Franz Kafka","categoria": "Ficcion","precio": 4200.0, "stock": 9,"isbn": ""},
    {"id": 9, "titulo": "Orgullo y prejuicio","autor": "Jane Austen","categoria": "Ficcion","precio": 4800.0, "stock": 3,"isbn": ""},
    {"id": 10,"titulo": "El amor en los tiempos del cólera","autor": "Gabriel García Márquez","categoria": "Ficcion","precio": 5900.0, "stock": 6,  "isbn": ""}
]

    clientes = [
        {"dni": "12345678", "nombre": "Juan", "apellido": "Pérez"},
        {"dni": "87654321", "nombre": "Ana", "apellido": "Gómez"}
    ]
    ventas = []
    facturas = []

    usuario = login(usuarios)
    while True:
        mostrar_menu_principal(usuario)
        opcion = input("Opción: ")
        if opcion == "1":
            menu_libros(libros)
        elif opcion == "2":
            menu_ventas(libros, clientes, ventas, facturas)
        elif opcion == "3":
            menu_clientes(clientes)
        elif opcion == "4":
            salir()
        else:
            print("Opción inválida.")

main()

# Fin del programa