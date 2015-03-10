# -*- coding: utf-8 -*-
from django.forms.models import ModelFormMetaclass, ModelForm
from .models import created_models

created_forms = {}


def create_dynamic_forms(created_models):
    created_forms = {}
    for model_name, model_class in created_models.iteritems():

        class Meta:
            model = model_class

        attrs = {'__module__': __name__, 'Meta': Meta}
        form_class = ModelFormMetaclass.__new__(ModelFormMetaclass,
            model_class.__name__ + 'Form', (ModelForm, ), attrs)
        created_forms[model_name] = form_class

    return created_forms


created_forms = create_dynamic_forms(created_models)
for form_class in created_forms.values():
    globals()[form_class.__name__] = form_class
