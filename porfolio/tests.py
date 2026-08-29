from django.test import TestCase, override_settings
from django.urls import reverse
from porfolio.models import Project


class ProjectsViewTests(TestCase):

    def setUp(self):
        # Crear proyectos de prueba con image como URL (simula public id o URL)
        Project.objects.create(
            title='Test Project 1',
            descriptions='Descripción de prueba 1',
            image='https://res.cloudinary.com/dqijixzes/image/upload/sample.jpg',
            link='https://example.com/1',
        )

    def test_projects_page_renders_without_cloudinary(self):
        """La vista /proyectos/ debe renderizar incluso si Cloudinary no está configurado."""
        # Forzar settings que indiquen que Cloudinary no está configurado
        with override_settings(CLOUDINARY_CLOUD_NAME='', CLOUDINARY_API_KEY='', CLOUDINARY_API_SECRET=''):
            url = reverse('projects')
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
            # Debe contener el título de la página
            self.assertContains(resp, 'Proyectos')
            # La imagen debe aparecer en el HTML (usamos la URL directa en el campo image)
            self.assertContains(resp, 'res.cloudinary.com')
