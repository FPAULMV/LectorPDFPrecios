import pandas
from pandas import DataFrame
from datetime import datetime
from servicios_sql import sqls
from config import lector
from log_writer import logger 




class ConsultasManejador():
    def __init__(self):
        self.CLIENTES_PORTAL = self._consultar_clientes_portal()
        self.FECHAS_RERGISTRADAS = sqls.consultar(lector.CONSULTAS_SQL['consultas']['ObtenerFechasRegistradas'])

    def _consultar_clientes_portal(self) -> DataFrame: 
        try:
            _inicio = datetime.now()
            clientes = sqls.consultar(lector.CONSULTAS_SQL['consultas']['ObtenerClientesPortal'])
            logger.registrar_log("1019", _inicio)
            return clientes
        except Exception as e:
            
            logger.registrar_log("1020", _inicio)
            pass


consultas_manejador = ConsultasManejador()

class FechasManejador():

    def __init__(self):
        self.FECHAS_FALTANTES = self._fechas_faltantes(self._todas_las_fechas(), consultas_manejador.FECHAS_RERGISTRADAS)

    def _todas_las_fechas(self) -> DataFrame:
        return pandas.DataFrame({"Fecha":pandas.date_range(datetime(2023, 1, 1), datetime.now())})

    def _fechas_faltantes(self, fechas_completas: DataFrame, fechas_incompletas: DataFrame)-> DataFrame:
        """
        Devuelve un DataFrame con los elementos de lista_completa
        que no se encuentran en lista_incompleta.
        """
        return fechas_completas[~fechas_completas['Fecha'].isin(fechas_incompletas['Fecha'])]
    
fechas_manejador = FechasManejador()


