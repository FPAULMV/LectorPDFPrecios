from servicios_pdf import PdfManejador
from models import ArchivosManejador



if __name__ == '__main__':
    archivos = ArchivosManejador()
    archivos_filtrados = archivos.archivos_filtrados
    input(archivos_filtrados)

    for ruta_archivo in archivos_filtrados:
        pdf = PdfManejador(ruta_archivo)
        texto_pdf = pdf.obtener_texto()
        input(texto_pdf)