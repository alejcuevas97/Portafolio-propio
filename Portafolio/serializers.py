from rest_framework import serializers

from certificado.models import Certification
from porfolio.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializa proyectos del portafolio."""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "title", "descriptions", "image", "link", "created", "update"]
        read_only_fields = ["id", "created", "update"]

    def get_image(self, obj):
        if not obj.image:
            return None
        try:
            return obj.image.url
        except Exception:
            return str(obj.image)


class CertificationSerializer(serializers.ModelSerializer):
    """Serializa certificaciones."""

    class Meta:
        model = Certification
        fields = [
            "id",
            "title",
            "issuer",
            "issued_date",
            "description",
            "credential_url",
            "order",
        ]
