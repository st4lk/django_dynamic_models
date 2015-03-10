# -*- coding: utf-8 -*-
import json
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import BaseFormView, BaseUpdateView
from django.http import HttpResponse, Http404
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import fields_for_model
from django.forms.fields import DateField
from django.forms.models import model_to_dict
from .models import created_models
from .forms import created_forms


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        models = []
        for model_name, model_class in created_models.items():
            models.append({
                "name": model_name,
                "label": model_class._meta.verbose_name_plural,
            })
        context['models'] = models
        return context


class DynamicMixin(object):
    context_object_name = "api_data"
    single_object_methods = ('POST', 'PUT')

    @property
    def model_name(self):
        if not hasattr(self, '_model_name'):
            model_name = self.kwargs['model'].lower()
            if model_name not in created_models:
                raise Http404
            self._model_name = model_name
        return self._model_name

    def get_model_meta_data(self):
        fields = []
        model = created_models[self.model_name]
        for field_name, field_object in fields_for_model(model).items():
            fields.append({
                'name': field_name,
                'label': field_object.label,
                'type': field_object.widget.input_type,
                'attrs': field_object.widget.attrs,
                'widget': 'datepicker' if isinstance(field_object, DateField) else None,
                'required': field_object.required,
            })
        return {
            'fields': fields,
            'url': reverse('dynamic_list', kwargs={'model': self.model_name}),
            'verbose_plural': model._meta.verbose_name_plural,
        }

    def get_queryset(self):
        return created_models[self.model_name].objects.all()

    def get_form_class(self):
        return created_forms[self.model_name]

    def form_valid(self, form):
        obj = form.save()
        context = {self.context_object_name: [obj, ]}
        return self.render_to_response(context)

    def form_invalid(self, form):
        context = {self.context_object_name: [None, ], "error": form.errors}
        return self.render_to_response(context, serialize=False)

    def convert_context_to_json(self, context, serialize=True):
        result = {'data': context[self.context_object_name]}
        if serialize:
            result['data'] = serializers.serialize('python', result['data'])
        if self.request.method in self.single_object_methods:
            result['data'] = result['data'][0]
        result['error'] = context.get('error', None)
        result['meta'] = self.get_model_meta_data()
        return json.dumps(result, cls=DjangoJSONEncoder)


class JsonMixin(object):
    def render_to_response(self, context, serialize=True, **response_kwargs):
        return self.render_to_json_response(context, serialize, **response_kwargs)

    def render_to_json_response(self, context, serialize, **response_kwargs):
        return HttpResponse(
            self.convert_context_to_json(context, serialize),
            content_type='application/json',
            **response_kwargs
        )


class DynamicModelListCreateView(DynamicMixin, JsonMixin, ListView, BaseFormView):
    pass


class DynamicModelUpdateView(DynamicMixin, JsonMixin, BaseUpdateView):
    single_object_methods = ('POST', 'PUT', 'GET')

    def get_form_kwargs(self):
        kwargs = super(DynamicModelUpdateView, self).get_form_kwargs()
        data = model_to_dict(self.object, exclude=['id'])
        # .update() is not good for QueryDict
        for k in kwargs['data']:
            data[k] = kwargs['data'][k]
        kwargs['data'] = data
        return kwargs

    def get(self, request, *args, **kwargs):
        """Just return single object"""
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context[self.context_object_name] = [context[self.context_object_name], ]
        return self.render_to_response(context)
