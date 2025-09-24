
import json, tomllib
from pathlib import Path


# Rutas a archivos necesarios para app. (En crudito)
RUTA_PLANTILLAS_LOGS = Path(r"utils\plantillas_logs.toml") 
RUTA_SETTINGS_JSON = Path(r"utils\settings.json")
RUTA_LOGS_JSON = Path(r"..\storage\logs\log_app_.json")


# Texto por default en caso de que el archivo de plantillas fuese eliminado o este corrupto.
TEXTO_CONFIGURACION_POR_DEFECTO = """# Plantilla creada al no encontrar el archivo.

[1001]
"id" = "1001" # Igual que la tabla -> [1001]
"level" = ""
"msg" = ""
"module_func" = ""

# ---

[1002]
"id" = "1002" # Igual que la tabla -> [1002]
"level" = "WARN"
"msg" = "No se encontro el archivo 'plantillas_logs.toml' y fue creado nuevamente con la plantilla por defecto."
"module_func" = "log_writer.py -> EscribirLogs.leer_plantillas_toml"

[1003]
"id" = "1003"
"level" = "DEBUG"
"msg" = "Informacion de 'plantillas_logs.toml' cargada correctamente."
"module_func" = "log_writer.py -> EscribirLogs.leer_plantillas_toml"
"""



class Configuraciones():
    def __init__(self):
        pass


class LeerArchivosConfiguraciones():

    def __init__(self):
        self.LOG_JSON_DICT = self.leer_json_logs()
        self.PLANTILLAS_TOML = self.leer_plantillas_toml()
        
    def _crear_file(self, ruta_archivo: Path) -> None:
        """Crear un archivo."""
        try:
            ruta_archivo.touch()
        except Exception as e:
            print(f"['1001'] - ERROR - Ocurrio un error al crear el archivo: \n{ruta_archivo}.\n--- DETALLES DEL ERROR ---\n{e}\n")


    def _escribir_file(self, data: dict, ruta_archivo: Path) -> None:
        """Escribe en un archivo."""
        try:
            ruta_archivo.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding='utf-8')
        except Exception as e:
            print(f"['1002'] - ERROR - Ocurrio un error al escribir en el archivo: \n{ruta_archivo}.\n--- DETALLES DEL ERROR ---\n{e}\n")


    def _leer_json(self, ruta_archivo: Path) -> dict:
        """Obtiene la informacion de un archivo JSON."""
        try:
            with ruta_archivo.open('r', encoding= 'utf-8') as f:
                data = json.load(f)
            print(f"['1006'] - INFO - Se obtubo la informacion del archivo: \n{ruta_archivo}")
            return data
        except (json.JSONDecodeError) as e:
            print(f"['1003'] - ERROR - No se pudo leer el archivo: \n{ruta_archivo}.\n--- DETALLES DEL ERROR ---\n{e}\n")

    def _leer_toml(self, ruta_archivo: Path) -> dict:
        """Obtiene la información de un archivo TOML"""
        try:
            with ruta_archivo.open('rb') as f:
                data = tomllib.load(f)
                print(f"['1007'] - INFO - Se obtubo la informacion del archivo: \n{ruta_archivo}")
            return data
        except (tomllib.TOMLDecodeError) as e:
            print(f"['1004'] - No se pudo leer el archivo TOML: \n{ruta_archivo}.\n--- DETALLES DEL ERROR ---\n{e}\n")
        except Exception as e:
            print(f"['1005'] - Ocurrió un error inesperado al leer el archivo TOML: \n{ruta_archivo}.\n--- DETALLES DEL ERROR ---\n{e}\n")


    def leer_json_logs(self) -> dict:
        """
        Obtiene la informaicion de un archivo json.
            - Valida que el documento exite o lo crea vacio.
            - Que no esté corrupto.             
        Retorna: 
            dict: Con la informacion del archivo.json.
        """
        if not RUTA_LOGS_JSON.exists():
            self._crear_file(RUTA_LOGS_JSON)
            self._escribir_file({}, RUTA_LOGS_JSON)

        data = self._leer_json(RUTA_LOGS_JSON)
        return data
        
    def escribir_json_logs(self):
        """
        Escribe dentro de un archivo json. 
            - Valida que el documento exite o lo crea con el archivo con el contenido.
            - Escribe logs.
            
        Retorna: 
            None
        """
        if not RUTA_LOGS_JSON.exists():
            self._crear_file(RUTA_LOGS_JSON)
            self._escribir_file(self.LOG_JSON_DICT, RUTA_LOGS_JSON)
        else:
            self._escribir_file(self.LOG_JSON_DICT, RUTA_LOGS_JSON)


    def leer_plantillas_toml(self):
        """
        Obtiene la informaicion de un archivo toml.
            - Valida que el documento exite o lo crea con la plantilla por defecto.
            - Que no esté corrupto.             
        Retorna: 
            dict: Con la informacion del archivo.json.
        """
        if not RUTA_PLANTILLAS_LOGS.exists():
            self._crear_file(RUTA_PLANTILLAS_LOGS)
            self._escribir_file(TEXTO_CONFIGURACION_POR_DEFECTO, RUTA_PLANTILLAS_LOGS)

        data = self._leer_toml(RUTA_PLANTILLAS_LOGS)
        return data

lector = LeerArchivosConfiguraciones()