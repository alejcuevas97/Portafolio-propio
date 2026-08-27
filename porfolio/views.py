from django.views.generic import ListView

from .models import Project
from .services import ProjectService


class ProjectListView(ListView):
    """Lista paginada de proyectos del portafolio."""

    model = Project
    template_name = "proyectos.html"
    context_object_name = "proyectos"
    paginate_by = 12

    def get_queryset(self):
        return ProjectService.get_all_projects()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_projects"] = ProjectService.get_project_count()
        return context
