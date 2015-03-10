# -*- coding: utf-8 -*-
import json
from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.auto.models import Users


class DymanicAPITestCase(TestCase):

    def test_api_list(self):
        user_list = [
            Users.objects.create(name='A', paycheck=1, date_joined=date.today()),
            Users.objects.create(name='B', paycheck=2, date_joined=date.today()),
        ]
        url = reverse('dynamic_list', kwargs={'model': 'users'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        json_data = json.loads(resp.content)
        self.assertEqual(len(json_data['data']), len(user_list))
        for user_json, user_db in zip(json_data['data'], user_list):
            self.assertUserEqual(user_json, user_db)

    def test_api_create(self):
        url = reverse('dynamic_list', kwargs={'model': 'users'})
        data = dict(name='A', paycheck=1, date_joined=date.today().isoformat())
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        user_db = Users.objects.all()[0]
        self.assertEqual(user_db.name, data['name'])
        self.assertUserEqual(json.loads(resp.content)['data'], user_db)

    def test_api_update(self):
        user = Users.objects.create(name='A', paycheck=1, date_joined=date.today())
        url = reverse('dynamic_detail', kwargs={'model': 'users', 'pk': user.pk})
        data = dict(name='B')
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 200)
        user_db = Users.objects.all()[0]
        self.assertEqual(user_db.name, data['name'])
        self.assertUserEqual(json.loads(resp.content)['data'], user_db)

    def assertUserEqual(self, user_json, user_db):
        self.assertEqual(user_json['pk'], user_db.pk)
        self.assertEqual(user_json['fields']['name'], user_db.name)
        self.assertEqual(user_json['fields']['paycheck'], user_db.paycheck)
        self.assertEqual(user_json['fields']['date_joined'], user_db.date_joined.isoformat())
