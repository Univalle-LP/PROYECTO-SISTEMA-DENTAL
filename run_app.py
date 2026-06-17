import os, sys, threading, webbrowser, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Cambia "mi_proyecto" por el nombre de tu carpeta de settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def abrir_navegador():
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    threading.Thread(target=abrir_navegador).start()
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '--noreload'])