from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from porfolio.views import ProjectListView

from .views import (
    AboutView,
    ContactView,
    HomeView,
    PerfilView,
    ResumeView,
    set_language,
)

urlpatterns = [
    path("config/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("perfil/", PerfilView.as_view(), name="profile"),
    path("resume/", ResumeView.as_view(), name="resume"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("set-language/<str:language_code>/", set_language, name="set_language"),
    path("proyectos/", ProjectListView.as_view(), name="projects"),
    path("certificaciones/", include("certificado.urls")),
    path("api/", include("Portafolio.api_urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
