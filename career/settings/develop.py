from .base import *

DEBUG = True
FILE_UPLOAD_PERMISSIONS = 0o644

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AWS_SES_ACCESS_KEY_ID = 'your access key'
AWS_SES_SECRET_ACCESS_KEY = 'your secret key'