import random
from datetime import datetime

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


# Validador de opciones 
def pedir_opcion(mensaje, opciones_validas):
    """
    Pide una opción al usuario y valida que sea un número dentro de las opciones válidas.
    
    :param mensaje: str, el texto que se muestra al pedir la opción
    :param opciones_validas: lista o conjunto con los números válidos (ej: [1, 2, 3])
    :return: int, la opción elegida por el usuario
    """
    while True:
        try:
            opcion = int(input(mensaje))
            if opcion in opciones_validas:
                return opcion
            else:
                print("✖ Opción fuera de rango.")
        except ValueError:
            print("✖ Ingresá un número válido.")

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto.replace(" ", "").isalpha():
            return texto.title()
        else:
            print("✖ Ingresá solo letras (pueden tener espacios, pero no números ni símbolos).")


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
        print("7) Mostrar libros filtrado por precio")
        print("8) Reactivar libro dado de baja")
        print("9) Gestionar categorías")
        print("10) Volver")
        print("-" * 60)

        opcion = pedir_opcion("Seleccione una opción: ", list(range(1, 11)))

        if opcion == 1:
            agregar_libro(libros)
        elif opcion == 2:
            buscar_libro_ui(libros)
        elif opcion == 3:
            modificar_libro(libros)
        elif opcion == 4:
            ver_stock_total(libros)
        elif opcion == 5:
            eliminar_libro(libros)
        elif opcion == 6:
            mostrar_ultimos_libros(libros)
        elif opcion == 7:
            libros_baratos(libros)
        elif opcion == 8:
            reactivar_libro(libros)
        elif opcion == 9:
            menu_categorias()
        elif opcion == 10:
            break


                       
CATEGORIAS = {
    "Ficcion",
    "Ciencia",
    "Historia",
    "Infantil"
}

# Eliminado el menú de categorías
# Se crea uno nuevo modulado, por un lado el menu_ui y por otro las funciones de gestión de categorías

# Menú para gestionar categorías de libros
# categorias es un set, no una lista
CATEGORIAS = {"Ficcion", "Ciencia", "Historia", "Infantil"}

def obtener_categorias():
    return sorted(CATEGORIAS)

def agregar_categoria(nombre):
    if nombre in CATEGORIAS:
        return False
    CATEGORIAS.add(nombre)
    return True

def modificar_categoria(actual, nueva):
    if actual not in CATEGORIAS or nueva in CATEGORIAS:
        return False
    CATEGORIAS.remove(actual)
    CATEGORIAS.add(nueva)
    return True

def eliminar_categoria(nombre):
    if nombre not in CATEGORIAS or len(CATEGORIAS) == 1:
        return False
    CATEGORIAS.remove(nombre)
    return True


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

        opcion = pedir_opcion("Seleccione una opción: ", [1, 2, 3, 4])

        if opcion == 1:
            agregar_cliente(clientes)
        elif opcion == 2:
            eliminar_cliente(clientes)
        elif opcion == 3:
            ver_clientes(clientes)
        elif opcion == 4:
            break


# Menú para gestionar categorías de libros
def menu_categorias():
    while True:
        print("\n--- GESTIÓN DE CATEGORÍAS ---")
        print("1) Ver categorías")
        print("2) Agregar categoría")
        print("3) Modificar categoría")
        print("4) Eliminar categoría")
        print("5) Volver")

        opcion = pedir_opcion("Seleccione una opción: ", [1, 2, 3, 4, 5])

        if opcion == 1:
            print("\nCategorías disponibles:")
            for cat in obtener_categorias():
                print(f"- {cat}")

        elif opcion == 2:
            nueva = input("Ingrese nueva categoría: ").title()
            if agregar_categoria(nueva):
                print("✔ Categoría agregada.")
            else:
                print("✖ Ya existe esa categoría.")
            for cat in obtener_categorias():
                print(f"- {cat}")

        elif opcion == 3:
            actual = input("Categoría a modificar: ").title()
            nueva = input("Nuevo nombre: ").title()
            if modificar_categoria(actual, nueva):
                print("✔ Modificada correctamente.")
            else:
                print("✖ Error al modificar. Verifique los nombres.")
            for cat in obtener_categorias():
                print(f"- {cat}")

        elif opcion == 4:
            nombre = input("Categoría a eliminar: ").title()
            if eliminar_categoria(nombre):
                print("✔ Eliminada correctamente.")
            else:
                print("✖ No se pudo eliminar. ¿Existe o es la única?")
            for cat in obtener_categorias():
                print(f"- {cat}")

        elif opcion == 5:
            break

# ──────────────────── Funciones de Libros ────────────────────
# Agrega un libro con validación de categoría y duplicados
def agregar_libro(libros):
    print("\n" + "-" * 60)
    # Bucle para permitir agregar múltiples libros hasta escribir 'salir'
    titulo = pedir_texto("Título (o 'salir' para terminar): ")
    while titulo.lower() != "salir":
        autor = pedir_texto("Autor: ")
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
            categoria = pedir_texto(f"Categoría {CATEGORIAS}: ")
            while categoria not in CATEGORIAS:
                print("✖ Categoría inválida.")
                categoria = pedir_texto(f"Categoría {CATEGORIAS}: ")
            # Solicitar precio y stock, validando cada uno por separado
            while True:
                try:
                    precio = float(input("Precio: "))
                    if precio < 0:
                        print("✖ El precio debe ser positivo.")
                        continue
                    break
                except ValueError:
                    print("✖ Precio inválido. Ingrese un número válido.")
            while True:
                try:
                    stock = int(input("Stock: "))
                    if stock < 0:
                        print("✖ El stock debe ser positivo.")
                        continue
                    break
                except ValueError:
                    print("✖ Stock inválido. Ingrese un número entero.")
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
                "isbn": "",
                "estado": "disponible"
            })
            print(f"✔ Libro agregado con ID {nuevo_id}.")
        print("-" * 60)
        titulo = pedir_texto("Otro título (o 'salir'): ")

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

def buscar_libro_por_titulo(libros, titulo):
    for libro in libros:
        if libro["titulo"].lower() == titulo.lower():
            return libro
    return None


# Permite modificar atributos del libro seleccionado
def modificar_libro(libros):
    titulo = input("Título del libro a modificar: ").strip()
    libro = buscar_libro_por_titulo(libros, titulo)
    if not libro:
        print("No se encontró un libro con ese título.")
        return

    print("1) Título\n2) Autor\n3) Categoría\n4) Precio\n5) Stock")
    op = input("¿Qué desea modificar?: ")
    
    if op == "1":
        libro["titulo"] = input("Nuevo título: ").title()
    elif op == "2":
        libro["autor"] = input("Nuevo autor: ").title()
    elif op == "3":
        nueva_cat = input(f"Nueva categoría {CATEGORIAS}: ").title()
        if nueva_cat in CATEGORIAS:
            libro["categoria"] = nueva_cat
        else:
            print("✖ Categoría inválida.")
    elif op == "4":
        libro["precio"] = float(input("Nuevo precio: "))
    elif op == "5":
        libro["stock"] = int(input("Nuevo stock: "))
    else:
        print("✖ Opción inválida.")


# Elimina un libro de la lista si existe
def eliminar_libro(libros):
    id_lib = int(input("ID a dar de baja: "))
    libro = buscar_libro(libros, id_lib)
    if libro:
        libro["estado"] = "no disponible"
        print("✔ Libro marcado como no disponible.")
    else:
        print("No encontrado.")

def reactivar_libro(libros):
    print("\nLibros actualmente NO disponibles:")
    no_disponibles = [l for l in libros if l.get("estado") != "disponible"]

    if not no_disponibles:
        print("✔ Todos los libros están disponibles.")
        return  # No hace falta continuar

    for l in no_disponibles:
        print(f"ID:{l['id']} - {l['titulo']}")

    try:
        id_lib = int(input("Ingrese el ID del libro a reactivar: "))
    except ValueError:
        print("ID inválido.")
        return

    libro = buscar_libro(libros, id_lib)
    if libro:
        if libro.get("estado") == "disponible":
            print("El libro ya está disponible.")
        else:
            libro["estado"] = "disponible"
            print("✔ Libro reactivado correctamente.")
    else:
        print("Libro no encontrado.")

# Imprime el stock completo de libros con sus categorías
def ver_stock_total(libros):
    print("\n" + "-" * 60)
    print(" STOCK TOTAL ")
    print("-" * 60)
    for libro in libros:
        if libro.get("estado") != "disponible":
            continue  # Salta libros no disponibles
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


def es_libro_barato(libro, limite):
    return libro["precio"] < limite and libro.get("estado") == "disponible"

# Muestra libros con precio menor a $5000 usando comprensión de listas
def libros_baratos(libros):
    try:
        limite = float(input("Mostrar libros con precio menor a: $"))
    except ValueError:
        print("✖ Ingresá un número válido.")
        return

    baratos = [libro for libro in libros if es_libro_barato(libro, limite)]

    print("\n" + "-" * 60)
    print(f" LIBROS BARATOS (<${limite}) ")
    print("-" * 60)
    if baratos:
        for libro in baratos:
            print(f"{libro['titulo']} - ${libro['precio']}")
    else:
        print("No hay libros por debajo de ese precio.")
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
    if cliente:
        print(f"Bienvenido/a {cliente['nombre']} {cliente['apellido']}")

    if not cliente:
        print("Cliente no encontrado. Agregando nuevo cliente.")
        agregar_cliente(clientes, dni_cliente)
        cliente = buscar_cliente(clientes, dni_cliente)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    factura = {"Factura": len(facturas) + 1, "Fecha": fecha, "DNI": dni_cliente, "Libros": {}, "Total": 0}
    total = 0
    libros_vendidos = []  # Guardamos libros y cantidades para posible reversión
    venta_parcial_matriz = [["Título", "Cantidad", "Precio Unitario"]]

    while True:
        try:
            id_lib = int(input("ID del libro a vender (0 salir): "))
            if id_lib == 0:
                break

            libro = buscar_libro(libros, id_lib)
            if libro and libro["stock"] > 0 and libro.get("estado") == "disponible":
                cant = int(input("Cantidad: "))
                if 0 < cant <= libro["stock"]:
                    p = libro["precio"] * cant
                    ventas.append({"dni": dni_cliente, "id_libro": id_lib, "cantidad": cant, "precio_total": p})
                    factura["Libros"][id_lib] = {"Cantidad": cant, "Precio": p}
                    total += p
                    libro["stock"] -= cant
                    libros_vendidos.append((libro, cant))  # Guardamos para reversión
                    venta_parcial_matriz.append([libro["titulo"], cant, f"${libro['precio']}"])
                    print("\nTicket parcial:")
                    for fila in venta_parcial_matriz:
                        print(f"{str(fila[0]):<30} {str(fila[1]):<10} {str(fila[2]):<10}")
                else:
                    print("Cantidad inválida o sin stock suficiente.")
            else:
                print("ID inválido o libro fuera de stock o no disponible.")

        except ValueError:
            print("Por favor, ingrese un número válido para el ID o cantidad.")

    if factura["Libros"]:  # Si hay libros en la factura, preguntar si se confirma
        confirmar = input("¿Desea confirmar la compra? (S/N): ").strip().lower()

        if confirmar == "s":
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
        else:
            for libro, cantidad in libros_vendidos:
                libro["stock"] += cantidad  # Revertimos stock
            print("✔ Venta cancelada. No se registró ninguna factura.")
    else:
        print("No se realizó ninguna venta.")


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
    print("Sesión cerrada. Volviendo al login...")

# ──────────────────── Programa principal ────────────────────
def main():
    usuarios = {"vendedor1": "contra1", "vendedor2": "contra2"}
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
                    menu_libros(libros)
                elif opcion == 2:
                    menu_ventas(libros, clientes, ventas, facturas)
                elif opcion == 3:
                    menu_clientes(clientes)
                elif opcion == 4:
                    salir()
                    break 

main()
# Fin del programa