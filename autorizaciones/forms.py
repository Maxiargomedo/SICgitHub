from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Persona

class RegistroForm(UserCreationForm):
    nombre_completo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Juan Pérez López'})  # <-- Aquí faltaba coma
    )
    rut = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 12.345.678-9'})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+56 9 8765 4321'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'tu.correo@empresa.com'})
    )

    class Meta:
        model = Usuario
        fields = ('email', 'nombre_completo', 'rut', 'telefono', 'password1', 'password2')

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if Usuario.objects.filter(persona__rut=rut).exists():
            raise forms.ValidationError("Este RUT ya está registrado")
        return rut

    def save(self, commit=True):
        usuario = super().save(commit=False)
        
        persona = Persona.objects.create(
            nombre_completo=self.cleaned_data['nombre_completo'],
            rut=self.cleaned_data['rut'],
            telefono=self.cleaned_data['telefono']
        )
        
        usuario.persona = persona
        
        if commit:
            usuario.save()
            self.save_m2m()  # Solo necesario si usas ManyToMany fields
        
        return usuario