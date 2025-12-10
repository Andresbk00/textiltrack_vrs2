from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario
import re

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rol', 'password']

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("La contraseña debe incluir una mayúscula.")

        if not re.search(r"[0-9]", password):
            raise ValidationError("La contraseña debe incluir un número.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("La contraseña debe incluir un carácter especial.")

        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].split('@')[0]
        user.is_active = False
        user.email_verificado = False
        user.aprobado = False
        user.estado = 'pendiente'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# usuarios/forms.py
from django import forms
from .models import Usuario

class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto_perfil']  # Solo la foto
