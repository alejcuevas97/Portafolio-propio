"""Read-only public API for portfolio content."""

from rest_framework import viewsets

from certificado.models import Certification
from porfolio.models import Project

from .serializers import CertificationSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by("-created")
    serializer_class = ProjectSerializer


class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificationSerializer

    def get_queryset(self):
        return Certification.objects.filter(active=True).order_by(
            "-issued_date", "order"
        )
