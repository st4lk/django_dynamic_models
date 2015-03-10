from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

AUTO_MODEL_YAML_FILE = os.path.join(BASE_DIR, 'tests', 'models_test.yaml')
