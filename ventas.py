from datetime import datetime
from utils import registrar_log, guardar_ventas, guardar_facturas, pedir_opcion
from libros import buscar_libro
from clientes import buscar_cliente, agregar_cliente

def menu_ventas(libros, clientes, ventas, facturas, usuario):
    print("\n" + "*" * 60)
    print("MENÚ VENTAS")
    print("*" * 60)
    print("2.1 - Vender libro")
    print("2.2 - Ver ventas realizadas")
    print("2.3 - Ver facturas emitidas")
    print("2.4 - Volver")
    print("-" * 60)

    opcion = pedir_opcion("Seleccione una opción: ", [1, 2, 3, 4])

    if opcion == 1:
        vender_libro(libros, clientes, ventas, facturas, usuario)
        return menu_ventas(libros, clientes, ventas, facturas, usuario)
    elif opcion == 2:
        ver_ventas_realizadas(ventas, usuario)
        return menu_ventas(libros, clientes, ventas, facturas, usuario)
    elif opcion == 3:
        ver_facturas_emitidas(facturas, usuario)
        return menu_ventas(libros, clientes, ventas, facturas, usuario)
    elif opcion == 4:
        return


def vender_libro(libros, clientes, ventas, facturas, usuario, dni_cliente=None):
    if dni_cliente is None:
        dni_cliente = input("DNI del cliente: ").strip()
        cliente = buscar_cliente(clientes, dni_cliente)
        if not cliente:
            print("Cliente no encontrado. Agregando nuevo cliente.")
            agregar_cliente(clientes, usuario=usuario, dni=dni_cliente)
    else:
        cliente = buscar_cliente(clientes, dni_cliente)
        if not cliente:
            print("Cliente no encontrado. Agregando nuevo cliente.")
            agregar_cliente(clientes, usuario=usuario, dni=dni_cliente)


    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    factura = {
        "Factura": len(facturas) + 1,
        "Fecha": fecha,
        "DNI": dni_cliente,
        "Libros": [],  # lista de dicts con id_libro, cantidad y precio_unitario
        "Total": 0
    }

    total = 0
    libros_vendidos = []
    venta_parcial_matriz = [["ID", "Título", "Cantidad", "Precio Unitario"]]

    while True:
        print("\nAgregar libro al carrito:")
        print("1) Buscar por ID")
        print("2) Buscar por título")
        print("3) Finalizar venta")
        opcion_busqueda = input("Seleccione una opción: ")

        if opcion_busqueda == "1":
            try:
                id_lib = int(input("Ingrese el ID del libro: "))
                libro = buscar_libro(libros, id_lib)
            except ValueError:
                print("✖ ID inválido.")
                continue
        elif opcion_busqueda == "2":
            titulo = input("Ingrese el título del libro: ").lower()
            libro = next((l for l in libros if l["titulo"].lower() == titulo and l.get("estado") == "disponible"), None)
            id_lib = libro["id"] if libro else None
        elif opcion_busqueda == "3":
            if not libros_vendidos:
                print("✖ No se agregaron libros. Venta cancelada.")
                return
            break
        else:
            print("✖ Opción inválida.")
            continue

        if opcion_busqueda in ["1", "2"]:
            if libro and libro["stock"] > 0 and libro.get("estado") == "disponible":
                try:
                    cant = int(input("Cantidad: "))
                    if 0 < cant <= libro["stock"]:
                        subtotal = libro["precio"] * cant
                        ventas.append({
                            "dni": dni_cliente,
                            "id_libro": id_lib,
                            "cantidad": cant,
                            "precio_total": subtotal,
                            "fecha": fecha,
                            "vendedor": usuario
                        })
                        libro["stock"] -= cant
                        total += subtotal
                        factura["Libros"].append({
                            "id_libro": id_lib,
                            "titulo": libro["titulo"],
                            "cantidad": cant,
                            "precio_unitario": libro["precio"]
                        })
                        libros_vendidos.append((id_lib, cant, libro["precio"], libro["titulo"]))
                        venta_parcial_matriz.append([str(id_lib), str(libro["titulo"]) ,str(cant), f"${libro['precio']:.2f}"])

                        
                        print(f"\n✔ Libro agregado al carrito: {libro['titulo']} (ID: {id_lib})")
                        print(f"   Cantidad: {cant} | Precio unitario: ${libro['precio']:.2f} | Subtotal: ${subtotal:.2f}")

                        
                        print("\nVenta parcial:")
                        for fila in venta_parcial_matriz:
                            print(" | ".join(fila))
                    else:
                        print("✖ Cantidad inválida o sin stock suficiente.")
                except ValueError:
                    print("✖ Cantidad inválida.")
            else:
                print("✖ Libro no encontrado o no disponible.")


    factura["Total"] = total
    facturas.append(factura)

    try:
        guardar_ventas(ventas, usuario)
        guardar_facturas(facturas, usuario)
        registrar_log("Venta realizada", datos={"total": total, "factura": factura["Factura"]}, usuario=usuario)
    except Exception as e:
        print("✖ Error al guardar la venta.")
        registrar_log("Error al guardar venta", datos={"error": str(e)}, usuario=usuario)

    print("\n" + "=" * 40)
    print("FACTURA N°", factura["Factura"])
    print("Fecha:", factura["Fecha"])
    print("Cliente DNI:", factura["DNI"])
    print("-" * 40)
    print("ID".ljust(6), "Cant.".ljust(6), "Precio".rjust(10))
    print("-" * 40)
    for id_lib, cant, precio, titulo in libros_vendidos:
        print(str(id_lib).ljust(6), str(cant).ljust(6), f"${precio:.2f}".rjust(10), "-", titulo)
    print("-" * 40)
    print("TOTAL:".ljust(12), f"${total:.2f}".rjust(10))
    print("=" * 40)
    print("Vendedor:", usuario)
    print("Gracias por su compra".center(40))
    print("¡Que tenga un excelente día!".center(40))


def ver_ventas_realizadas(ventas, usuario):
    print("\n" + "-" * 60)
    print(" VENTAS REALIZADAS ")
    print("-" * 60)
    for v in ventas:
        print(v)
    print("-" * 60)
    registrar_log("Ver ventas realizadas", datos={"cantidad": len(ventas)}, usuario=usuario)

def ver_facturas_emitidas(facturas, usuario):
    print("\n" + "-" * 60)
    print(" FACTURAS EMITIDAS ")
    print("-" * 60)
    for f in facturas:
        print(f)
        print("-" * 60)
    registrar_log("Ver facturas emitidas", datos={"cantidad": len(facturas)}, usuario=usuario)
