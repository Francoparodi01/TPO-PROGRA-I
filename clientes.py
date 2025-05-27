from utils import pedir_opcion

def buscar_cliente(clientes, dni):
    for cli in clientes:
        if cli["dni"] == dni:
            return cli
    return None

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

def eliminar_cliente(clientes):
    dni = input("DNI a eliminar: ")
    cli = buscar_cliente(clientes, dni)
    if cli:
        clientes.remove(cli)
        print("✔ Cliente eliminado.")
    else:
        print("No encontrado.")

def ver_clientes(clientes):
    print("\n" + "-" * 60)
    print(" CLIENTES ")
    print("-" * 60)
    for c in clientes:
        print(f"DNI:{c['dni']:>10} | {c['nombre']} {c['apellido']}")
    print("-" * 60)

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
