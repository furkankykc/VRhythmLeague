from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from League import validators
from League.models import Song, Week


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


# class PlayListModelForm(forms.ModelForm):
#     class Meta:
#         model = PlayList
#         fields = ('name', 'game', 'difficulty', 'songs')
#
#     def __init__(self, *args, **kwargs):
#         forms.ModelForm.__init__(self, *args, **kwargs)
#         self.fields['songs'].queryset = Song.objects.all()


class WeekModelForm(forms.ModelForm):
    class Meta:
        model = Week
        fields = ('description', 'songs')
        exclude = ['game']

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance.season.difficulty:
            if self.instance.season.difficulty == self.instance.season.HARD:
                self.fields['songs'].queryset = Song.objects.filter(hard__isnull=False)
            elif self.instance.season.difficulty == self.instance.season.NORMAL:
                self.fields['songs'].queryset = Song.objects.filter(normal__isnull=False)
            elif self.instance.season.difficulty == self.instance.season.EASY:
                self.fields['songs'].queryset = Song.objects.filter(easy__isnull=False)
            elif self.instance.season.difficulty == self.instance.season.EXPERT:
                self.fields['songs'].queryset = Song.objects.filter(expert__isnull=False)
            elif self.instance.season.difficulty == self.instance.season.EXPERTPLUS:
                self.fields['songs'].queryset = Song.objects.filter(expert_plus__isnull=False)
        else:
            self.fields['songs'].queryset = Song.objects.all()

    def clean(self):

        error, messagge = validators.max_releations(self.cleaned_data['songs'],
                                                    self.instance.songs,
                                                    self.instance.season.type.song_count)
        if error:
            raise forms.ValidationError("Exception:%s" % messagge)
