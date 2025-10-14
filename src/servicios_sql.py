import pyodbc, pandas
from pandas import DataFrame
from config import CONN_STR
from log_writer import logger 
from datetime import datetime




class ServiciosSql():

    def __init__(self):
        self.conn = self.conectar()

    def conectar(self) -> None:
        """
        Conecta a la base de datos.
        """
        _inicio = datetime.now()
        try:
            conn = pyodbc.connect(CONN_STR)
            logger.registrar_log("1012", _inicio)
            return conn
        except Exception as e:
            print(e)
            logger.registrar_log("1013", _inicio)

    def desconectar(self) -> None:
        """
        Desconecta a la base de datos.
        """
        _inicio = datetime.now()
        if self.conn:
            self.conn.close()
        logger.registrar_log("1014", _inicio)

    def consultar(self, query: str)-> DataFrame:
        """
        Realizar consultas a la base de datos y obtener un DataFrame.
        """
        _inicio = datetime.now()
        query = query.strip()
        if not query:
            logger.registrar_log("1021", _inicio)
            return pandas.DataFrame()

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            columnas = [desc[0] for desc in cursor.description]
            resultados = cursor.fetchall()
            df = pandas.DataFrame.from_records(resultados, columns=columnas)
            logger.registrar_log("1015", _inicio)
            return df
        except Exception as e:
            print(e)
            logger.registrar_log("1016", _inicio)
            self.desconectar()
            return None
        
    def ejecutar(self, query: str) -> None:
        """
        Ejecuta comandos a la base de datos.
        """
        _inicio = datetime.now()
        query = query.strip()
        if not query:
            logger.registrar_log("1022", _inicio)

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            logger.registrar_log("1017", _inicio)
        except Exception as e:
            print(e)
            logger.registrar_log("1018", _inicio)
            self.conn.rollback()
        finally:
            self.desconectar()

sqls = ServiciosSql()


