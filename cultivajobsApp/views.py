from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from cultivajobsApp.models import Estudiante, Empleador, Oferta
from cultivajobsApp.forms import Estudianteregistroform, Empleadorregistroform, OfertaForm, EstudiantePerfilForm
import random
from django.core.exceptions import ValidationError

def generate_verification_code():
    """Genera un código de verificación de 6 dígitos."""
    return str(random.randint(100000, 999999))

def home(request):
    return render(request, 'cultivajobsApp/home.html')

def sobreNosotros(request):
    return render(request, 'cultivajobsApp/sobrenosotros.html')

def custom_login(request):
    """Vista personalizada de inicio de sesión."""
    if request.method == 'POST':
        username = request.POST['username'].lower()  # Convertir el email ingresado a minúsculas
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirige al dashboard después del login
        else:
            messages.error(request, "Credenciales incorrectas. Por favor, inténtalo de nuevo.")
    return render(request, 'registration/login.html')


def registrarestudiante(request):
    form = Estudianteregistroform()
    if request.method == 'POST':
        form = Estudianteregistroform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            if Estudiante.objects.filter(email=email).exists():
                form.add_error('email', "Este correo electrónico ya está registrado como estudiante.")
                return render(request, 'cultivajobsApp/registroestudiante.html', {'form': form})
            if Empleador.objects.filter(email=email).exists():
                form.add_error('email', "Este correo electrónico ya está registrado como empleador.")
                return render(request, 'cultivajobsApp/registroestudiante.html', {'form': form})

            # Verificación de la confirmación de contraseña
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data.get('confirm_password')
            if password != confirm_password:
                form.add_error('confirm_password', "Las contraseñas no coinciden.")
                return render(request, 'cultivajobsApp/registroestudiante.html', {'form': form})

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            verification_code = generate_verification_code()
            estudiante = Estudiante(
                user=user,
                email=email,
                password=make_password(password),
                verification_code=verification_code
            )
            estudiante.is_active = False  # Inactivo hasta verificación
            estudiante.save()
            
            # Mensaje amigable y detallado
            message = (
                f"Hola {email.split('@')[0]},\n\n"
                "¡Bienvenido a Cultivajobs! Estamos muy contentos de que te hayas unido a nuestra plataforma "
                "y estés listo para comenzar a explorar las oportunidades que ofrecemos.\n\n"
                "Para completar tu registro, por favor utiliza el siguiente código de verificación en nuestra página:\n\n"
                f"Tu código de verificación es: {verification_code}\n\n"
                "Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.\n\n"
                "Saludos cordiales,\n"
                "El equipo de Cultivajobs"
            )
            
            send_mail(
                subject="Verificación de tu cuenta en Cultivajobs",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            request.session['email_pendiente'] = email
            return redirect('verificacion_email')
    return render(request, 'cultivajobsApp/registroestudiante.html', {'form': form})
def registrarempleador(request):
    form = Empleadorregistroform()
    if request.method == 'POST':
        form = Empleadorregistroform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            if Estudiante.objects.filter(email=email).exists():
                form.add_error('email', "Este correo electrónico ya está registrado como estudiante.")
                return render(request, 'cultivajobsApp/registroempleador.html', {'form': form})
            if Empleador.objects.filter(email=email).exists():
                form.add_error('email', "Este correo electrónico ya está registrado como empleador.")
                return render(request, 'cultivajobsApp/registroempleador.html', {'form': form})

            # Verificación de la confirmación de contraseña
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data.get('confirm_password')
            if password != confirm_password:
                form.add_error('confirm_password', "Las contraseñas no coinciden.")
                return render(request, 'cultivajobsApp/registroempleador.html', {'form': form})

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            verification_code = generate_verification_code()
            empleador = Empleador(
                user=user,
                email=email,
                password=make_password(password),
                verification_code=verification_code
            )
            empleador.is_active = False  # Inactivo hasta verificación
            empleador.save()

            # Mensaje amigable y detallado
            message = (
                f"Hola {email.split('@')[0]},\n\n"
                "¡Gracias por registrarte en Cultivajobs como empleador! Valoramos tu interés y estamos aquí para ayudarte "
                "a conectar con el talento que estás buscando.\n\n"
                "Para completar tu registro, por favor utiliza el siguiente código de verificación en nuestra página:\n\n"
                f"Tu código de verificación es: {verification_code}\n\n"
                "Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.\n\n"
                "Saludos cordiales,\n"
                "El equipo de Cultivajobs"
            )

            send_mail(
                subject="Verificación de tu cuenta en Cultivajobs",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            request.session['email_pendiente'] = email
            return redirect('verificacion_email')
    return render(request, 'cultivajobsApp/registroempleador.html', {'form': form})


def verificar_codigo(request):
    """Vista para verificar el código de verificación de email."""
    if request.method == 'POST':
        codigo_ingresado = request.POST['codigo_verificacion']
        email = request.session.get('email_pendiente')
        try:
            usuario = Estudiante.objects.get(email=email) if Estudiante.objects.filter(email=email).exists() else Empleador.objects.get(email=email)
        except (Estudiante.DoesNotExist, Empleador.DoesNotExist):
            messages.error(request, "No se encontró el usuario. Inténtalo de nuevo.")
            return redirect('custom_login')

        if usuario.verification_code == codigo_ingresado:
            usuario.is_active = True  # Activa el usuario si el código es correcto
            usuario.verification_code = ""  # Limpia el código después de la verificación
            usuario.save()
            messages.success(request, "Cuenta verificada con éxito. Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Código incorrecto. Inténtalo de nuevo.")
    return render(request, 'registration/verificar_codigo.html')

def registro_exitoso(request):
    return render(request, 'cultivajobsApp/registro_exitoso.html')

@login_required
def dashboard(request):
    if hasattr(request.user, 'estudiante'):
        return redirect('menu_estudiante')
    elif hasattr(request.user, 'empleador'):
        return redirect('menu_empleador')
    else:
        messages.error(request, "No tienes un perfil asociado para acceder a esta sección.")
        return redirect('login')


@login_required
def menu_empleador(request):
    # Obtiene al empleador autenticado
    empleador = request.user.empleador
    
    # Obtener las ofertas que ha creado este empleador
    ofertas = empleador.ofertas.all()

    return render(request, 'menu/empleador.html', {'ofertas': ofertas})

@login_required
def menu_ofertas(request):
    form = OfertaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # Guardar la oferta sin confirmar el empleador aún
        oferta = form.save(commit=False)
        
        # Asociar el empleador autenticado con la oferta
        oferta.save()  # Guardamos la oferta primero
        oferta.empleadores.add(request.user.empleador)  # Asocia al empleador autenticado
        oferta.save()

        messages.success(request, "Oferta creada exitosamente.")
        return redirect('menu_empleador')
    
    return render(request, 'menu/ofertas.html', {'form': form})

def ver_ofertas(request):
    ofertas = Oferta.objects.all()
    return render(request, 'menu/verofertas.html', {'ofertas': ofertas})

@login_required
def postular_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)
    estudiante = request.user.estudiante

    # Verificar si el perfil del estudiante está completo
    if not estudiante.perfil_completo():
        messages.warning(request, "Debes completar tu perfil antes de poder postular a una oferta.")
        return redirect('perfil_estudiante')

    # Verificar si el estudiante ya ha postulado a esta oferta
    if estudiante.ofertas.filter(id=oferta_id).exists():
        messages.warning(request, "Ya has postulado a esta oferta.")
    else:
        # Guardar la postulación del estudiante
        estudiante.ofertas.add(oferta)

        # Mensaje de felicitación y detalles de postulación para el estudiante
        mensaje_estudiante = (
            f"¡Felicitaciones {estudiante.nombre}!\n\n"
            "Te has postulado exitosamente a la oferta de trabajo:\n\n"
            f"**{oferta.titulo}**\n\n"
            f"{oferta.descripcion}\n\n"
            "Nos alegra que estés aprovechando las oportunidades en CultivaJobs. "
            "Pronto, el empleador revisará tu perfil, y te notificaremos sobre cualquier actualización. "
            "Si necesitas asistencia o tienes alguna pregunta, no dudes en contactarnos.\n\n"
            "Atentamente,\n"
            "El equipo de CultivaJobs"
        )

        # Enviar correo al estudiante
        send_mail(
            subject="Postulación Exitosa en CultivaJobs",
            message=mensaje_estudiante,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[estudiante.email],
            fail_silently=False,
        )

        # Enviar un correo electrónico a cada empleador asociado con la oferta
        for empleador in oferta.empleadores.all():
            if empleador.email:
                print(f"Intentando enviar correo a empleador: {empleador.email}")  # Depuración

                mensaje_empleador = (
                    f"Estimado/a {empleador.user.username},\n\n"
                    f"Nos complace informarle que el estudiante {estudiante.nombre} "
                    f"se ha postulado a su oferta de trabajo: {oferta.titulo}.\n\n"
                    "Le invitamos a revisar el perfil del postulante en CultivaJobs. "
                    "Si considera que el candidato es adecuado, puede contactarlo para coordinar "
                    "una entrevista o enviar una respuesta a su postulación.\n\n"
                    "Gracias por confiar en CultivaJobs para encontrar el talento que necesita.\n\n"
                    "Atentamente,\n"
                    "El equipo de CultivaJobs"
                )

                send_mail(
                    subject="Nueva Postulación Recibida en CultivaJobs",
                    message=mensaje_empleador,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[empleador.email],
                    fail_silently=False,
                )

        messages.success(request, f"Te has postulado exitosamente a la oferta: {oferta.titulo}.")

    # Renderizar la página de confirmación de postulación
    return render(request, 'menu/postulacion.html', {'oferta': oferta, 'estudiante': estudiante})



@login_required
def actualizar_perfil_estudiante(request):
    estudiante = request.user.estudiante
    if request.method == 'POST':
        form = EstudiantePerfilForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado con éxito.")
            return redirect('menu_estudiante')
    else:
        form = EstudiantePerfilForm(instance=estudiante)

    return render(request, 'menu/perfil_estudiante.html', {'form': form})



@login_required
def menu_estudiante(request):
    estudiante = request.user.estudiante

    # Verificar si el perfil está completo
    perfil_completo = all([
        estudiante.nombre,
        estudiante.descripcion,
        estudiante.habilidades,
    ])

    if not perfil_completo:
        messages.info(request, "Debes completar tu perfil antes de postular a ofertas.")
        return redirect('perfil_estudiante')

    # Obtener todas las ofertas y las ofertas a las que el estudiante ya está postulado
    ofertas = Oferta.objects.all()
    postulaciones = estudiante.ofertas.all()  # Ofertas a las que el estudiante ya ha postulado

    return render(request, 'menu/estudiante.html', {
        'ofertas': ofertas,
        'estudiante': estudiante,
        'postulaciones': postulaciones,
    })


@login_required
def cancelar_postulacion(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)
    estudiante = request.user.estudiante

    # Verificar si el estudiante ya está postulado a esta oferta
    if estudiante.ofertas.filter(id=oferta_id).exists():
        # Quitar la oferta de las postulaciones del estudiante
        estudiante.ofertas.remove(oferta)
        messages.success(request, f"Has cancelado tu postulación a la oferta: {oferta.titulo}.")
    else:
        messages.warning(request, "No estás postulado a esta oferta.")

    # Redirigir a la página de búsqueda para reflejar el estado actualizado
    return redirect('buscar_ofertas')



def buscar_ofertas(request):
    query = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()

    # Filtra las ofertas
    ofertas = Oferta.objects.all()
    if query:
        ofertas = ofertas.filter(titulo__icontains=query)
    if categoria:
        ofertas = ofertas.filter(categoria=categoria)

    # Obtener el estudiante autenticado y sus postulaciones
    estudiante = request.user.estudiante
    postulaciones = estudiante.ofertas.all()  # Ofertas a las que el estudiante ya está postulado

    # Depuración
    print("Query:", query)
    print("Categoría seleccionada:", categoria)
    print("Ofertas encontradas:", list(ofertas))

    return render(request, 'menu/estudiante.html', {
        'ofertas': ofertas,
        'postulaciones': postulaciones,  # Pasamos las postulaciones a la plantilla
        'query': query,
        'categoria': categoria
    })


@login_required
def ver_candidatos(request, oferta_id):
    # Obtener la oferta usando el id
    oferta = get_object_or_404(Oferta, id=oferta_id)
    
    # Obtener los estudiantes postulados
    estudiantes_postulados = oferta.postulantes.all()

    return render(request, 'menu/vercandidatos.html', {
        'oferta': oferta,
        'estudiantes_postulados': estudiantes_postulados
    })
