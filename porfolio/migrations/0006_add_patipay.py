from django.db import migrations


def create_patipay(apps, schema_editor):
    Project = apps.get_model('porfolio', 'Project')
    title = 'PatinPay – Plataforma de Gestión de Eventos Deportivos'
    link = 'https://patinpay-frontend.pages.dev'
    descriptions = (
        'Plataforma SaaS de gestión de eventos: entradas, tienda, rifas, transmisiones en vivo y control de acceso por QR.'
    )
    # Imagen: usar la URL pública de Cloudinary como fallback. Si la instalación tiene Cloudinary
    # configurado, la administración puede editarla para usar el public ID.
    image_value = 'https://res.cloudinary.com/dqijixzes/image/upload/v1787821130/dygiwu7rlpslc3p9da5r.jpg'

    # Evitar duplicados
    obj, created = Project.objects.get_or_create(
        title=title,
        defaults={
            'descriptions': descriptions,
            'image': image_value,
            'link': link,
        },
    )


def remove_patipay(apps, schema_editor):
    Project = apps.get_model('porfolio', 'Project')
    Project.objects.filter(title__icontains='PatinPay').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('porfolio', '0005_delete_foto_project_image'),
    ]

    operations = [
        migrations.RunPython(create_patipay, reverse_code=remove_patipay),
    ]
