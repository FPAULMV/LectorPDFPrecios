from ftplib import FTP
from pathlib import Path

def ftp_send_file(host: str, port: int, user: str, psw: str, local_file: Path) -> None:
    
    if local_file.exists():
        with FTP() as ftp:
            print(f"Enviando documento: {local_file.name}")
            ftp.connect(host, port, timeout=10)
            ftp.login(user, psw)

            # Subir el archivo.
            with open(local_file, "rb") as f:
                ftp.storbinary(f"STOR {local_file.name}", f)
    else: 
        print(f"No se encontro la ruta al archivo: {local_file}")
        

def ftp_unlink(local_file: Path) -> None:
    local_file.unlink(missing_ok = False)
