import os

SECRET_KEY = '7)@!n!$4v7r9!t-ul0r)rlyi%zhi!zbp%w06+4q!*e&4-f%80_'
DEBUG = int(os.environ.get('DEBUG', default=0))
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
STATIC_URL = '/static/'

INSTALLED_APPS = (
    'iamusic',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True
    },
]

ROOT_URLCONF = 'iamusic.urls'
