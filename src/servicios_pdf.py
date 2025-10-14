from PyPDF2 import PdfReader
from pathlib import Path
from log_writer import logger, datetime



class PdfManejador():

    def __init__(self, ruta_archivo: Path):
        self.ruta_archivo = ruta_archivo
        self.reader = PdfReader(Path(self.ruta_archivo))
        pass

    def _validar_archivo(self) -> bool:
        _inicio = datetime.now()
        if not self.ruta_archivo.exists() or not self.ruta_archivo.is_file():
            error = str(FileNotFoundError(f"La ruta {self.ruta_archivo} no es valida o no existe."))
            logger.registrar_log('1038', _inicio, error)
        
        if self.ruta_archivo.suffix.lower() != '.pdf':
            error = str(FileNotFoundError(f"La ruta {self.ruta_archivo} no es una extencion '.pdf' valida"))
            logger.registrar_log('1039', _inicio, error)


    def obtener_texto(self) -> str:
        """
        Extrae la informacion de un '.pdf'.
        """
        _inicio = datetime.now()
        self._validar_archivo()
        texto = ""
        pagina_countador = 0
        try:
            for pagina in self.reader.pages:
                pagina_countador += 1
                texto += pagina.extract_text() or ""
            logger.registrar_log('1040', _inicio)
        
        except Exception as e:
            err_msg = f"Error en la pagina: {pagina_countador} ERROR: {e}"
            logger.registrar_log('1041', _inicio, err_msg)
            
        return texto
        

    def obtener_metadatos(self) -> dict:
        """
        Obtiene los metadatos del '.pdf'.
        """
        _inicio = datetime.now()
        self._validar_archivo()
        metadatos = self.reader.metadata or {}

        datos = {
            "titulo": metadatos.get("/Title"),
            "autor": metadatos.get("/Author"),
            "productor": metadatos.get("/Producer"),
            "fecha_creacion": metadatos.get("/CreationDate"),
            "fecha_modificacion": metadatos.get("/ModDate"),
            "paginas": len(self.reader.pages)
        }
        logger.registrar_log('1042', _inicio)
        return datos

    # Aun sin desarrollar. 
    # def es_escaneo(self) -> bool:
    #    pass