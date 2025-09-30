import pyodbc, pandas
from pandas import DataFrame
from config import CONN_STR
from log_writer import logger 
from datetime import datetime


class ServiciosSql():

    def __init__(self):
        self.conn = self._conectar()

    def _conectar(self) -> None:
        """
        Conecta a la base de datos.
        """
        _inicio = datetime.now()
        try:
            conn = CONN_STR
            logger.registrar_log("1010", _inicio)
            return conn
        except Exception as e:
            print(e)
            logger.registrar_log("1011", _inicio)


    def _desconectar(self) -> None:
        """
        Desconecta a la base de datos.
        """
        _inicio = datetime.now()
        if self.conn:
            self.conn.close()
        logger.registrar_log("1012", _inicio)

    def _consultar(self, query: str)-> DataFrame:
        """
        Realizar consultas a la base de datos y obtener un DataFrame.
        """
        _inicio = datetime.now()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            columnas = [desc[0] for desc in cursor.description]
            resultados = cursor.fetchall()
            df = pandas.DataFrame.from_records(resultados, columns=columnas)
            logger.registrar_log("1013", _inicio)
            return df
        except Exception as e:
            print(e)
            logger.registrar_log("1014", _inicio)
            self._desconectar()
            return None
        
    def _ejecutar(self, query: str) -> None:
        """
        Ejecuta comandos a la base de datos.
        """
        _inicio = datetime.now()
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            logger.registrar_log("1015", _inicio)
        except Exception as e:
            self.conn.rollback()
            logger.registrar_log("1016", _inicio)
        finally:
            self._desconectar()