import versioning, json, tomllib, tomli_w, os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv


# Rutas a archivos necesarios para app. (En crudito)
RUTA_PLANTILLAS_LOGS = Path(r"utils\plantillas_logs.toml") 
RUTA_SETTINGS_JSON = Path(r"utils\settings.json")
RUTA_LOGS_JSON = Path(r"..\storage\logs\log_app_.json")
RUTA_QUERYS = Path(r"utils\querys.toml")
RUTA_ENV = Path(r"..\.env")

#Plantilla para json vacio. 
JSON_VACIO_PLANTILLA = {"0": {"id": "1000", "level": "INFO", "msg": "EMPTY", "module_func": "EMPTY", "time_start": "0", "time_end": "0", "execution_time_seconds": "0", "time_stamp":"0"}}
# Texto por default en caso de que el archivo de plantillas fuese eliminado o este corrupto.
TEXTO_CONFIGURACION_POR_DEFECTO = {
    "1009": {"id": "1001", "level": "", "msg": "", "module_func": ""},
    "1010": {"id": "1002", "level": "", "msg": "", "module_func": ""}
    }

# Cargar variables de entorno .env
load_dotenv()
CONN_STR = os.getenv("CONN_STR")

class LeerArchivosConfiguraciones():

    def __init__(self):
        self.LOG_JSON_DICT = self.leer_json_logs()
        self.PLANTILLAS_TOML = self.leer_plantillas_toml()
        self.CONSULTAS_SQL = self.leer_query_sql()
        
    def _crear_file(self, ruta_archivo: Path) -> None:
        """Crear un archivo."""
        try:
            ruta_archivo.touch()
        except Exception as e:
            msg = {
                "1001": {"id": "1001", "level": "ERROR", "msg": f"Ocurrio un error al crear el archivo: {ruta_archivo}. DETALLES: {e}", 
                "module_func": "config.py->LeerArchivosConfiguraciones._crear_file()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')


    def _escribir_file(self, data: dict, ruta_archivo: Path) -> None:
        """Escribe en un archivo."""
        try:
            ruta_archivo.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding='utf-8')
        except Exception as e:
            msg = {
                "1002": {"id": "1002", "level": "ERROR", "msg": f"Ocurrio un error al escribir en el archivo: {ruta_archivo}. DETALLES: {e}", 
                "module_func": "config.py->LeerArchivosConfiguraciones._escribir_file()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')
            

    def _escribir_toml(self, data: dict, ruta_archivo: Path) -> None:
        """Escribe un diccionario en un archivo TOML."""
        try:
            with ruta_archivo.open("wb") as f:
                tomli_w.dump(data, f)  # dump convierte dict -> TOML y escribe
            msg = {
                "1003": {"id": "1003", "level": "INFO", "msg": f"Se guardo correctamente la informacion en: {ruta_archivo}.", 
                "module_func": "config.py->LeerArchivosConfiguraciones._escribir_toml()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')
        except Exception as e:
            msg = {
                "1004": {"id": "1004", "level": "ERROR", "msg": f"Ocurrio un error al escribir en el archivo: {ruta_archivo}. DETALLES: {e}", 
                "module_func": "config.py->LeerArchivosConfiguraciones._escribir_toml()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')

    def _leer_json(self, ruta_archivo: Path) -> dict:
        """Obtiene la informacion de un archivo JSON."""
        try:
            with ruta_archivo.open('r', encoding= 'utf-8') as f:
                data = json.load(f)
            msg = {
                "1005": {"id": "1005", "level": "INFO", "msg": f"Se obtubo la informacion del archivo: {ruta_archivo}", 
                "module_func": "config.py->LeerArchivosConfiguraciones._leer_json()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')
            return data
        except (json.JSONDecodeError) as e:
            msg = {
                "1006": {"id": "1006", "level": "ERROR", "msg": f"No se pudo leer el archivo: {ruta_archivo}. DETALLES: {e}", 
                "module_func": "config.py->LeerArchivosConfiguraciones._leer_json()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')
            return {}

    def _leer_toml(self, ruta_archivo: Path) -> dict:
        """Obtiene la información de un archivo TOML"""
        try:
            with ruta_archivo.open('rb') as f:
                data = tomllib.load(f)
            msg = {
                "1007": {"id": "1007", "level": "INFO", "msg": f"Se obtubo la informacion del archivo: {ruta_archivo}.", 
                "module_func": "config.py->LeerArchivosConfiguraciones._leer_toml()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')
            return data
        except (tomllib.TOMLDecodeError) as e:
            msg = {
                "1008": {"id": "1008", "level": "ERROR", "msg": f"No se pudo leer el archivo TOML: {ruta_archivo}. DETALLES: {e}", 
                "module_func": "config.py->LeerArchivosConfiguraciones._leer_toml()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')
        except Exception as e:
            msg = {
                "1009": {"id": "1009", "level": "ERROR", "msg": f"Ocurrió un error inesperado al leer el archivo TOML: {ruta_archivo}. DETALLES: {e}", 
                "module_func": "config.py->LeerArchivosConfiguraciones._leer_toml()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')


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
            self._escribir_file(JSON_VACIO_PLANTILLA, RUTA_LOGS_JSON)

        data = self._leer_json(RUTA_LOGS_JSON)
        return data
        
    def escribir_json_logs(self, data_log: dict):
        """
        Escribe dentro de un archivo json. 
            - Valida que el documento exite o lo crea con el archivo con el contenido.
            - Escribe logs.
            
        Retorna: 
            None
        """
        if not RUTA_LOGS_JSON.exists():
            self._crear_file(RUTA_LOGS_JSON)
            self._escribir_file(data_log, RUTA_LOGS_JSON)
        else:
            self._escribir_file(data_log, RUTA_LOGS_JSON)


    def leer_plantillas_toml(self):
        """
        Obtiene la informaicion de un archivo toml.
            - Valida que el documento exite o lo crea con la plantilla por defecto.
            - Que no esté corrupto.             
        Retorna: 
            dict: Con la informacion del 'archivo.toml'.
        """
        if not RUTA_PLANTILLAS_LOGS.exists():
            self._crear_file(RUTA_PLANTILLAS_LOGS)
            self._escribir_toml(TEXTO_CONFIGURACION_POR_DEFECTO, RUTA_PLANTILLAS_LOGS)

        data = self._leer_toml(RUTA_PLANTILLAS_LOGS)
        return data

    def leer_query_sql(self) -> dict:
        """
        Obtiene la informaicion de un archivo toml.
            - Valida que el documento exite.
            - Que no esté corrupto.             
        Retorna: 
            dict: Con la informacion del 'archivo.toml'.
        """
        try: 
            if RUTA_PLANTILLAS_LOGS.exists():
                querys = self._leer_toml(RUTA_QUERYS)
                return querys
        except Exception as e:
            msg = {
                "1019": {"id": "1019", "level": "ERROR", "msg": f"Ocurrió un error inesperado al leer el archivo: {RUTA_QUERYS}. DETALLES: {e}", 
                "module_func": "config.py->LeerArchivosConfiguraciones._leer_toml()", "time_start": f"{datetime.now()}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg, end='\n\n')    



lector = LeerArchivosConfiguraciones()