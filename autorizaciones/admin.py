from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Persona, Solicitud


# Eliminar PersonaInline y crear UsuarioInline
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Credenciales de Usuario'
    fk_name = 'persona'  # Nombre del campo OneToOneField en Usuario

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    inlines = (UsuarioInline,)
    list_display = ('nombre_completo', 'rut', 'telefono')
    search_fields = ('nombre_completo', 'rut')

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'get_full_name', 'is_staff')
    search_fields = ('email', 'persona__nombre_completo')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'fecha_registro')}),
    )
    
    def get_full_name(self, obj):
        return obj.persona.nombre_completo
    get_full_name.short_description = 'Nombre Completo'

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descripcion', 'estado', 'fecha_creacion')
    search_fields = ('usuario__email', 'descripcion')
    list_filter = ('estado',)


