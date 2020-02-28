from django.conf.urls import url
from django.contrib import admin, messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from jwt.utils import force_unicode

from League.forms import ChooseSiteForm
from . import services
# Register your models here.
from django.db.models.base import ModelBase

from League import models, forms

for model_name in dir(models):
    try:
        model = getattr(models, model_name)
        if isinstance(model, ModelBase):
            admin.site.register(model)
            # print(model_name)
    except Exception as ex:
        print(ex)
        pass

#


#      save()->services.create_season()
#
# class SeasonInline(admin.StackedInline):
#     model = models.Season
#     # exclude = ["uid", "join_date", "mod_date"]
#
admin.site.unregister(models.Season)


class SeasonAdmin(admin.ModelAdmin):
    # inlines = [SeasonInline, ]
    exclude = ['finishing_at']

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            # season_data = form.save()
            services.create_season_(obj)

        super(SeasonAdmin, self).save_model(request, obj, form, change)


admin.site.register(models.Season, SeasonAdmin)


# admin.site.unregister(models.PlayList)


# class PlaylistAdmin(admin.ModelAdmin):
# form = AthleteForm
# list_select_related = ('game',)
#
# def formfield_for_foreignkey(self, db_field, request, **kwargs):
# print(self.form)
# if db_field.name == "game":
#     kwargs["queryset"] = models.Song.objects.filter(game_id=1)
# return super(PlaylistAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

# def get_form(self, request, obj=None, **kwargs):
#     form = super(PlaylistAdmin, self).get_form(request, obj, **kwargs)
#     try:
#         game = obj.game
#     except:
#         game = 1
#     if form.is_valid:
#         form.fields['songs'].queryset = models.Song.objects.filter(game__id=game)
#     return form

# def formfield_for_foreignkey(self, db_field, request, **kwargs):
#     print(db_field.name)
#     if db_field.name == "game":
#         # kwargs["queryset"] = models.Song.objects.filter(game_id=1)
#         print('yaaay')
#     return super(PlaylistAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
# #
# def formfield_for_manytomany(self, db_field, request, **kwargs):
#     if self.form.is_valid:
#         print(self.form.cleaned_data)
#     if db_field.name == "songs":
#         kwargs["queryset"] = models.Song.objects.filter(game_id=1)
#     return super(PlaylistAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


# admin.site.register(models.PlayList, PlaylistAdmin)
# admin.site.unregister(models.PlayList)


