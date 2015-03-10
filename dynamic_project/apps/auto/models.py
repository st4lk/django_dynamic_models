# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.base import ModelBase
from django.conf import settings
import yaml

created_models = {}

FIELD_MAP = {
    'int': models.IntegerField,
    'char': models.CharField,
    'date': models.DateField,
}


def create_dynamic_models(models_data):
    created_models = {}

    for model_name, model_data in models_data.iteritems():

        class Meta:
            verbose_name_plural = model_data['title']

        attrs = {'__module__': __name__, 'Meta': Meta}
        for field_data in model_data['fields']:
            field_data = field_data.copy()  # to not modify existing dict by pop
            field_type = field_data.pop('type')
            field_class = FIELD_MAP[field_type]
            field_title = field_data.pop('title')
            field_name = field_data.pop('id')
            if field_type == 'char':
                field_data.setdefault('max_length', 50)
            attrs[field_name] = field_class(field_title, **field_data)
        model_class = ModelBase.__new__(ModelBase, model_name.capitalize(),
            (models.Model,), attrs)
        created_models[model_name.lower()] = model_class
    return created_models


_yaml_file_name = getattr(settings, 'AUTO_MODEL_YAML_FILE', None)
if _yaml_file_name:
    with open(_yaml_file_name) as f:
        models_data = yaml.load(f.read())

    created_models = create_dynamic_models(models_data)
    for model_class in created_models.values():
        globals()[model_class.__name__] = model_class
