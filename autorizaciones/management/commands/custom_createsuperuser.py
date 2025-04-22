from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from autorizaciones.models import Persona

class Command(BaseCommand):
    help = 'Crea superusuarios con validación de datos completa'
    
    def add_arguments(self, parser):
        parser.add_argument('--email', required=True, help='Correo electrónico institucional')
        parser.add_argument('--nombre_completo', required=True, help='Nombre completo del usuario')
        parser.add_argument('--rut', required=True, help='RUT con formato 12.345.678-9')
        parser.add_argument('--telefono', help='Teléfono de contacto', default='')

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            # Verificar existencia previa
            if User.objects.filter(email=options['email']).exists():
                raise ValueError(f"❌ El email {options['email']} ya está registrado")
                
            if Persona.objects.filter(rut=options['rut']).exists():
                raise ValueError(f"❌ El RUT {options['rut']} ya está en uso")
            
            # Crear usuario
            password = input("Ingrese la contraseña (mínimo 8 caracteres): ").strip()
            if len(password) < 8:
                raise ValueError("La contraseña debe tener al menos 8 caracteres")
            
            user = User.objects.create_superuser(
                email=options['email'],
                password=password,
                nombre_completo=options['nombre_completo'],
                rut=options['rut'],
                telefono=options['telefono']
            )
            
            # Mensaje de éxito
            self.stdout.write(self.style.SUCCESS("\n✅ Usuario creado exitosamente!"))
            self.stdout.write(self.style.SUCCESS(f"   Nombre: {user.persona.nombre_completo}"))
            self.stdout.write(self.style.SUCCESS(f"   Email: {user.email}"))
            self.stdout.write(self.style.SUCCESS(f"   RUT: {user.persona.rut}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Error: {str(e)}"))
            self.stdout.write(self.style.WARNING("🚨 Se realizó rollback de la transacción"))