from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission
)
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validar_rut(value):
    if not value.replace('.', '').replace('-', '').isdigit():
        raise ValidationError('RUT inválido. Solo debe contener números, puntos y guión')

class Persona(models.Model):
    nombre_completo = models.CharField("Nombre Completo", max_length=100)
    rut = models.CharField(
        "RUT",
        max_length=12,
        unique=True,
        validators=[validar_rut],
        error_messages={
            'unique': 'Este RUT ya está registrado en el sistema'
        }
    )
    fecha_nacimiento = models.DateField("Fecha de Nacimiento", null=True, blank=True)
    telefono = models.CharField("Teléfono", max_length=20, blank=True)
    
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        indexes = [
            models.Index(fields=['rut'], name='rut_idx')
        ]

    def __str__(self):
        return f"{self.nombre_completo} ({self.rut})"

class UsuarioManager(BaseUserManager):
    def _crear_persona(self, datos_persona):
        try:
            return Persona.objects.create(**datos_persona)
        except Exception as e:
            raise ValidationError(f"Error al crear persona: {str(e)}")

    def create_user(self, email, password=None, **extra_fields):
        try:
            validate_email(email)
            email = self.normalize_email(email)
            
            if Usuario.objects.filter(email=email).exists():
                raise ValidationError("Este correo ya está registrado")

            datos_persona = {
                'nombre_completo': extra_fields.pop('nombre_completo', 'Usuario Nuevo'),
                'rut': extra_fields.pop('rut', '00000000-0'),
                'telefono': extra_fields.pop('telefono', '')
            }
            
            persona = self._crear_persona(datos_persona)
            
            user = self.model(
                email=email,
                persona=persona,
                **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
            
        except Exception as e:
            if 'persona' in locals():
                persona.delete()
            raise

    def create_superuser(self, email, password=None, **extra_fields):
        required_fields = ['nombre_completo', 'rut']
        for field in required_fields:
            if field not in extra_fields:
                raise ValidationError(f"Campo requerido faltante: {field}")

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Correo Electrónico", unique=True)
    persona = models.OneToOneField(
        Persona,
        on_delete=models.PROTECT,
        related_name='usuario',
        verbose_name="Datos Personales"
    )
    is_active = models.BooleanField("Activo", default=True)
    is_staff = models.BooleanField("Acceso Admin", default=False)
    fecha_registro = models.DateTimeField("Fecha de Registro", auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        permissions = [
            ("puede_aprobar_solicitudes", "Puede aprobar solicitudes de compra")
        ]

    def __str__(self):
        return f"{self.persona.nombre_completo} <{self.email}>"

class Solicitud(models.Model):
    ESTADOS = (
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Rechazada', 'Rechazada')
    )

    MEDIDAS = (
        ('c/u' , 'c/u'),
        ('litros' , 'litros'),
        ('kilos' , 'kilos'),
        ('metro', 'metro '),
        ('cc' , 'cc')
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='solicitudes',
        verbose_name="Solicitante"
    )
    descripcion = models.TextField("Descripción")
    cantidad = models.IntegerField("Cantidad")
    unidad = models.CharField(
        "Medidas",
        max_length=20,
        choices=MEDIDAS,
        default='Pendiente'
    )
    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=ESTADOS,
        default='Pendiente'
    )
    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)
    fecha_requerida = models.DateField("Fecha requerida")
    rechazos = models.IntegerField("Rechazos", default=0)

    class Meta:
        verbose_name = "Solicitud de Compra"
        verbose_name_plural = "Solicitudes de Compras"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estado'], name='estado_idx'),
            models.Index(fields=['fecha_creacion'], name='fecha_creacion_idx')
        ]

    def __str__(self):
        return f"Solicitud #{self.id} - {self.usuario.email}"