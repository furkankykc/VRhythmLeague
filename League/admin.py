from django.contrib import admin

# Register your models here.
from django.db.models.base import ModelBase

from League import models

for model_name in dir(models):
    try:
        model = getattr(models, model_name)
        if isinstance(model, ModelBase):
            admin.site.register(model)
            # print(model_name)
    except Exception as ex:
        print(ex)
        pass
