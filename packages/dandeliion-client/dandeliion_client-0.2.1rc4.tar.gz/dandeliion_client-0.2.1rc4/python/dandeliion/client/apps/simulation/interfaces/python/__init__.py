import django
if not hasattr(django, 'apps'):
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dandeliion.client.settings')
    django.setup()
