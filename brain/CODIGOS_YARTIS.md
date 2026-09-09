Directorio
0x0x0Polo0700|crear|tipo|nombre|ruta|respuesta
0x0x0Polo0700|eliminar|tipo|nombre|ruta|respuesta

0x0x0Polo0700|modificar|tipo|ruta|texto_viejo$$texto_nuevo|explicacion|

mover va ser diferente el unico
0x0x0Polo0700|mover|tipo|ruta_inicio|ruta_final|none|

archivo
0x0x0Polo0700|crear|tipo|ruta|respuesta|none
0x0x0Polo0700|eliminar|tipo|ruta|respuesta|none
0x0x0Polo0700|modificar|tipo|ruta|texto_viejo$$texto_nuevo|explicacion|

mover va ser diferente el unico
0x0x0Polo0700|mover|tipo|ruta_inicio|ruta_final|none|

============================================
CATEGORIAS (familias): como meto un comando nuevo
============================================

1. Crear, eliminar = misma estructura -> categoria 1
2. Modificar = estructura distinta (texto_viejo$$nuevo) -> categoria 2
3. Mover = estructura distinta (ruta_inicio -> ruta_final) -> categoria 3
4. Comando nuevo: piensa que parametros ocupa
   -> si comparte con una familia, usa ESA categoria
   -> si es estructura nueva, crea categoria nueva

Ejemplo: grep y find ocupan lo mismo (ruta + patron) -> misma categoria.
El parser solo ve la estructura, no el nombre del comando.
