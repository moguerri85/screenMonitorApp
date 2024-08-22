from cx_Freeze import setup, Executable

executables = [Executable("ScreenMonitorApp\\ScreenMonitorApp.py", base="Win32GUI")]

# Configurazione dell'installazione
setup(
    name="ScreenMonitorApp",
    version="1.0",
    description="Screen Monitor App, monitoraggio dello schermo e condivisione di zoom automatizzato",
    executables=executables,
)
