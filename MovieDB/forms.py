################################################################################
# This file constitutes the Forms Layer. It is responsible for defining and
# validating forms and their fields and any other forms behavior logic.
#
# The Forms Layer knows about itself only.
################################################################################
import datetime

from django import forms
from django.forms import widgets

from MovieDB import models

class NavBarSearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=200,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search...',
        }),
    )


class MovieForm(forms.ModelForm):
    class Meta:
        model=models.Movie
        fields=['title', 'company', 'year', 'rating']
        widgets={
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Movie Title',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Production Company',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'maxlength': '4',
                'min': '1870',
                'max': datetime.date.today().year,
                'value': datetime.date.today().year
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        # mid = kwargs['mid']
        # self.fields['genres'] = forms.ModelChoiceField(queryset=models.MovieGenre.objects.filter(mid=mid))


class MovieGenreForm(forms.ModelForm):
    class Meta:
        model=models.MovieGenre
        fields=['genre']
        widgets={
            'genre': forms.CheckboxSelectMultiple(attrs={
               # 'class': 'form-control',
            }),
        }


class AddActorDirectorForm(forms.Form):
    pass


class AddActorToMovieForm(forms.Form):
    pass


class AddActorDirectorToMovieForm(forms.Form):
    pass
