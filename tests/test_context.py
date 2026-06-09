from brain.context import Registro


def test_agregar_un_mensaje():
    mensajes = Registro()
    mensajes.agregar(
        "Hola, Como estás?, Esta es una prueba unitaria, es mi primera vez, pera, manzana",
        "Hola, bien, gracias",
    )
    assert len(mensajes.HISTORIAL_IA) == 1
    assert len(mensajes.HISTORIAL_USUARIO) == 1
    assert "Hola" in mensajes.formato()
