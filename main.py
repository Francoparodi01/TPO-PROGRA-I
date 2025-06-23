from utils import cargar_usuarios, login, registrar_log, cargar_libros, cargar_clientes, cargar_ventas, cargar_facturas, pedir_opcion, mostrar_menu_principal
from libros import menu_libros
from clientes import menu_clientes
from ventas import menu_ventas

def menu_principal(libros, clientes, ventas, facturas, usuario):
    while True:
        mostrar_menu_principal(usuario["nombre"])
        opcion = pedir_opcion("Seleccione una opción: ", [1, 2, 3, 4])

        if opcion == 1:
            registrar_log("Ingreso al módulo Libros", usuario=usuario["nombre"])
            menu_libros(libros, usuario["nombre"])
        elif opcion == 2:
            registrar_log("Ingreso al módulo Ventas", usuario=usuario["nombre"])
            menu_ventas(libros, clientes, ventas, facturas, usuario["nombre"])
        elif opcion == 3:
            registrar_log("Ingreso al módulo Clientes", usuario=usuario["nombre"])
            menu_clientes(clientes, usuario["nombre"])
        elif opcion == 4:
            registrar_log("Cierre de sesión", usuario=usuario["nombre"])
            print("Sesión cerrada. Volviendo al login...\n")
            break

def main():
    usuarios = cargar_usuarios("usuarios.json")
    libros = cargar_libros()
    clientes = cargar_clientes()
    ventas = cargar_ventas()
    facturas = cargar_facturas()

    while True:
        usuario = None
        while usuario is None:
            usuario = login(usuarios)
        print(f"Bienvenido/a {usuario['nombre']}")
        menu_principal(libros, clientes, ventas, facturas, usuario)

if __name__ == "__main__":
    main()
