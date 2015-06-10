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


class MovieGenreForm(forms.Form):
    genres = forms.MultipleChoiceField(
        choices=models.MovieGenre.GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
    )


class ActorForm(forms.ModelForm):
    class Meta:
        model = models.Actor
        fields = {'last', 'first', 'sex', 'dob', 'dod'}
        widgets = {
            'last': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
            'first': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'sex': forms.Select(attrs={
                'class': 'form-control',
            }),
            'dob': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'dod': forms.DateInput(attrs={
                'class': 'form-control',
            }),
        }


class DirectorForm(forms.ModelForm):
    class Meta:
        model = models.Director
        fields = {'last', 'first', 'dob', 'dod'}
        widgets = {
            'last': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
            'first': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'sex': forms.Select(attrs={
                'class': 'form-control',
            }),
            'dob': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'dod': forms.DateInput(attrs={
                'class': 'form-control',
            }),
        }


class AddActorToMovieForm(forms.Form):
    pass


class AddActorDirectorToMovieForm(forms.Form):
    pass
