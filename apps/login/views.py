from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from datetime import datetime, timedelta

from .models import Usuario
from .models import Usuario, LogLogin
# =====================================================
# CONTROL SIMPLE DE INTENTOS (ANTI BRUTE FORCE)
# =====================================================

LOGIN_ATTEMPTS = {}

MAX_ATTEMPTS = 5

BLOCK_TIME = 300  # 5 minutos
def registrar_log(usuario, exitoso):
    
    LogLogin.objects.create(
        usuario=usuario,
        exitoso=exitoso
    )

def is_blocked(ip):

    if ip in LOGIN_ATTEMPTS:

        data = LOGIN_ATTEMPTS[ip]

        if data["attempts"] >= MAX_ATTEMPTS:

            if datetime.now() < data["block_until"]:

                return True

            else:

                LOGIN_ATTEMPTS.pop(ip)

    return False


def register_attempt(ip):

    if ip not in LOGIN_ATTEMPTS:

        LOGIN_ATTEMPTS[ip] = {
            "attempts": 1,
            "block_until": datetime.now()
        }

    else:

        LOGIN_ATTEMPTS[ip]["attempts"] += 1

        if LOGIN_ATTEMPTS[ip]["attempts"] >= MAX_ATTEMPTS:

            LOGIN_ATTEMPTS[ip]["block_until"] = datetime.now() + timedelta(seconds=BLOCK_TIME)


# =====================================================
# LOGIN
# =====================================================

@csrf_protect
def login_view(request):

    if request.session.get('id_usuario'):
        return redirect('/dashboard/')

    if request.method == 'POST':

        username = escape(request.POST.get('username', '').strip())
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "Completa todos los campos")
            return render(request, 'login/login.html')

        try:

            usuario = Usuario.objects.get(username=username)

            if not usuario.activo:

                registrar_log(username, False)

                messages.error(request, "Usuario inhabilitado")
                return render(request, 'login/login.html')

            if check_password(password, usuario.password):

                # 🔐 LOG EXITOSO
                registrar_log(username, True)

                request.session.flush()

                request.session['id_usuario'] = usuario.id_usuario
                request.session['nombre'] = usuario.nombre
                request.session['username'] = usuario.username

                request.session.set_expiry(3600)

                return redirect('/dashboard/')

            else:

                # ❌ LOG FALLIDO
                registrar_log(username, False)

                messages.error(request, "Credenciales incorrectas")

        except Usuario.DoesNotExist:

            # ❌ LOG FALLIDO
            registrar_log(username, False)

            messages.error(request, "Credenciales incorrectas")

    return render(request, 'login/login.html')

def logout_view(request):
    
    # limpia TODO
    request.session.flush()

    return redirect('/')