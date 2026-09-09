import os
import pathlib
import psutil
from pathlib import Path
import win32com


class Herramientas:
    def __init__(self):
        self.herramienta = pathlib.Path(".")
        self.pathActual = Path.cwd()

    # ===================== CRUD NÚCLEO =====================

    def crear_archivo(self, nombre_archivo):
        create_file = self.herramienta / nombre_archivo
        create_file.touch(exist_ok=True)

    def eliminar_archivo(self, nombre_archivo):
        delete_file = self.herramienta / nombre_archivo
        if delete_file.exists():
            delete_file.unlink()

    def modificar_archivo(self, nombre_archivo, contenido):
        modift_file = self.herramienta / nombre_archivo
        with open(modift_file, "w") as f:
            f.write(contenido)

    def mover_archivo(self, nombre_archivo, nueva_ruta):
        old_file = self.herramienta / nombre_archivo
        new_file = self.herramienta / nueva_ruta
        old_file.rename(new_file)

    def crear_directorio(self, nombre_directorio):
        new_dir = self.herramienta / nombre_directorio
        new_dir.mkdir(exist_ok=True)

    def eliminar_directorio(self, nombre_directorio):
        del_dir = self.herramienta / nombre_directorio
        if del_dir.exists():
            del_dir.rmdir()

    def modificar_directorio(self, nombre_directorio, nuevo_nombre):
        old_dir = self.herramienta / nombre_directorio
        new_dir = self.herramienta / nuevo_nombre
        old_dir.rename(new_dir)

    def mover_directorio(self, nombre_directorio, nueva_ruta):
        old_dir = self.herramienta / nombre_directorio
        new_dir = self.herramienta / nueva_ruta
        old_dir.rename(new_dir)

    # ===================== HERRAMIENTAS ADICIONALES =====================
    # Tienen sentido pero se usan rara vez. opencode puede pasar la ruta.

    def listar_archivos(self, Directorio):
        try:
            archivos = []
            if not Directorio.is_dir():
                return None
            for nombre in Directorio.iterdir():
                if nombre.is_file():
                    print(nombre.name)
                    archivos.append(nombre)
            return archivos
        except Exception as e:
            return f"No se puede listar los archivos hubo un error puede ser un directorio invalido, Error: {e}"

    def listar_directorios(self, Directorio):
        try:
            directorios = []
            for nombre in Directorio.iterdir():
                if nombre.is_dir():
                    print(nombre.name)
                    directorios.append(nombre)
            return directorios
        except Exception as e:
            return f"Directorio invalido, Error: {e}"

    def buscar_archivo(self, archivo_buscado, Directorio):
        try:
            for nombre in Directorio.iterdir():
                if nombre.is_file() and nombre.name == archivo_buscado:
                    print(nombre.name)
                    return nombre
            return None
        except Exception as e:
            return f"Archivo invalido, Error {e}"

    def buscar_directorio(self, directorio_buscado, Directorio):
        try:
            for nombre in Directorio.iterdir():
                if nombre.is_dir() and nombre.name == directorio_buscado:
                    print(nombre.name)
                    return nombre
            return None
        except Exception as e:
            return f"Directorio no encontrado o invalido, Error {e}"

    def obtener_info_archivo(self, archivo_name):
        try:
            info = {
                "nombre": archivo_name.name,
                "ruta": str(archivo_name.resolve()),
                "tamano": self.obtener_tamano_archivo(archivo_name),
                "fecha_creacion": self.obtener_fecha_creacion_archivo(archivo_name),
                "fecha_modificacion": self.obtener_fecha_modificacion_archivo(
                    archivo_name
                ),
                "permisos": self.obtener_permisos_archivo(archivo_name),
                "propietario": self.obtener_propietario_archivo(archivo_name),
                "grupo": self.obtener_grupo_archivo(archivo_name),
                "tipo": self.obtener_tipo_archivo(archivo_name),
            }
            return info
        except Exception as e:
            return f"archivo no encontrado o invalido, Error {e}"

    def obtener_info_directorio(self, Directorio):
        if not Directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        cwd = self.pathActual
        directorio = cwd / Directorio
        info = {
            "nombre": directorio.name,
            "ruta": str(directorio.resolve()),
            "tamano": self.obtener_tamano_directorio(directorio),
            "fecha_creacion": self.obtener_fecha_creacion_directorio(directorio),
            "fecha_modificacion": self.obtener_fecha_modificacion_directorio(
                directorio
            ),
            "permisos": self.obtener_permisos_directorio(directorio),
            "propietario": directorio.owner() if self.sistema() == "posix" else None,
            "grupo": directorio.group() if self.sistema() == "posix" else None,
            "tipo": self.obtener_tipo_directorio(directorio),
        }
        return info

    def obtener_ruta_absoluta(self, archivo_o_directorio):
        ruta = Path(archivo_o_directorio)
        if not ruta.exists():
            return "Error de ruta"
        ruta_absoluta = os.path.abspath(archivo_o_directorio)
        return ruta_absoluta

    def obtener_ruta_absoluta_mediante_proceso(self, pid):
        # aqui se saca el pid
        if not pid:
            return
        # aqui suponemos que ya tiene ruta
        # if ruta:
        #    res = ruta
        # finally:
        #    res = res + titulo
        #    return res

    def obtener_ruta_relativa(self, ruta, start):
        if not ruta or not start:
            return "datos insuficientes para obtener la ruta relativa"
        return os.path.relpath(ruta, start)

    def obtener_tamano_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return archivo.stat().st_size

    def obtener_tamano_directorio(self, directorio):
        if not directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        return directorio.stat().st_size

    def obtener_fecha_creacion_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return archivo.stat().st_ctime

    def obtener_fecha_creacion_directorio(self, directorio):
        if not directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        return directorio.stat().st_ctime

    def obtener_fecha_modificacion_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return archivo.stat().st_mtime

    def obtener_fecha_modificacion_directorio(self, directorio):
        if not directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        return directorio.stat().st_mtime

    def obtener_permisos_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return oct(archivo.stat().st_mode)[-3:]

    def obtener_permisos_directorio(self, directorio):
        if not directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        return oct(directorio.stat().st_mode)[-3:]

    def obtener_propietario_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        if self.sistema() == "posix":
            return archivo.owner()
        return None

    def obtener_grupo_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        if self.sistema() == "posix":
            return archivo.group()
        return None

    def obtener_tipo_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return archivo.suffix

    def obtener_tipo_directorio(self, directorio):
        if not directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        return "directorio"

    def obtener_extension_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return archivo.suffix

    def obtener_contenido_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        with open(archivo, "r") as f:
            return f.read()

    def obtener_numero_lineas_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return len(self.obtener_contenido_archivo(archivo).splitlines())

    def obtener_numero_palabras_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return len(self.obtener_contenido_archivo(archivo).split())

    def obtener_numero_caracteres_archivo(self, archivo):
        if not archivo.is_file():
            return "La ruta proporcionada no es un archivo válido."
        return len(self.obtener_contenido_archivo(archivo))

    def obtener_numero_subdirectorios(self, directorio):
        if not directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        return len([item for item in directorio.iterdir() if item.is_dir()])

    def obtener_numero_archivos(self, directorio):
        if not directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        return len([item for item in directorio.iterdir() if item.is_file()])

    def obtener_numero_elementos(self, directorio):
        if not directorio.is_dir():
            return "La ruta proporcionada no es un directorio válido."
        return len(list(directorio.iterdir()))

    def obtener_fecha_ultimo_acceso(self, ruta):
        if not ruta.exists():
            return "La ruta proporcionada no existe."
        return ruta.stat().st_atime

    def obtener_fecha_ultimo_cambio(self, ruta):
        if not ruta.exists():
            return "La ruta proporcionada no existe."
        return ruta.stat().st_mtime

    def obtener_espacio_libre(self, ruta):
        if not ruta.exists():
            return "La ruta proporcionada no existe."
        diskUsage = psutil.disk_usage(ruta)
        return diskUsage.free

    def obtener_espacio_ocupado(self, ruta):
        if not ruta.exists():
            return "La ruta proporcionada no existe."
        diskUsage = psutil.disk_usage(ruta)
        return diskUsage.used

    def obtener_espacio_total(self, ruta):
        if not ruta.exists():
            return "La ruta proporcionada no existe."
        diskUsage = psutil.disk_usage(ruta)
        return diskUsage.total

    def sistema(self):
        OS = os.name
        return OS
