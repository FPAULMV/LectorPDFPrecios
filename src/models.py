import pandas, sys
from pathlib import Path
from pandas import DataFrame
from datetime import datetime
from servicios_sql import sqls
from config import lector
from config import MSG_SALIDA_FINALIZAR, RUTA_DIRECTORIO_LECTOR
from log_writer import logger 





class ConsultasManejador():
    """
    Manejador para las consultas a la base de datos.
    """

    def __init__(self):
        self.CLIENTES_PORTAL = self._consultar_clientes_portal()
        self.FECHAS_RERGISTRADAS = self._consultar_fechas_registradas()
        self._validar_resultados()

    def _consultar_clientes_portal(self) -> DataFrame: 
        """
        Consulta la informacion de los clientes activos.
        """
        try:
            _inicio = datetime.now()
            clientes = sqls.consultar(lector.CONSULTAS_SQL['consultas']['ObtenerClientesPortal'])
            logger.registrar_log("1019", _inicio)
            return clientes
        except Exception as e:
            print(e)
            logger.registrar_log("1020", _inicio)
            sys.exit(MSG_SALIDA_FINALIZAR)

    def _consultar_fechas_registradas(self) -> DataFrame: 
        """
        Consulta informacion de los precios registrados.
        """
        try:
            _inicio = datetime.now()
            clientes = sqls.consultar(lector.CONSULTAS_SQL['consultas']['ObtenerFechasRegistradas'])
            logger.registrar_log("1023", _inicio)
            return clientes
        except Exception as e:
            print(e)
            logger.registrar_log("1024", _inicio)
            sys.exit(MSG_SALIDA_FINALIZAR)
        
    def _validar_resultados(self) -> None:
        """
        Valida que las consultas tengan contenido.
        """
        _inicio = datetime.now()
        def _esta_vacio(df) -> None:
            return (df is None) or (df.empty if isinstance(df, DataFrame) else True)
        
        vacios = []
        if _esta_vacio(self.CLIENTES_PORTAL):
            vacios.append(1)
        if _esta_vacio(self.FECHAS_RERGISTRADAS):
            vacios.append(2)

        if vacios:
            logger.registrar_log("1025", _inicio)
            sys.exit(MSG_SALIDA_FINALIZAR)

# consultas_manejador = ConsultasManejador()


class FechasManejador():
    """
    Manejador la para las fechas faltantes de registrar.
    """

    def __init__(self):
        self.FECHAS_FALTANTES = self._fechas_faltantes(self._todas_las_fechas(), consultas_manejador.FECHAS_RERGISTRADAS)

    def _todas_las_fechas(self) -> DataFrame:
        """
        Obtiene todas las fechas que deberian de estar registradas desde el 2023-01-01.
        """
        return pandas.DataFrame({"Fecha":pandas.date_range(datetime(2023, 1, 1), datetime.now())})

    def _fechas_faltantes(self, fechas_completas: DataFrame, fechas_incompletas: DataFrame)-> DataFrame:
        """
        Devuelve un DataFrame con las fechas faltantes de registrar.
        """
        return fechas_completas[~fechas_completas['Fecha'].isin(fechas_incompletas['Fecha'])]
    
# fechas_manejador = FechasManejador()


class ArchivosManejador():
    """
    Manejador para las rutas de los archivos del aplicativo.
    """
    def __init__(self):
        self._validar_directorio_vacio()
        self.archivos = self._obtener_archivos()
        # Es una: list[Path] con los archivos '.pdf' encontrados.
        self.archivos_filtrados = self._filtar_archivos(self.archivos)
        # self._eliminar_contenido_directorio() <- Se usara en otro momento. 

    def _validar_directorio_existe(self) -> bool:
        """
        Valida que las ruta al directorio existe.
        """
        _inicio = datetime.now()
        if RUTA_DIRECTORIO_LECTOR.exists() and RUTA_DIRECTORIO_LECTOR.is_dir():
            logger.registrar_log("1026", _inicio)
            return True
        else:
            logger.registrar_log("1027", _inicio)
            sys.exit(MSG_SALIDA_FINALIZAR)

    def _validar_directorio_vacio(self):
        """
        Valida si el directorio tiene elmenetos.
        """
        _inicio = datetime.now()
        self._validar_directorio_existe()
        _es_vacio = not any(RUTA_DIRECTORIO_LECTOR.iterdir())
        if not _es_vacio:
            logger.registrar_log("1028", _inicio)
            return True
        else:
            logger.registrar_log("1029", _inicio)
            sys.exit(MSG_SALIDA_FINALIZAR)

    def _obtener_archivos(self) -> list:
        """
        Obtiene todas las rutas a los archivos de un directorio.
        """
        _inicio = datetime.now()
        self._validar_directorio_existe()
        try :
            archivos = [archivo for archivo in RUTA_DIRECTORIO_LECTOR.iterdir() if archivo.is_file()]
            logger.registrar_log("1030", _inicio)
            return archivos
        except Exception as e:
            print(e)
            logger.registrar_log("1031", _inicio)
            return None

    def _filtar_archivos(self, archivos: list) -> list:
        """
        Obtiene los archivos filtrados por '.pdf'.
        """
        _inicio = datetime.now()
        self._validar_directorio_existe()
        try :
            archivos_filtrados = [archivo for archivo in archivos if archivo.suffix.lower() == ".pdf"]
            logger.registrar_log("1032", _inicio)
            return archivos_filtrados
        except Exception as e:
            print(e)
            logger.registrar_log("1033", _inicio)
            return None

    def _eliminar_contenido_directorio(self) -> None:
        """
        Elimina el contenido del directorio asignado para resivir los pdf
        """
        _inicio = datetime.now()
        self._validar_directorio_existe()
        eliminados = []
        for elemento in RUTA_DIRECTORIO_LECTOR.iterdir():
            if elemento.is_file():
                try:
                    elemento.unlink()
                    logger.registrar_log("1034", _inicio, elemento)
                except Exception as e:
                    logger.registrar_log("1035", _inicio, e)
            elif elemento.is_dir():
                try: 
                    elemento.rmdir()
                    logger.registrar_log("1036", _inicio)
                except Exception as e:
                    logger.registrar_log("1037", _inicio, e)

            eliminados.append(elemento)
            print(f"Contenido elimindao {elemento}.")
        return eliminados
