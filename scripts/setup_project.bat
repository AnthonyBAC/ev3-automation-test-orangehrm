@echo off
setlocal
pushd "%~dp0\.."

where python >nul 2>&1
if errorlevel 1 (
    echo No se encontro Python en PATH.
    echo Instala Python 3.10+ y vuelve a ejecutar este script.
    popd
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo No se pudo crear entorno virtual.
        popd
        exit /b 1
    )
)

echo Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo No se pudieron instalar dependencias.
    popd
    exit /b 1
)

echo.
echo Proyecto listo.
echo Siguiente paso: scripts\run_tests.bat

popd
exit /b 0
