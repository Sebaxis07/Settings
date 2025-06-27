from django import forms
from .models import Libro
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'autor': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título del Libro',
            'autor': 'Nombre del Autor',
            'imagen': 'Portada del Libro (Opcional)',
        }
class CustomUserCreationForm(UserCreationForm):
    """
    Un formulario que crea un usuario, con todos los campos necesarios.
    Hereda de UserCreationForm para manejar la contraseña de forma segura.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):
    """
    Un formulario para actualizar la información de un usuario,
    excluyendo la contraseña.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que los campos de tipo checkbox se vean mejor
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_staff'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_superuser'].widget.attrs.update({'class': 'form-check-input'})
        
        # Para el resto de campos
        text_fields = ['username', 'first_name', 'last_name']
        for field_name in text_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
