from django.contrib import admin
from . import models


for model in models.created_models.values():
    admin.site.register(model)
