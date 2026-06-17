@echo off

echo Creando entorno virtual...

python -m venv venv

call venv\Scripts\activate

pip install --upgrade pip

pip install -r requirements.txt

pause