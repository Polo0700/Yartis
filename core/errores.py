ERRORES = {
    # ===================== CRUD =====================
    "E_RUTA_INVALIDA": {
        "mensaje": "La ruta no existe. Verifica la ruta en el campo 3.",
        "solucion": "Corrige la ruta del campo 3 y emite el comando de nuevo.",
    },
    "E_YA_EXISTE": {
        "mensaje": "El elemento ya existe en esa ruta.",
        "solucion": "Usa modificar en vez de crear, o elige otro nombre.",
    },
    "E_NO_EXISTE": {
        "mensaje": "El elemento no existe en esa ruta.",
        "solucion": "Verifica el nombre y la ruta del campo 3 y reintenta.",
    },
    "E_PERMISO": {
        "mensaje": "No tengo permisos para tocar ese elemento.",
        "solucion": "Elige otra ruta o avisa al usuario de los permisos.",
    },
    "E_TIPO_INCORRECTO": {
        "mensaje": "El tipo no coincide con la ruta indicada.",
        "solucion": "Corrige el campo 2 como archivo o directorio segun sea.",
    },
    # ===================== PARSER =====================
    "E_FORMATO": {
        "mensaje": "El comando no tiene el formato correcto.",
        "solucion": "Reemite el comando con los 7 campos separados por pipe.",
    },
    "E_ACCION_DESCONOCIDA": {
        "mensaje": "La accion no es reconocida.",
        "solucion": "Usa crear, eliminar, modificar o mover en el campo 1.",
    },
    "E_TIPO_DESCONOCIDO": {
        "mensaje": "El tipo no es reconocido.",
        "solucion": "Usa archivo o directorio en el campo 2.",
    },
    "E_MODIFICAR_SIN_DOBLE_PESO": {
        "mensaje": "El texto a modificar no tiene el separador doble peso.",
        "solucion": "Separa texto viejo y nuevo con dos signos de peso.",
    },
    "E_SIN_RESPUESTA_RAPIDA": {
        "mensaje": "Falta la respuesta rapida al final del comando.",
        "solucion": "Agrega la frase al final en el campo 7.",
    },
    # ===================== FLUJO =====================
    "E_SIN_CONFIRMACION": {
        "mensaje": "No recibiste confirmacion del usuario.",
        "solucion": "Espera a que el usuario confirme antes de ejecutar.",
    },
    "E_VACIO": {
        "mensaje": "No se recibio texto para procesar.",
        "solucion": "Pide al usuario que repita lo que quiere.",
    },
}


def obtener_error(codigo):
    """Devuelve el error completo buscando el codigo en el catalogo."""
    return ERRORES.get(codigo, {
        "mensaje": "Error desconocido.",
        "solucion": "Verifica el codigo del error.",
    })