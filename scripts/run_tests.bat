@echo off
setlocal
pushd "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
    echo No se encontro entorno virtual.
    echo Ejecuta primero: scripts\setup_project.bat
    popd
    exit /b 1
)

".venv\Scripts\python.exe" run_tests.py %*
set "EXIT_CODE=%ERRORLEVEL%"

if exist "reports\html\report.html" (
    start "" "reports\html\report.html"
)

popd
exit /b %EXIT_CODE%
