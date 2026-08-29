from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField

# === Principio S (Single Responsibility) ===
# Validadores separados
class ProjectValidator:
    """Encargado únicamente de validar proyectos"""
    
    @staticmethod
    def validate_title(title):
        """Valida que el título no esté vacío"""
        if not title or len(title.strip()) == 0:
            raise ValueError(_("El título del proyecto no puede estar vacío"))
        return True
    
    @staticmethod
    def validate_link(link):
        """Valida la URL"""
        validator = URLValidator()
        try:
            validator(link)
            return True
        except Exception as e:
            raise ValueError(f"URL inválida: {e}")


# === Principio S (Single Responsibility) ===
class Project(models.Model):
    """Modelo para representar un proyecto del portafolio"""
    
    title = models.CharField(
        max_length=150,
        verbose_name=_('Título'),
        help_text=_('Título del proyecto')
    )
    descriptions = models.TextField(
        verbose_name=_('Descripción'),
        help_text=_('Descripción detallada del proyecto')
    )
    image = CloudinaryField(
        verbose_name=_('Imagen'),
        help_text=_('Imagen de portada del proyecto')
    )
    link = models.URLField(
        max_length=150,
        verbose_name=_('Enlace'),
        help_text=_('URL del proyecto o demostración')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Fecha de creación')
    )
    update = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Fecha de actualización')
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Proyecto')
        verbose_name_plural = _('Proyectos')
        ordering = ['-created']
    
    # === Principio S: Métodos específicos del modelo ===
    def get_absolute_url(self):
        """Retorna la URL absoluta del proyecto"""
        # Modificar según tu estructura de URLs
        return f"/proyecto/{self.pk}/"
    
    def is_recent(self, days=30):
        """Verifica si el proyecto fue creado recientemente"""
        from django.utils.timezone import now
        from datetime import timedelta
        return self.created >= now() - timedelta(days=days)
    
    @property
    def image_url(self):
        """Retorna una URL segura para la imagen (evita levantar excepción si Cloudinary no está configurado)."""
        if not self.image:
            return ""
        try:
            return self.image.url
        except Exception:
            return str(self.image)
    
    def save(self, *args, **kwargs):
        """Valida antes de guardar"""
        ProjectValidator.validate_title(self.title)
        ProjectValidator.validate_link(self.link)
        super().save(*args, **kwargs)
