from libros import buscar_libro

def test_buscar_libro_encuentra():
    # Preparo una lista de libros de prueba
    libros = [
        {"id": 1, "titulo": "1984"},
        {"id": 2, "titulo": "Rayuela"},
    ]
    # Llamo la función que quiero testear
    libro = buscar_libro(libros, 2)
    # Verifico que lo que devuelve sea lo correcto
    assert libro["titulo"] == "Rayuela"

def test_buscar_libro_no_encuentra():
    libros = [
        {"id": 1, "titulo": "1984"}
    ]
    libro = buscar_libro(libros, 5)
    assert libro is None
