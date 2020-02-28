from django.conf.urls import url
from django.contrib import admin, messages
from django.db.models import Q
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
admin.site.unregister(models.PlayList)


class ChangeSiteAdmin(admin.ModelAdmin):
    """
    Extends ``django.contrib.admin.ModelAdmin`` class. Provides some extra
    views for change site management at admin panel. It also changes
    default ``change_form_template`` option to
    ``'components/admin/change_form.html'`` which is required for
    adding ``changesite`` object action.
    **Extra options**
    ``filter_by_site_fields`` - list of fields to filter to selected site.
    Can be field name or tuple consisting of field name and lookup field.
    """
    change_form_template = 'components/admin/change_form.html'
    fields = ('game', 'songs')

    def get_site_id(self, request, obj=None):
        if obj:
            return obj.game.id
        else:
            return int(request.GET.get('game', 0))

    def get_urls(self):
        urls = super(ChangeSiteAdmin, self).get_urls()
        # info = self.model._meta.app_label, self.model._meta.module_name
        my_urls = [
            url(r'^(?P<object_id>\d+)/changesite/$',
                self.admin_site.admin_view(self.changesite),
                name='_changesite'),
        ]
        return my_urls + urls

    def add_view(self, request, *args, **kwargs):
        site_id = self.get_site_id(request)
        if not site_id:
            return self.selectsite(request)
        return super(ChangeSiteAdmin, self).add_view(request, *args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(
            ChangeSiteAdmin, self
        ).get_form(request, obj, **kwargs)
        site_id = self.get_site_id(request, obj)
        # disable adding new site in this form
        field = form.base_fields['songs']
        field.widget.can_add_related = False
        # restrict site choices to selected site
        field.choices = [c for c in field.choices if c[0] == site_id]
        # restrict additional ForeignKey and ManyToManyField fields
        for opts in getattr(self, 'filter_by_site_fields', []):
            if type(opts) is str:
                field = opts
                kwargs = {'game__id': site_id}
            else:
                field = opts[0]
                kwargs = {opts[1]: site_id}
            field = form.base_fields[field]
            field.queryset = field.queryset.filter(**kwargs)
        return form

    def selectsite(self, request):
        model = self.model
        opts = model._meta
        form = ChooseSiteForm()
        context = {
            'form': form,
            'title': ('Select site for new %s') % force_unicode(opts.verbose_name),
        }
        template = 'components/admin/selectsite.html'
        return render_to_response(template, context)

    def changesite(self, request, object_id, **kwargs):
        original = self.get_object(request, object_id)
        if request.POST:
            form = ChooseSiteForm(request.POST)
            if form.is_valid():
                site = form.cleaned_data['game']
                if (hasattr(original, 'changesite')):
                    original.changesite(site)
                else:
                    original.game = site
                    original.save()
                msg = ("Site has been changed to %s") % (site)
                messages.add_message(request, messages.INFO, msg)
                # info = self.model._meta.app_label, self.model._meta.module_name
                return redirect('admin:%s_%s_change', original.id)
        else:
            form = ChooseSiteForm(initial={'site': original.game})

        model = self.model
        opts = model._meta
        context = RequestContext(request, {
            'form': form,
            'title': ('Change site for %s') % force_unicode(opts.verbose_name),
        })
        template = 'components/admin/changesite.html'
        return render_to_response(template, context)


admin.site.register(models.PlayList, ChangeSiteAdmin)
