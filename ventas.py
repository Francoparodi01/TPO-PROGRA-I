from datetime import datetime
from utils import pedir_opcion
from libros import buscar_libro
from clientes import buscar_cliente, agregar_cliente


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
    libros_vendidos = []
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
                    libros_vendidos.append((libro, cant))
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

    if factura["Libros"]:
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
                libro["stock"] += cantidad
            print("✔ Venta cancelada. No se registró ninguna factura.")
    else:
        print("No se realizó ninguna venta.")


def ver_ventas_realizadas(ventas):
    print("\n" + "-" * 60)
    print(" VENTAS REALIZADAS ")
    print("-" * 60)
    for v in ventas:
        print(v)
    print("-" * 60)


def ver_facturas_emitidas(facturas):
    print("\n" + "-" * 60)
    print(" FACTURAS EMITIDAS ")
    print("-" * 60)
    for f in facturas:
        print(f)
        print("-" * 60)
