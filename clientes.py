from utils import pedir_opcion, registrar_log, guardar_clientes

def buscar_cliente(clientes, dni):
    return next((cli for cli in clientes if cli["dni"] == dni), None)

def agregar_cliente(clientes, usuario, dni=None):
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
        registrar_log("Agregar cliente", datos={"dni": dni, "resultado": "ya existente"}, usuario=usuario)
        return

    nombre = input("Nombre: ").strip().title()
    while not nombre:
        print("✖ Nombre no puede ser vacío.")
        nombre = input("Nombre: ").strip().title()

    apellido = input("Apellido: ").strip().title()
    while not apellido:
        print("✖ Apellido no puede ser vacío.")
        apellido = input("Apellido: ").strip().title()

    cliente = {"dni": dni, "nombre": nombre, "apellido": apellido}
    clientes.append(cliente)

    try:
        guardar_clientes(clientes, usuario)
        print("-" * 60)
        print(f"Cliente agregado: DNI:{dni} | {nombre} {apellido}")
        print("-" * 60)
        registrar_log("Agregar cliente", datos=cliente, usuario=usuario)
    except Exception as e:
        print("✖ Error al guardar cliente.")
        registrar_log("Error al guardar cliente", datos={"error": str(e)}, usuario=usuario)

def eliminar_cliente(clientes, usuario):
    dni = input("DNI a eliminar: ").strip()
    cli = buscar_cliente(clientes, dni)
    if cli:
        clientes.remove(cli)
        try:
            guardar_clientes(clientes, usuario)
            print("✔ Cliente eliminado.")
            registrar_log("Eliminar cliente", datos={"dni": dni, "resultado": "eliminado"}, usuario=usuario)
        except Exception as e:
            print("✖ Error al guardar cambios.")
            registrar_log("Error al eliminar cliente", datos={"dni": dni, "error": str(e)}, usuario=usuario)
    else:
        print("✖ Cliente no encontrado.")
        registrar_log("Eliminar cliente", datos={"dni": dni, "resultado": "no encontrado"}, usuario=usuario)

def ver_clientes(clientes, usuario):
    print("\n" + "-" * 60)
    print(" CLIENTES ")
    print("-" * 60)

    lineas = list(map(lambda c: f"DNI:{c['dni']:>10} | {c['nombre']} {c['apellido']}", clientes))
    for linea in lineas:
        print(linea)

    print("-" * 60)
    registrar_log("Ver clientes", datos={"cantidad": len(clientes)}, usuario=usuario)

def menu_clientes(clientes, usuario):
    print("\n" + "*" * 60)
    print("MENÚ CLIENTES")
    print("*" * 60)
    print("3.1 - Agregar cliente")
    print("3.2 - Eliminar cliente")
    print("3.3 - Ver clientes")
    print("3.4 - Volver")
    print("-" * 60)

    opcion = pedir_opcion("Seleccione una opción: ", [1, 2, 3, 4])

    if opcion == 1:
        agregar_cliente(clientes, usuario)
        return menu_clientes(clientes, usuario)
    elif opcion == 2:
        eliminar_cliente(clientes, usuario)
        return menu_clientes(clientes, usuario)
    elif opcion == 3:
        ver_clientes(clientes, usuario)
        return menu_clientes(clientes, usuario)
    elif opcion == 4:
        return
