SECRET_KEY = '7)@!n!$4v7r9!t-ul0r)rlyi%zhi!zbp%w06+4q!*e&4-f%80_'
DEBUG = True

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
