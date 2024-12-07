from django import forms
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from .models import Estudiante, Empleador, Oferta

class Estudianteregistroform(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(10)]
    )
    confirm_password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        label="Confirmar Contraseña"
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Verifica si el correo ya está registrado en Estudiante o Empleador
        if Estudiante.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado como estudiante.")
        if Empleador.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado como empleador.")
        
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Las contraseñas no coinciden.")
        return cleaned_data


class Empleadorregistroform(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(10)]
    )
    confirm_password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput,
        label="Confirmar Contraseña"
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Verifica si el correo ya está registrado en Estudiante o Empleador
        if Estudiante.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado como estudiante.")
        if Empleador.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado como empleador.")
        
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Las contraseñas no coinciden.")
        return cleaned_data


class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['titulo', 'descripcion', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la oferta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la oferta'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class EstudiantePerfilForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'descripcion', 'habilidades', 'direccion', 'telefono']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'habilidades': forms.TextInput(attrs={'placeholder': 'Ejemplo: Python, Java, SQL'}),
        }