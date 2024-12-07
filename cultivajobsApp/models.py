from django.db import models
from django.contrib.auth.models import User

class Empleador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con User
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=6, blank=True, null=True)  # Código de verificación
    is_active = models.BooleanField(default=False)  # Estado de activación de la cuenta

class Oferta(models.Model):
    CATEGORIA_OPCIONES = [
        ('CR', 'Comida Rápida'),
        ('RT', 'Retail'),
        ('SP', 'Supermercado'),
        ('LM', 'Logística y Mensajería'),
        ('AT', 'Atención al Cliente'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=2, choices=CATEGORIA_OPCIONES, default='CR')
    empleadores = models.ManyToManyField('Empleador', blank=True, related_name='ofertas')

    def __str__(self):
        return self.titulo


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    ofertas = models.ManyToManyField(Oferta, blank=True, related_name='postulantes')
    
    # Campos adicionales del perfil
    nombre = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    habilidades = models.TextField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)  # Nuevo campo
    telefono = models.CharField(max_length=20, blank=True)    # Nuevo campo

    def __str__(self):
        return self.user.username

    def perfil_completo(self):
        # Verificar si todos los campos obligatorios están llenos
        return bool(self.nombre and self.descripcion and self.habilidades and self.direccion and self.telefono)



