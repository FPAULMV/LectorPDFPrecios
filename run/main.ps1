# Definir variables
        $VenvPath = "C:\Users\AdminTI\OneDrive - Sinergia\VirtualEnv\Scripts"
        $ScriptPath = "C:\Users\AdminTI\PaulMorales\Proyectos\LectorPDFPrecios\src\"
        $ScriptName = "main.py"

        # Activar el entorno virtual
        Set-Location -Path $VenvPath
        .\activate 
        Write-Output "----- ENTORNO VIRTUAL ACTIVADO -----"


        # Cambiar al directorio del script
        Set-Location -Path $ScriptPath

        # Ejecutar el script Python
        python.exe ".\$ScriptName"

        # Desactivar el entorno virtual
        deactivate
        Write-Output "----- ENTORNO VIRTUAL DESACTIVADO -----"
        Write-Output "Finalizado!"
        