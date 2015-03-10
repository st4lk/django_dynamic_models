# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.management import call_command
from apps.auto.models import create_dynamic_models


test_data_models = {
    "gifts": {
        "title": u"Подарки",
        "fields": [
            {"id": "title", "title": u"Название", "type": "char"},
            {"id": "weight", "title": u"Вес", "type": "int"},
        ]
    },
}


class DymanicModelTestCase(TestCase):
    def test_models_created(self):
        created_models = create_dynamic_models(test_data_models)
        gift_model = created_models['gifts']
        call_command('syncdb', noinput=True, verbosity=0)

        gift = gift_model(title=u"Шар", weight=200)
        gift.save()
        self.assertEqual(gift, gift_model.objects.get(pk=gift.pk))
