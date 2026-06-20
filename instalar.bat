@echo off
title Instalador del Proyecto Django

echo =====================================
echo   VERIFICANDO PYTHON 3.12
echo =====================================

py -3.12 --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python 3.12 no esta instalado.
    echo.
    echo Descargalo desde:
    echo https://www.python.org/downloads/release/python-3120/
    echo.
    pause
    exit /b
)

echo Python 3.12 encontrado.
echo.

echo =====================================
echo   CREANDO ENTORNO VIRTUAL
echo =====================================

py -3.12 -m venv venv

if errorlevel 1 (
    echo Error al crear el entorno virtual.
    pause
    exit /b
)

call venv\Scripts\activate.bat

echo.
echo =====================================
echo   ACTUALIZANDO PIP
echo =====================================

python -m pip install --upgrade pip

echo.
echo =====================================
echo   INSTALANDO DEPENDENCIAS
echo =====================================

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error instalando dependencias.
    pause
    exit /b
)

echo.
echo =====================================
echo   INSTALACION COMPLETADA
echo =====================================
echo.

python --version

pause
