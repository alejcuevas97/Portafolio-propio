from django.conf import settings
from django.utils import translation
from django.views.generic import TemplateView
from django.shortcuts import render, redirect


# === Principio O (Open/Closed) ===
# Vista base genérica - extensible sin modificar
class BasePageView(TemplateView):
    """
    Vista base reutilizable para páginas estáticas.
    Cumple el principio Open/Closed: abierta para extensión, cerrada para modificación.
    """
    
    def get_context_data(self, **kwargs):
        """Método que puede ser extendido por subclases"""
        context = super().get_context_data(**kwargs)
        # Aquí puedes agregar lógica común a todas las páginas
        context['page_title'] = self.page_title if hasattr(self, 'page_title') else 'Página'
        return context


# === Principio S (Single Responsibility) ===
# Cada vista tiene una única responsabilidad: renderizar su página
class HomeView(BasePageView):
    """Vista para la página de inicio"""
    template_name = 'index.html'
    page_title = 'Inicio'


class AboutView(BasePageView):
    """Vista para la página de acerca de"""
    template_name = 'about.html'
    page_title = 'Acerca de'


class PerfilView(BasePageView):
    """Vista para el perfil del usuario"""
    template_name = 'perfil.html'
    page_title = 'Perfil'


class ResumeView(BasePageView):
    """Vista para el currículum"""
    template_name = 'resume.html'
    page_title = 'Currículum'


class ContactView(BasePageView):
    """Vista para contacto"""
    template_name = 'contact.html'
    page_title = 'Contacto'


def set_language(request, language_code):
    """Cambia el idioma activo y redirige a la página anterior."""
    supported_languages = dict(settings.LANGUAGES)
    if language_code not in supported_languages:
        language_code = settings.LANGUAGE_CODE

    response = redirect(request.GET.get('next') or request.META.get('HTTP_REFERER') or '/')
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
    translation.activate(language_code)
    return response
