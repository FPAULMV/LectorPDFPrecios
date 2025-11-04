import versioning, pandas, os, sys, urllib.parse
from pathlib import Path
from sqlalchemy import create_engine, text
from pandas import DataFrame
from dotenv import load_dotenv



# Se cargan las variables de entorno .env.

try:
    #Agregar Log.info
    load_dotenv()
    CONN_STR = os.getenv('CONN_STR')
    PATH_FOLDER = os.getenv('PATH_FOLDER')
    HOST = str(os.getenv('HOST'))
    PORT = int(os.getenv('PORT'))
    USER = str(os.getenv('USER'))
    PSW = str(os.getenv('PSW'))
    odbc_encoded = urllib.parse.quote_plus(CONN_STR)
    engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={odbc_encoded}",
    pool_pre_ping=True,fast_executemany=True)
    print("\n--- Variables de entorno cargadas con exito. ---\n")


except Exception as e:
    # Agregar Log.Error
    print("Hubo un error al cargar las variables de entorno.")
    print(e)
finally:
    #Agregar Log.info
    print("-> FIN: de la carga de las variables de entorno.\n")
# ------------------------------------------------------------------------

# Validar que el directorio existe.
try:
    #Agregar Log.info
    PATH_FOLDER = Path(PATH_FOLDER)
    if PATH_FOLDER.exists() and PATH_FOLDER.is_dir():
        pass
    else: 
        print(f"La ruta no es un directorio o no existe.")
        sys.exit(1)
except Exception as e:
    # Agregar Log.Error
    print("Hubo un error al acceder al directorio de los archivos.")
    print(e)
    sys.exit(1)
finally:
    #Agregar Log.info
    print("-> FIN: Termino la validacion del directorio con los pdf\n")
# ------------------------------------------------------------------------


# Validar si el folder de los archivos esta vacio.
try:
    #Agregar Log.info
    if not any(PATH_FOLDER.iterdir()):
        print("El directorio se encuentra vacio.")
        sys.exit(0)

except Exception as e:
    # Agregar Log.Error
    print("Hubo un error al comprobar el contenido del directorio.")
    print(e)

finally:
    #Agregar Log.info
    pass
    print("-> FIN: Termino de comprabar si el directorio tiene elementos.\n")
# ------------------------------------------------------------------------


# Obtiene una lista de los archivos del directorio de archivos.
try:
    #Agregar Log.info
    ARCHIVOS_OBTENIDOS = [p for p in PATH_FOLDER.iterdir() if p.is_file and p.suffix.lower() == '.pdf']
    if not ARCHIVOS_OBTENIDOS:
        print("INFO: - No se encontraron archivos pdf para validar.\n")
        sys.exit("-> Fin de la ejecucion del programa. <-".upper())
except Exception as e:
    # Agregar Log.Error
    print("Hubo un error al crear la lista con las rutas a los archivos.")
    print(e)
finally:
    #Agregar Log.info
    print("-> FIN: Termino la obtencion de las rutas a los archivos pdf.\n")
# ------------------------------------------------------------------------


# Valida que el documento existe, es un archiv y el contenido es accesible.

from PyPDF2 import PdfReader
from typing import Pattern, Optional
import re

def _validar_archivo(archivo: Path) -> bool:
    """
    Valida que el archivo exita, sea un archivo y 
    se pueda accederal contenido.
    """

    if not archivo.exists():
        print(f"El archivo al que se quiere acceder NO EXISTE.\nARCHIVO: {archivo}")
        return False
    
    if not archivo.is_file():
        print(f"La ruta a la que se quiere acceder NO ES UN ARCHIVO.\nARCHIVO: {archivo}")
        return False

    if not os.access(archivo, os.R_OK):
        print(f"No se puede acceder a la informacion del archivo.\nARCHIVO: {archivo}")
        return False  
    return True

for archivo in ARCHIVOS_OBTENIDOS:
    print("Trabajando con el archivo:")
    print(archivo)

    reader = PdfReader(Path(archivo))

    # Se consulta a la base de datos los clientes activos. 
    try:
        #Agregar Log.info
        query = "SELECT DISTINCT(Id) FROM [NexusFuel].[Portal].[ClientUser] ORDER BY [Id] DESC"
        with engine.connect() as conn:
            CLIENTES_ACTIVOS = pandas.read_sql(query, conn)
    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al consultar la informacion de los clientes activos.")
        print(e)
    finally:
        #Agregar Log.info
        engine.dispose()
        print("-> FIN: de la consulta de clientes unicos.\n")
    # ------------------------------------------------------------------------

    # Se consulta la informacion de las fechas de precios registradas.
    try: 
        #Agregar Log.info
        query = "SELECT DISTINCT [Fecha], [Tad] FROM [Sinergia_Aux].[dbo].[PreciosPemex_New] ORDER BY [Fecha], [Tad];"
        with engine.connect() as conn:
            FECHAS_REGISTRADAS = pandas.read_sql(query, conn)
    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al consultar la informacion de los precios registrados.")
        print(e)
    finally:
        #Agregar Log.info
        engine.dispose()    
        print("-> FIN: de la consulta de los precios registrados.\n")
    # ------------------------------------------------------------------------


    # Validar que los DataFrame obtenidos no esten vacios.
    try:
        #Agregar Log.info
        if CLIENTES_ACTIVOS.empty:
            print("El DataFrame para los clientes activos está vacio.")
            sys.exit(1)

        if FECHAS_REGISTRADAS.empty:
            print("El DataFrame para los precios registrados está vacio.")
            sys.exit(1)
    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al validar el contenido de los DataFrame.")
        print(e)
    finally:
        # Agregar Log.Error
        print("-> FIN: Termino la validacion de los DataFrame.\n")
    # ------------------------------------------------------------------------
    try:
        #Agregar Log.info
        if not _validar_archivo(archivo):
            sys.exit(1)

    except Exception as e:
        # Agregar Log.Error

        print("Hubo un error al validar el archivo.")
        print(e)

    finally:
        #Agregar Log.info
        pass
        print(f"-> FIN: Termino la validacion del archivo. {archivo}\n")
    # -------------------------------------------------------------

    # Obtiene el contenido del archivo pdf.
    try:
        #Agregar Log.info
        TEXTO_EXTRAIDO = ""
        PAGINAS_LEIDAS = 0
        MAX_PAGINAS = 5
        for page in reader.pages:
            if PAGINAS_LEIDAS < MAX_PAGINAS:
                TEXTO_EXTRAIDO += page.extract_text().upper() or ""
                PAGINAS_LEIDAS += 1
            else:
                print("Se alcanzo el limite de paginas a leer.")

    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al extraer el texto del pdf")
        print(e)
    finally:
        #Agregar Log.info
        print("-> FIN: Termino la extraccion del texto del pdf.\n")
    # -------------------------------------------------------------


    def _normalizar_lineas(linea: str) -> str:
        """
        Normaliza el texto del pdf para manejarlo.
        """
        a = re.sub(r"\s+", " ", linea).strip()
        b = a.replace(",", "").replace("*", "")
        return b
    
    # Mensaje
    TEXTO_NORMALIZADO = []
    try:
        #Agregar Log.info
        for linea in TEXTO_EXTRAIDO.splitlines():
            linea_normalizada = _normalizar_lineas(linea)
            TEXTO_NORMALIZADO.append(linea_normalizada)
    except Exception as e:
        # Agregar Log.Error

        print("Hubo un error al normalizar el texto del archivo.")
        print(e)
    finally:
        #Agregar Log.info
        pass
        print("-> FIN: Termino la normalizacion del texto del archivo.\n")
    # -------------------------------------------------------------

    # Extrae solo las lineas importantes del documento.
    # Expreciones regulares que nos ayudan a definir las lineas de texto que
    # concideramos importantes.
    REG_DATOS = re.compile(
                r"^(?P<tad>\d+)\s+(?P<nombre>[A-ZÁÉÍÓÚÑ\s]+?)\s+"
                r"(?P<p1>\d+\.\d{5})(?:\s+(?P<p2>\d+\.\d{5}))?(?:\s+(?P<p3>\d+\.\d{5}))?$"
                )

    REG_FECHA_SIMP = re.compile(
                r"DEL\s+(?P<d1>\d{1,2})\s+AL\s+(?P<d2>\d{1,2})\s+DE\s+(?P<m>[A-ZÁÉÍÓÚÜÑ]+)\s+DE\s+(?P<y>\d{4})",
                re.IGNORECASE
                )

    REG_FECHA_CRUZ = re.compile(
                r"DEL\s+(?P<d1>\d{1,2})\s+DE\s+(?P<m1>[A-ZÁÉÍÓÚÜÑ]+)\s+AL\s+(?P<d2>\d{1,2})\s+DE\s+(?P<m2>[A-ZÁÉÍÓÚÜÑ]+)\s+DE\s+(?P<y>\d{4})",
                re.IGNORECASE
                )

    LISTA_FECHAS_SIMPLES = [] # Usar solo el primer elemento.
    LISTA_FECHAS_CRUZADAS = []
    LISTA_DATOS_EXTRAIDOS = []

    def patron_match(patron: Pattern[str], linea: str) -> Optional[re.Match]:
            """
            Busca en una linea de texto coincidencias en el patron si hace matchTu ubicación
            devuelve la linea encontrada
            """
            texto = patron.search(linea)
            return texto.group(0) if texto else None

    # Ordena la informacion relevante.
    try:
        for linea in TEXTO_NORMALIZADO:
            #Agregar Log.info
            coincidencia_fecha_simple = patron_match(REG_FECHA_SIMP, linea)
            if coincidencia_fecha_simple:
                LISTA_FECHAS_SIMPLES.append(coincidencia_fecha_simple)

            coincidencia_fecha_compuesta = patron_match(REG_FECHA_CRUZ, linea)
            if coincidencia_fecha_compuesta:
                LISTA_FECHAS_CRUZADAS.append(linea)

            coincidencia_datos = patron_match(REG_DATOS, linea)
            if coincidencia_datos:
                LISTA_DATOS_EXTRAIDOS.append(linea)
    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al ordenar las coincidencias en las lineas del texto")
        print(e)

    finally:
        #Agregar Log.info
        print("-> FIN: Termino la busqueda de coincidencias en las lineas del texto.\n")  
    # -------------------------------------------------------------

    if LISTA_FECHAS_SIMPLES:
        FECHA_OBTENIDA = {}
        # Obtiene: Dia inicio, dia fin, mes y año de la fecha encontrada en el formato simple.
        try:
            #Agregar Log.info
            
            fecha_simple_primer_elemento = LISTA_FECHAS_SIMPLES[0]
            reg_ex_simp = REG_FECHA_SIMP.search(fecha_simple_primer_elemento)

            if fecha_simple_primer_elemento:
                FECHA_OBTENIDA.update({
                    "dia_uno": reg_ex_simp.group('d1'),
                    "dia_dos": reg_ex_simp.group('d2'),
                    "mes": reg_ex_simp.group('m'),
                    "año": reg_ex_simp.group('y')
                })
            else:
                print("La lista: {LISTA_FECHAS_SIMPLES} esta vacia.")

        except Exception as e:
            # Agregar Log.Error
            print("Hubo un error al obtener la información de: '{fecha_simple_primer_elemento}'")
            print(type(e).__name__, e)
            sys.exit(1)
        finally:
            #Agregar Log.info
            print("-> FIN: Terminó la extracción de la información de fechas en formato siemple.\n")
# -------------------------------------------------------------

    elif LISTA_FECHAS_CRUZADAS:
        # Obtiene: Dia inicio, dia fin, mes y año de la fecha 
        # encontrada en el formato FEHCAS CRUSADAS.
        try:
            #Agregar Log.info
            fecha_cruzadas_primer_elemento = LISTA_FECHAS_CRUZADAS[0]
            reg_ex_crus = REG_FECHA_CRUZ.search(fecha_cruzadas_primer_elemento)

            if fecha_cruzadas_primer_elemento:
                FECHA_OBTENIDA.update({
                    "dia_uno": reg_ex_crus.group('d1'),
                    "dia_dos": reg_ex_crus.group('d2'),
                    "mes_uno": reg_ex_crus.group('m1'),
                    "mes_dos": reg_ex_crus.group('m2'),
                    "año": reg_ex_crus.group('y'),
                })
            else:
                print("La lista: {LISTA_FECHAS_CRUZADAS} esta vacia.")
        except Exception as e:
            # Agregar Log.Error
            print("Hubo un error al obtener la información de: '{fecha_cruzadas_primer_elemento}'")
            print(type(e).__name__, e)
            sys.exit(1)
        finally:
            #Agregar Log.info
            pass
            print("-> FIN: Terminó la extracción de la información de fechas en formato cruzado.\n")
    else:
        print("Las listas de fechas se encuentran vacias. El programa finalizara.")
        sys.exit(1)
    # -------------------------------------------------------------



    # Obtiene: Un diccionario con la informacion de cada elemento
    # en la lista LISTA_DATOS_EXTRAIDOS.
    DICCIONARIO_DATOS = []
    try:
        #Agregar Log.info
        if LISTA_DATOS_EXTRAIDOS:
            for elemento in LISTA_DATOS_EXTRAIDOS:
                reg_ex_dato = REG_DATOS.search(elemento)
                if reg_ex_dato:
                    if reg_ex_dato.group('p3') == None:
                        diccionario_de_elementos = {
                            "tad": reg_ex_dato.group('tad'),
                            "tad_nombre": reg_ex_dato.group('nombre'),
                            "precio_magna": reg_ex_dato.group('p1'),
                            "precio_premium": None,
                            "precio_diesel": reg_ex_dato.group('p2')
                        }
                        DICCIONARIO_DATOS.append(diccionario_de_elementos)
                    else:
                        diccionario_de_elementos = {
                            "tad": reg_ex_dato.group('tad'),
                            "tad_nombre": reg_ex_dato.group('nombre'),
                            "precio_magna": reg_ex_dato.group('p1'),
                            "precio_premium": reg_ex_dato.group('p2'),
                            "precio_diesel": reg_ex_dato.group('p3')
                        }
                        DICCIONARIO_DATOS.append(diccionario_de_elementos)

                else:
                    print("No se encontro un dato que coincida para el elemento: {elemento}")
                    print(f"valor actualmente asignado a la varieble: -> {elemento}")
                    print("en la lista: {LISTA_DATOS_EXTRAIDOS}")
        else:
            print("La lista: {LISTA_DATOS_EXTRAIDOS} esta vacia.")

        pass
    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al obtener el diccionario de datos para {LISTA_DATOS_EXTRAIDOS}")
        print(e)
        sys.exit(1)
    finally:
        #Agregar Log.info
        print("-> FIN: Termino la creacion del diccionario con los datos de: {LISTA_DATOS_EXTRAIDOS}\n")
    # -------------------------------------------------------------


    from datetime import date, timedelta

    def _obtener_mes(mes: str) -> int:
        mes = mes.upper().strip().replace(" ", "")
        meses = {
            "ENERO": 1,
            "FEBRERO": 2,
            "MARZO": 3,
            "ABRIL": 4,
            "MAYO": 5,
            "JUNIO": 6,
            "JULIO": 7,
            "AGOSTO": 8,
            "SEPTIEMBRE": 9,
            "OCTUBRE": 10,
            "NOVIEMBRE": 11,
            "DICIEMBRE": 12
        }
        return int(meses[mes])
    
    # Obtiene el rango de fechas de la fecha obtenida.
    try:
        FECHA_INICIO_OBTENIDA = None
        FECHA_FIN_OBTENIDA = None
        RANGO_DE_FECHAS = []

        #Agregar Log.info
        if len(FECHA_OBTENIDA) == 4:
            _dia_uno = int(FECHA_OBTENIDA['dia_uno'])
            _dia_dos = int(FECHA_OBTENIDA['dia_dos'])
            _mes = int(_obtener_mes(FECHA_OBTENIDA['mes']))
            _año = int(FECHA_OBTENIDA['año'])

            FECHA_INICIO_OBTENIDA = date(_año, _mes, _dia_uno) 
            FECHA_FIN_OBTENIDA = date(_año, _mes, _dia_dos) 
        
            if FECHA_INICIO_OBTENIDA < FECHA_FIN_OBTENIDA:
                RANGO_DE_FECHAS = [FECHA_INICIO_OBTENIDA + timedelta(days=i) 
                    for i in range((FECHA_FIN_OBTENIDA - FECHA_INICIO_OBTENIDA).days + 1)]
                
            else:
                print("Algo ocurrio al momento de obtener las fechas, la {FECHA_INICIO_OBTENIDA}")
                print(f"con un valor de: -> {FECHA_INICIO_OBTENIDA}")
                print("deberia de ser menor a {FECHA_FIN_OBTENIDA}")
                print(f"que tiene valor de: -> {FECHA_FIN_OBTENIDA}")
                break

        elif len(FECHA_OBTENIDA) == 5:
            _dia_uno = int(FECHA_OBTENIDA['dia_uno'])
            _dia_dos = int(FECHA_OBTENIDA['dia_dos'])
            _mes_uno = int(_obtener_mes(FECHA_OBTENIDA['mes_uno']))
            _mes_dos = int(_obtener_mes(FECHA_OBTENIDA['mes_dos']))
            _año = int(FECHA_OBTENIDA['año'])

            FECHA_INICIO_OBTENIDA = date(_año, _mes_uno, _dia_uno) 
            FECHA_FIN_OBTENIDA = date(_año, _mes_dos, _dia_dos) 

            if FECHA_INICIO_OBTENIDA < FECHA_FIN_OBTENIDA:
                RANGO_DE_FECHAS = [FECHA_INICIO_OBTENIDA + timedelta(days=i) 
                    for i in range((FECHA_FIN_OBTENIDA - FECHA_INICIO_OBTENIDA).days + 1)]
                
            else:
                print("Algo ocurrio al momento de obtener las fechas, la {FECHA_INICIO_OBTENIDA}")
                print(f"con un valor de: -> {FECHA_INICIO_OBTENIDA}")
                print("deberia de ser menor a {FECHA_FIN_OBTENIDA}")
                print(f"que tiene valor de: -> {FECHA_FIN_OBTENIDA}")
                break
        else:
            print("No huvo informacion para validar {FECHA_INICIO_OBTENIDA} y {FECHA_FIN_OBTENIDA}.")
            print("El programa finalizará.")

    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al crear el rango de fechas entre {FECHA_INICIO_OBTENIDA} y {FECHA_FIN_OBTENIDA}.")
        print(e)
        sys.exit(1)
    finally:
        #Agregar Log.info
        print("-> FIN: Termino la creacion del rango de fechas entre {FECHA_INICIO_OBTENIDA} y {FECHA_FIN_OBTENIDA}\n")
    # -------------------------------------------------------------


    # Crea el diccionario final con todos los datos obtenidos del pdf. 
    try:
        LISTA_DATOS_COMPLETOS = [] 
        #Agregar Log.info
        if DICCIONARIO_DATOS:
            for fecha_en_curso in RANGO_DE_FECHAS:
                fecha = str(fecha_en_curso)
                for dicc_datos in DICCIONARIO_DATOS:
                    LISTA_DATOS_COMPLETOS.append({
                        "Fecha": fecha,
                        "Tad": dicc_datos['tad'],
                        "TadNombre": dicc_datos['tad_nombre'],
                        "PrecioMagna": dicc_datos['precio_magna'],
                        "PrecioPremium": dicc_datos['precio_premium'],
                        "PrecioDiesel": dicc_datos['precio_diesel']
                    })
        else:
            print("La lista de datos {LISTA_DATOS_COMPLETOS} esta vacia.")
            print(f"CONTENIDO DE LA LISTA:\n{LISTA_DATOS_COMPLETOS}")
    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al crear el diccionario final con todos los datos.")
        print(e)
        sys.exit(1)
    finally:
        #Agregar Log.info
        pass
        print("-> FIN: Termino la creacion del diccionario final con todos los datos.\n")
    # -------------------------------------------------------------


    # Inserta la informacion extraida del pdf en una tabla. 
    try:
        # Agregar Log.info
        existentes = set(zip(FECHAS_REGISTRADAS['Fecha'].astype(str),
                             FECHAS_REGISTRADAS['Tad'].astype(str)))
        
        insert_text = text("""
            INSERT INTO [Sinergia_Aux].[dbo].[PreciosPemex_New]
                (Fecha, Tad, TadNombre, PrecioMagna, PrecioPremium, PrecioDiesel)
            VALUES (:fecha, :tad, :tad_nombre, :magna, :premium, :diesel);
                """)
        with engine.begin() as conn:
            print("Insertando los datos:")
            for registro in LISTA_DATOS_COMPLETOS:
                clave = (str(registro['Fecha']), str(registro['Tad']))

                if clave in existentes:
                    print(f"Ya fue registrada la clave: {clave}")
                    continue

                FECHA = registro['Fecha']
                TAD = registro['Tad']
                TAD_NOMBRE = registro['TadNombre']
                PRECIO_MAGNA = registro['PrecioMagna']
                PRECIO_PREMIUM = registro['PrecioPremium']
                PRECIO_DIESEL = registro['PrecioDiesel']

                print(TAD, TAD_NOMBRE, PRECIO_MAGNA, PRECIO_PREMIUM, PRECIO_DIESEL)
                print("----------")

                conn.execute(
                    insert_text, 
                    {
                        "fecha": FECHA,
                        "tad": int(TAD),
                        "tad_nombre": TAD_NOMBRE,
                        "magna": PRECIO_MAGNA,
                        "premium": None if PRECIO_PREMIUM in (None, "None", "") else PRECIO_PREMIUM,
                        "diesel": PRECIO_DIESEL,
                    },
                )
        print("-> FIN: Inserción de precios.\n")
    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al insertar la informacion en la tabla.")
        print(e)
    finally:
        print("-> FIN: Insertar datos en la tabla.\n")
    # -------------------------------------------------------------

    # Renombrar el documento. 
    ARCHIVO_RENOMBRADO = False
    try:
        #Agregar Log.info
        NOMBRE_BASE = f"Precios del {FECHA_INICIO_OBTENIDA} al {FECHA_FIN_OBTENIDA}{archivo.suffix}"
        NUEVO_NOMBRE = archivo.with_name(NOMBRE_BASE)
        archivo.rename(NUEVO_NOMBRE)
        ARCHIVO_RENOMBRADO = True

    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al renombrar el archivo.")
        print(e)
    finally:
        #Agregar Log.info
        print("-> FIN: Termino renombrar el archivo.\n")
    # -------------------------------------------------------------

    from datetime import datetime
    # Registrar archivo a los clientes.
    try:
        #Agregar Log.info
        INSERT_CLIENTES_EJECUTADO = False

        if ARCHIVO_RENOMBRADO:
            insert_clientes = text("""
                INSERT INTO [NexusFuel].[CardSystem].[ArchivosGenerales] 
                    (Nombre, nombreArchivo, Destino, Tipo, FechaInicio, FechaFin, FechaCreacion)
                VALUES (:nombre, :nombre_archivo, :destino, :tipo, :fecha_inicio, :fecha_fin, :fecha_creacion);
                    """)
            
            ahora = datetime.now()
            fecha_actual = ahora.strftime("%Y-%m-%d %H:%M:%S")
            fecha_final = (ahora + timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")
            print("Insertando registros...")
            with engine.begin() as conn:
                for cliente in CLIENTES_ACTIVOS.itertuples():
                    NOMBRE_ARCHIVO = str(NUEVO_NOMBRE.name)
                    CLIENTE_ACTUAL =  int(cliente[1])
                    print(NOMBRE_ARCHIVO, CLIENTE_ACTUAL, fecha_actual, fecha_final)
                    print("----------")
                    
                    conn.execute(
                        insert_clientes, 
                        {
                            "nombre": "Precios de combustible.",
                            "nombre_archivo": NOMBRE_ARCHIVO,
                            "destino": CLIENTE_ACTUAL,
                            "tipo": 1,
                            "fecha_inicio": fecha_actual,
                            "fecha_fin": fecha_final,
                            "fecha_creacion": fecha_actual,
                        },
                    )

            INSERT_CLIENTES_EJECUTADO = True
            print("Registros insertados.\n")
        else:
            print(f"No se renombro el archivo, no hay informacion para subir.")
    except Exception as e:
        # Agregar Log.Error
        print("Hubo un error al insertar la informacion documentos clientes.\n")
        print(e)
    finally:
        #Agregar Log.info
        print("-> FIN: Inserción de la informacion documentos clientes.\n")
    # -------------------------------------------------------------


    from servicio_sftp import ftp_send_file, ftp_unlink
    ARCHIVO_ENVIADO = False
    if INSERT_CLIENTES_EJECUTADO:
    # Envia el documento al servidor 50 por ftp
        try:
            #Agregar Log.info
            ftp_send_file(HOST, PORT, USER, PSW, NUEVO_NOMBRE)
            ARCHIVO_ENVIADO = True
        except Exception as e:
            # Agregar Log.Error
            print("Ocurrio un error al enviar el documento al servidor.")
            print(e)
        finally:
            #Agregar Log.info
            print("-> FIN: Termino de enviar el archivo al servidor.\n")
        # -------------------------------------------------------------
    else:
        print("No se ejecuto la insercion de clientes, no se enviará el archivo al servidor.")

    if ARCHIVO_ENVIADO:
    # Elimina el documento local
        try:
            #Agregar Log.info
            ftp_unlink(NUEVO_NOMBRE)
        except Exception as e:
            # Agregar Log.Error
            print("Ocurrio un error al eliminar el archivo")
            print(e)
        finally:
            #Agregar Log.info
            print("-> FIN: Se elimino el archivo local. ")
        # -------------------------------------------------------------
    else:
        print("No se envio el archivo al servidor. No se borrara el archivo.")
        
print("-> Fin de la ejecucion del programa. <-".upper())