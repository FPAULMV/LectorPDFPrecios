import sys
from datetime import datetime
from config import lector

PLANTILLAS = lector.PLANTILLAS_TOML
DATOS_LOGS = lector.LOG_JSON_DICT
CAMPOS_REQUERIDOS = ['time_stamp', 'id', 'level',
                    'msg', 'module_func', 'time_start',
                    'time_end', 'execution_time_seconds']


class EscribirLogs():
    """ Este modulo procesa los logs para el programa."""
    
    def __init__(self):
        self.diccionario_valido_logs = self.comprobar_campos_json(DATOS_LOGS, CAMPOS_REQUERIDOS)
        self.ultimo_registro = self.obtener_ultimo_registro()
        self.siguiente_registro = self.ultimo_registro + 1

    
    def comprobar_campos_json(self, diccionario: dict, campos_requeridos: list) -> dict:
        """
        Devuelve un diccionario con los elementos que cuentan con los campos requeridos.
        Descarta todos los elementos que no coinciden.
        """
        data = {
            k: subdict
            for k, subdict in diccionario.items()
            if set(campos_requeridos) == set(subdict.keys())
        }
        return(data)

    def obtener_ultimo_registro(self) -> int:
        """
        Obtiene el ultimo registro del diccionario.
        """
        if self.diccionario_valido_logs:
            return int(list(self.diccionario_valido_logs.keys())[-1])
        else:
            return 0
        
    def incrementar_registro(self) -> int:
        """
        Incrementa en +1 el valor de siguiente_registro y lo devuelve.
        """
        self.siguiente_registro += 1
        return self.siguiente_registro
        
    def diccionario_tiempos(self, inicio: datetime = "", fin: datetime = "") -> dict:
        """
        Devuelve un diccionario con los tiempos de ejecución formateados.
        """
        if not inicio:
            sys.exit("Falta la fecha de inicio.")
        if not fin:
            sys.exit("Falta la fecha de fin.")
        
        tiempo_total = fin - inicio
        
        # Formatear las fechas
        inicio_formateado = inicio.strftime("%Y-%m-%d %H:%M:%S")
        fin_formateado = fin.strftime("%Y-%m-%d %H:%M:%S")
        
        # Formatear el tiempo de ejecución (segundos con milisegundos)
        segundos_totales = tiempo_total.total_seconds()
        segundos_enteros = int(segundos_totales)
        milisegundos = int((segundos_totales - segundos_enteros) * 1000)
        tiempo_ejecucion = f"{segundos_enteros}.{milisegundos:02d}"

        return {
            "time_start": inicio_formateado,
            "time_end": fin_formateado,
            "execution_time_seconds": tiempo_ejecucion
        }

    def diccionario_completo(self, dict_tiempos: dict, codigo_plantilla: str) -> None:
        _inicio = datetime.now()
        plantilla = PLANTILLAS[codigo_plantilla]
        print(plantilla)
        try: 
            out_dict = {
                    f"{self.siguiente_registro}" : {
                        "id": plantilla['id'],
                        "level": plantilla['level'],
                        "msg": plantilla['msg'],
                        "module_func": plantilla['module_func'],
                        "time_start": dict_tiempos['time_start'],
                        "time_end": dict_tiempos['time_end'],
                        "execution_time_seconds": dict_tiempos['execution_time_seconds'],
                        "time_stamp": format(datetime.now(), "%Y-%m-%d %H:%M:%S")
                        }
                }
            self.incrementar_registro()
            return out_dict
        
        except Exception as e:
            msg = {
                "1009": {"id": "1009", "level": "FATAL", "msg": f"Ocurrió un error al crear el log. DETALLES: {e}", 
                "module_func": "log_writer.py->EscribirLogs.diccionario_completo()", "time_start": f"{_inicio}",
                "time_end": f"{datetime.now()}", "execution_time_seconds": "0", "time_stamp": f"{datetime.now()}"}
                }
            print(msg)


    def registrar_log(self, codigo_plantilla: str, inicio: datetime = "", fin: datetime = "") -> None:
        """
        Registra un log con los datos proporcionados.
        """
        diccionario_tiempos = self.diccionario_tiempos(inicio, fin)
        log_salida = self.diccionario_completo(diccionario_tiempos, codigo_plantilla)
        DATOS_LOGS.update(log_salida)
        lector.escribir_json_logs(DATOS_LOGS)

logger = EscribirLogs()


