def login(usuarios):
    print("=" * 60)
    print("SISTEMA DE LIBRERÍA")
    print("=" * 60)
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    while usuario not in usuarios or usuarios[usuario] != contrasena:
        print("\nUsuario o contraseña incorrectos. Intente nuevamente.\n")
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")
    return usuario


def pedir_opcion(mensaje, opciones_validas):
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


def mostrar_menu_principal(usuario):
    print("\n" + "-" * 60)
    print(f"Bienvenido, {usuario}")
    print("-" * 60)
    print("1) Libros")
    print("2) Ventas")
    print("3) Clientes")
    print("4) Salir")
    print("-" * 60)


def salir():
    print("Sesión cerrada. Volviendo al login...")
