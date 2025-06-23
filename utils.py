import json
from datetime import datetime
from pathlib import Path
import os
import csv

# ---------- LOGGING ----------

LOG_FILE = Path("logs.json")

def registrar_log(accion, datos=None, usuario="sistema"):
    """
    Registra una acción en logs.json

    :param accion: (str) Descripción de la acción
    :param datos: (dict|None) Información extra
    :param usuario: (str) Usuario que realiza la acción
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "accion": accion,
        "usuario": usuario,
        "datos": datos or {}
    }

    if LOG_FILE.exists():
        try:
            with LOG_FILE.open("r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []

    logs.append(log_entry)

    with LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


# ---------- LOGIN Y MENÚ ----------

def login(usuarios):
    print("=" * 60)
    print("SISTEMA DE LIBRERÍA")
    print("=" * 60)

    nombre = input("Nombre: ").strip()
    usuario_encontrado = next((u for u in usuarios if u.get("nombre", "").lower() == nombre.lower()), None)
    if usuario_encontrado is None:
        print("Usuario no encontrado.")
        registrar_log("Login fallido - usuario no encontrado", {"nombre": nombre})
        return None

    contrasena = input("Contraseña: ")
    if usuario_encontrado.get("contrasena") == contrasena:
        registrar_log("Login exitoso", usuario=nombre)
        print("\n" + "-" * 60)
        return usuario_encontrado
    else:
        print("Contraseña incorrecta.")
        registrar_log("Login fallido - contraseña incorrecta", {"nombre": nombre})
        return None


# ---------- CARGA VENDEDORES ----------

def cargar_usuarios(path="usuarios.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)  # Aquí devuelve una lista
    except Exception as e:
        print("Error cargando usuarios:", e)
        return []


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

def pedir_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("✖ El número debe ser positivo.")
            else:
                return valor
        except ValueError:
            print("✖ Ingresá un número válido.")

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != "": # Aseguramos que no esté vacío
            return texto  # Ya no filtramos por letras solamente
        else:
            print("✖ No puede estar vacío.")


def mostrar_menu_principal(usuario):
    print("-" * 60)
    print("1) Libros")
    print("2) Ventas")
    print("3) Clientes")
    print("4) Salir")
    print("-" * 60)


def salir():
    print("Sesión cerrada. Volviendo al login...")


# ---------- CLIENTES ----------

ARCHIVO_CLIENTES = "clientes.json"

def cargar_clientes(usuario="sistema"):
    if not os.path.exists(ARCHIVO_CLIENTES):
        return []
    try:
        with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print("✖ Archivo de clientes malformado. Se cargará una lista vacía.")
        registrar_log("Error al cargar clientes", {"error": str(e)}, usuario)
        return []
    except Exception as e:
        print("✖ Error inesperado al cargar clientes.")
        registrar_log("Error inesperado al cargar clientes", {"error": str(e)}, usuario)
        return []

def guardar_clientes(clientes, usuario="sistema"):
    try:
        with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as f:
            json.dump(clientes, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("✖ Error al guardar clientes.")
        registrar_log("Error al guardar clientes", {"error": str(e)}, usuario)


# ---------- LIBROS ----------

ARCHIVO_LIBROS = "libros.json"

def guardar_libros(libros, usuario="sistema"):
    try:
        with open(ARCHIVO_LIBROS, "w", encoding="utf-8") as f:
            json.dump(libros, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("✖ Error al guardar libros.")
        registrar_log("Error al guardar libros", {"error": str(e)}, usuario)

def cargar_libros(usuario="sistema"):
    libros = []
    try:
        if not os.path.exists(ARCHIVO_LIBROS):
            registrar_log("Archivo libros.json no encontrado", usuario=usuario)
            return []
        with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as f:
            libros = json.load(f)
            for libro in libros:
                libro["id"] = int(libro["id"])
                libro["precio"] = float(libro["precio"])
                libro["stock"] = int(libro["stock"])
    except json.JSONDecodeError as e:
        print("✖ Error al leer libros.json: archivo malformado.")
        registrar_log("Archivo libros.json malformado", {"error": str(e)}, usuario)
    except Exception as e:
        print("✖ Error al cargar libros.")
        registrar_log("Error al cargar libros", {"error": str(e)}, usuario)
    return libros


# ---------- VENTAS / FACTURAS ----------

ARCHIVO_VENTAS = "ventas.json"
ARCHIVO_FACTURAS = "facturas.json"

def cargar_ventas(usuario="sistema"):
    try:
        with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        registrar_log("Error al cargar ventas", {"error": str(e)}, usuario)
        return []
    except Exception as e:
        registrar_log("Error inesperado al cargar ventas", {"error": str(e)}, usuario)
        return []

def guardar_ventas(ventas, usuario="sistema"):
    try:
        with open(ARCHIVO_VENTAS, "w", encoding="utf-8") as f:
            json.dump(ventas, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("✖ Error al guardar ventas.")
        registrar_log("Error al guardar ventas", {"error": str(e)}, usuario)

def cargar_facturas(usuario="sistema"):
    try:
        with open(ARCHIVO_FACTURAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        registrar_log("Error al cargar facturas", {"error": str(e)}, usuario)
        return []
    except Exception as e:
        registrar_log("Error inesperado al cargar facturas", {"error": str(e)}, usuario)
        return []

def guardar_facturas(facturas, usuario="sistema"):
    try:
        with open(ARCHIVO_FACTURAS, "w", encoding="utf-8") as f:
            json.dump(facturas, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("✖ Error al guardar facturas.")
        registrar_log("Error al guardar facturas", {"error": str(e)}, usuario)
