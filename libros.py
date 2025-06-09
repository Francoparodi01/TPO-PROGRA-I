import random
import re 

from utils import pedir_texto, pedir_opcion, registrar_log

CATEGORIAS = ("Ficcion", "Ciencia", "Historia", "Infantil")

def menu_libros(libros, usuario):
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
            agregar_libro(libros, usuario)
        elif opcion == 2:
            buscar_libro_ui(libros, usuario)
        elif opcion == 3:
            modificar_libro(libros, usuario)
        elif opcion == 4:
            ver_stock_total(libros, usuario)
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

def validar_isbn(isbn):
    patron = r"^\d{3}-\d{10}$"
    return bool(re.match(patron, isbn))

def agregar_libro(libros, usuario):
    print("\n" + "-" * 60)
    titulo = pedir_texto("Título (o 'salir' para terminar): ")
    while titulo.lower() != "salir":
        autor = pedir_texto("Autor: ")
        existe = any(libro for libro in libros if libro["titulo"] == titulo and libro["autor"] == autor)
        if existe:
            print("✖ Ya existe ese libro.")
        else:
            categoria = pedir_texto(f"Categoría {CATEGORIAS}: ")
            while categoria not in CATEGORIAS:
                print("✖ Categoría inválida.")
                categoria = pedir_texto(f"Categoría {CATEGORIAS}: ")
            try:
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))
                if precio < 0 or stock < 0:
                    raise ValueError
            except ValueError:
                print("✖ Datos inválidos. Precio y stock deben ser positivos.")
                continue
            isbn = input("ISBN (formato 000-0000000000): ")
            while not validar_isbn(isbn):
                print("✖ Formato inválido.")
                isbn = input("ISBN (formato 000-0000000000): ")

            nuevo_id = generar_id_unico(libros)
            libro_nuevo = {
                "id": nuevo_id,
                "titulo": titulo,
                "autor": autor,
                "categoria": categoria,
                "precio": precio,
                "stock": stock,
                "isbn": isbn,
                "estado": "disponible"
            }
            libros.append(libro_nuevo)
            print(f"✔ Libro agregado con ID {nuevo_id}.")
            # Registrar log
            registrar_log(
                "Agregar libro",
                datos=libro_nuevo,
                usuario=usuario
            )
        print("-" * 60)
        titulo = pedir_texto("Otro título (o 'salir'): ")


def generar_id_unico(libros):
    ids = {libro["id"] for libro in libros}
    nuevo = random.randint(10000, 99999)
    while nuevo in ids:
        nuevo = random.randint(10000, 99999)
    return nuevo

def buscar_libro(libros, id_libro, usuario):
    libro = next((libro for libro in libros if libro["id"] == id_libro), None)    
    return libro

def buscar_libro_ui(libros, usuario):
    try:
        id_lib = int(input("ID a buscar: "))
        libro = buscar_libro(libros, id_lib, usuario)  # Pasando usuario

        registrar_log(
            "Buscar libro",
            datos={"id": id_lib, "encontrado": bool(libro)},
            usuario=usuario
        )

        print(libro if libro else "No encontrado.")
    except ValueError:
        print("✖ ID inválido.")

def buscar_libro_por_titulo(libros, titulo):
    return next((libro for libro in libros if libro["titulo"].lower() == titulo.lower()), None)

def modificar_libro(libros, usuario="desconocido"):
    titulo = input("Título del libro a modificar: ").strip()
    libro = buscar_libro_por_titulo(libros, titulo)
    if not libro:
        print("No se encontró un libro con ese título.")
        return

    print("1) Título\n2) Autor\n3) Categoría\n4) Precio\n5) Stock")
    op = input("¿Qué desea modificar?: ")

    if op == "1":
        valor_anterior = libro["titulo"]
        libro["titulo"] = input("Nuevo título: ").title()
        registrar_log(
            "Modificar título",
            datos={"id": libro["id"], "anterior": valor_anterior, "nuevo": libro["titulo"]},
            usuario=usuario
        )
    elif op == "2":
        valor_anterior = libro["autor"]
        libro["autor"] = input("Nuevo autor: ").title()
        registrar_log(
            "Modificar autor",
            datos={"id": libro["id"], "anterior": valor_anterior, "nuevo": libro["autor"]},
            usuario=usuario
        )
    elif op == "3":
        nueva_cat = input(f"Nueva categoría {CATEGORIAS}: ").title()
        if nueva_cat in CATEGORIAS:
            valor_anterior = libro["categoria"]
            libro["categoria"] = nueva_cat
            registrar_log(
                "Modificar categoría",
                datos={"id": libro["id"], "anterior": valor_anterior, "nuevo": nueva_cat},
                usuario=usuario
            )
        else:
            print("✖ Categoría inválida.")
    elif op == "4":
        valor_anterior = libro["precio"]
        libro["precio"] = float(input("Nuevo precio: "))
        registrar_log(
            "Modificar precio",
            datos={"id": libro["id"], "anterior": valor_anterior, "nuevo": libro["precio"]},
            usuario=usuario
        )
    elif op == "5":
        valor_anterior = libro["stock"]
        libro["stock"] = int(input("Nuevo stock: "))
        registrar_log(
            "Modificar stock",
            datos={"id": libro["id"], "anterior": valor_anterior, "nuevo": libro["stock"]},
            usuario=usuario
        )
    else:
        print("✖ Opción inválida.")

def eliminar_libro(libros):
    try:
        id_lib = int(input("ID a dar de baja: "))
        libro = buscar_libro(libros, id_lib)
        if libro:
            libro["estado"] = "no disponible"
            print("✔ Libro marcado como no disponible.")
            registrar_log("Eliminar libro", datos={"id": id_lib, "resultado": "ok"}, usuario="sistema")
        else:
            print("No encontrado.")
            registrar_log("Eliminar libro", datos={"id": id_lib, "resultado": "no encontrado"}, usuario="sistema")
    except ValueError:
        print("✖ ID inválido.")
        registrar_log("Eliminar libro", datos={"id": "inválido"}, usuario="sistema")

def reactivar_libro(libros):
    no_disponibles = [l for l in libros if l.get("estado") != "disponible"]
    if not no_disponibles:
        print("✔ Todos los libros están disponibles.")
        registrar_log("Reactivar libro", datos={"resultado": "todos disponibles"}, usuario="sistema")
        return

    for l in no_disponibles:
        print(f"ID:{l['id']} - {l['titulo']}")

    try:
        id_lib = int(input("Ingrese el ID del libro a reactivar: "))
        libro = buscar_libro(libros, id_lib)
        if libro:
            if libro.get("estado") == "disponible":
                print("El libro ya está disponible.")
                registrar_log("Reactivar libro", datos={"id": id_lib, "resultado": "ya disponible"}, usuario="sistema")
            else:
                libro["estado"] = "disponible"
                print("✔ Libro reactivado correctamente.")
                registrar_log("Reactivar libro", datos={"id": id_lib, "resultado": "reactivado"}, usuario="sistema")
        else:
            print("Libro no encontrado.")
            registrar_log("Reactivar libro", datos={"id": id_lib, "resultado": "no encontrado"}, usuario="sistema")
    except ValueError:
        print("✖ ID inválido.")
        registrar_log("Reactivar libro", datos={"id": "inválido", "resultado": "error de entrada"}, usuario="sistema")


def ver_stock_total(libros, usuario):
    print("\n" + "-" * 60)
    print(" STOCK TOTAL ")
    print("-" * 60)
    for libro in libros:
        if libro.get("estado") != "disponible":
            continue
        categoria = libro.get("categoria", "Sin categoría")
        print(
            f"ID:{libro['id']:>5} | {libro['titulo']:<30} | Categoría:{categoria:<15} | Stock:{libro['stock']:>3}"
        )
    print("-" * 60)
    registrar_log(
        "Consultar stock total",
        datos={"cantidad_libros": sum(1 for libro in libros if libro.get("estado") == "disponible")},
        usuario=usuario
    )

def mostrar_ultimos_libros(libros, usuario="sistema"):
    if not libros:
        print("No hay libros.")
        registrar_log("Mostrar últimos libros", datos={"resultado": "sin libros"}, usuario=usuario)
        return
    try:
        n = int(input("¿Cuántos últimos mostrar? "))
    except ValueError:
        print("✖ Número inválido.")
        registrar_log("Mostrar últimos libros", datos={"resultado": "input inválido"}, usuario=usuario)
        return
    n = max(1, min(n, len(libros)))
    print("\n" + "-" * 60)
    print(f"Últimos {n} libros")
    for libro in libros[-n:]:
        print(f"ID:{libro['id']:>5} | {libro['titulo']} ({libro['categoria']})")
    print("-" * 60)
    registrar_log("Mostrar últimos libros", datos={"cantidad_mostrada": n}, usuario=usuario)


def libros_baratos(libros, usuario="sistema"):
    try:
        limite = float(input("Mostrar libros con precio menor a: $"))
    except ValueError:
        print("✖ Ingresá un número válido.")
        registrar_log("Libros baratos", datos={"limite": "inválido"}, usuario=usuario)
        return
    baratos = [l for l in libros if l["precio"] < limite and l.get("estado") == "disponible"]
    print("\n" + "-" * 60)
    print(f" LIBROS BARATOS (<${limite}) ")
    print("-" * 60)
    if baratos:
        for l in baratos:
            print(f"{l['titulo']} - ${l['precio']}")
    else:
        print("No hay libros por debajo de ese precio.")
    print("-" * 60)
    registrar_log("Libros baratos", datos={"limite": limite, "cantidad": len(baratos)}, usuario=usuario)


def obtener_categorias():
    return sorted(CATEGORIAS)

def agregar_categoria(nombre, usuario="sistema"):
    if nombre in CATEGORIAS:
        registrar_log("Agregar categoría", datos={"nombre": nombre, "resultado": "ya existe"}, usuario=usuario)
        return False
    CATEGORIAS.add(nombre)
    registrar_log("Agregar categoría", datos={"nombre": nombre, "resultado": "agregada"}, usuario=usuario)
    return True


def modificar_categoria(actual, nueva):
    if actual not in CATEGORIAS or nueva in CATEGORIAS:
        return False
    CATEGORIAS.remove(actual)
    CATEGORIAS.add(nueva)
    return True

def eliminar_categoria(nombre, usuario="sistema"):
    if nombre not in CATEGORIAS or len(CATEGORIAS) == 1:
        registrar_log("Eliminar categoría", datos={"nombre": nombre, "resultado": "fallo"}, usuario=usuario)
        return False
    CATEGORIAS.remove(nombre)
    registrar_log("Eliminar categoría", datos={"nombre": nombre, "resultado": "eliminada"}, usuario=usuario)
    return True

def menu_categorias(usuario="sistema"):
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
            if agregar_categoria(nueva, usuario):
                print("✔ Categoría agregada.")
            else:
                print("✖ Ya existe esa categoría.")

        elif opcion == 3:
            actual = input("Categoría a modificar: ").title()
            nueva = input("Nuevo nombre: ").title()
            if modificar_categoria(actual, nueva, usuario):
                print("✔ Modificada correctamente.")
            else:
                print("✖ Error al modificar. Verifique los nombres.")

        elif opcion == 4:
            nombre = input("Categoría a eliminar: ").title()
            if eliminar_categoria(nombre, usuario):
                print("✔ Eliminada correctamente.")
            else:
                print("✖ No se pudo eliminar. ¿Existe o es la única?")

        elif opcion == 5:
            break
