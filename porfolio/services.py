"""
=== PRINCIPIO D: DEPENDENCY INVERSION ===

Este módulo encapsula la lógica de negocios separada del acceso a datos.
Las vistas dependen de este servicio, no directamente de los modelos.
"""

from django.db.models import QuerySet
from django.core.cache import cache
from .models import Project


class ProjectService:
    """
    Servicio de proyectos - encapsular lógica de negocio.
    
    Beneficios SOLID:
    - Single Responsibility: Solo responsable de la lógica de proyectos
    - Dependency Inversion: Las vistas usan este servicio, no acceden directamente a BD
    - Open/Closed: Fácil de extender sin modificar vistas existentes
    """
    
    CACHE_KEY = 'projects_all'
    CACHE_TIMEOUT = 3600  # 1 hora
    
    @staticmethod
    def get_all_projects() -> QuerySet:
        """
        Obtiene todos los proyectos ordenados por fecha de creación.
        """
        return Project.objects.all().order_by('-created')
    
    @staticmethod
    def get_project_count() -> int:
        """Retorna el número total de proyectos."""
        return Project.objects.count()
    
    @staticmethod
    def search_projects(query: str) -> QuerySet:
        """
        Busca proyectos por título o descripción.
        """
        from django.db.models import Q

        return Project.objects.filter(
            Q(title__icontains=query) | Q(descriptions__icontains=query)
        ).order_by('-created')
    
    @staticmethod
    def get_cached_projects():
        """
        Obtiene proyectos desde caché en forma serializable (lista de dicts).
        Evita almacenar instancias de modelos Django en el cache (pickling).
        """
        projects = cache.get(ProjectService.CACHE_KEY)
        if projects is None:
            qs = ProjectService.get_all_projects()
            # Serializar solo los campos necesarios para mostrar en la UI/API
            projects = [
                {
                    "id": p.id,
                    "title": p.title,
                    "descriptions": p.descriptions,
                    "image": getattr(p, 'image_url', str(p.image) if p.image else ""),
                    "link": p.link,
                    "created": p.created,
                    "update": p.update,
                }
                for p in qs
            ]
            cache.set(ProjectService.CACHE_KEY, projects, ProjectService.CACHE_TIMEOUT)
        return projects
    
    @staticmethod
    def invalidate_cache():
        """Invalida el caché de proyectos."""
        cache.delete(ProjectService.CACHE_KEY)
    
    @staticmethod
    def get_projects_by_year(year: int) -> QuerySet:
        """
        Obtiene proyectos creados en un año específico.
        """
        return Project.objects.filter(created__year=year).order_by('-created')
    
    @staticmethod
    def create_project(title: str, descriptions: str, image, link: str) -> Project:
        """
        Crea un nuevo proyecto.
        """
        from .models import ProjectValidator

        ProjectValidator.validate_title(title)
        ProjectValidator.validate_link(link)

        project = Project.objects.create(
            title=title,
            descriptions=descriptions,
            image=image,
            link=link
        )
        ProjectService.invalidate_cache()
        return project
    
    @staticmethod
    def update_project(project_id: int, **kwargs) -> Project:
        """
        Actualiza un proyecto existente.
        """
        project = Project.objects.get(id=project_id)

        if 'title' in kwargs:
            from .models import ProjectValidator
            ProjectValidator.validate_title(kwargs['title'])

        if 'link' in kwargs:
            from .models import ProjectValidator
            ProjectValidator.validate_link(kwargs['link'])

        for key, value in kwargs.items():
            setattr(project, key, value)
        project.save()
        ProjectService.invalidate_cache()
        return project
    
    @staticmethod
    def delete_project(project_id: int) -> bool:
        """
        Elimina un proyecto de la base de datos.
        """
        deleted, _ = Project.objects.filter(id=project_id).delete()
        if deleted:
            ProjectService.invalidate_cache()
        return deleted > 0
