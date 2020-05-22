from django.contrib import admin

from League.forms import WeekModelForm
from . import services
from .models import *


class PageAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('name',)}  # new
    list_display = (
        'name',
        'slug',
    )
    # fields = ('name', 'slug')

    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(PageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['slug'].disabled = True
        form.base_fields['slug'].help_text = "This field is not editable"
        return form

    class Meta:
        abstract = True


@admin.register(Game)
class GameAdmin(PageAdmin):
    # list_display = ('name', 'slug')
    pass
# @admin.register(AlphaUsers)
# class AlphaUsersAdmin(PageAdmin):
#     pass
admin.site.register(AlphaUsers)

@admin.register(Song)
class SongAdmin(PageAdmin):
    list_display = ('name', 'sub_name')
    search_fields = ['name']
    list_filter = ('game',)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    # inlines = [SeasonInline, ]
    exclude = ['user_list']

    # prepopulated_fields = {'slug': ('name',)}  # new
    readonly_fields = ['finishing_at']

    # def save_form(self, request, form, change):
    #     form.save(commit=False)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            # season_data = form.save()
            # if not season_data.id:
            # print(change)
            if not change:
                services.create_season_(obj)
            else:
                if 'type' in form.changed_data:
                    print(form.cleaned_data['type'])

                # for data in form.changed_data:

                super(SeasonAdmin, self).save_model(request, obj, form, change)
                services.clean_weeks(obj)
                Week.objects.bulk_create(services.create_week(obj))


# @admin.register(PlayList)
# class PlaylistAdmin(admin.ModelAdmin):
#     class Media:
#         js = ("league/js/AdminSiteClick.js",)
#
#     # autocomplete_fields = ['songs']
#     form = PlayListModelForm
#
#     # filter_horizontal = ('songs',)
#     # add_form_template = 'admin/change_form.html'


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    # fields = ('description', 'songs')
    readonly_fields = ['season', 'game', 'limit','created_at','updated_at']
    form = WeekModelForm
    list_display = ('name', 'game', 'season', 'limit', 'difficulty',)  # 'get_week')
    list_filter = ('season',)
    ordering = ('season', 'created_at',)
    filter_horizontal = ('songs',)

    def game(self, obj):
        return obj.season.game.name

    def limit(self, obj):
        return obj.season.type.song_count

    def difficulty(self, obj):
        return obj.season.get_difficulty()


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'song_count')

    # def save_model(self, request, obj, form, change):
    #     if form.is_valid():
    #         # season_data = form.save()
    #         # if not season_data.id:
    #         # print(change)
    #         # desicion making for update or create instance
    #         if change:
    #             if 'is_daily' or 'count' in form.changed_data:
    #                 # print(form.cleaned_data['type'])
    #
    #                 super(TypeAdmin, self).save_model(request, obj, form, change)
    #                 for season in Season.objects.filter(type=obj):
    #                     services.clean_weeks(season)
    #                     Week.objects.bulk_create(services.create_week(season))
