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


# class AddMovieForm(forms.Form):
#     title = forms.CharField(
#         max_length=100,
#         label='Title',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Movie Title',
#             })
#     )
#     year = forms.IntegerField(
#         min_value='1870',
#         max_value=datetime.date.today().year,
#         widget=widgets.NumberInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         ),
#     )
#     mpaa_rating = forms.ChoiceField(
#         choices=[],
#         widget=forms.Select(attrs={
#             'class': 'form-control',
#         }),
#     )
#     company = forms.CharField(
#         max_length=50,
#         label='Company',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Production Company'
#             }),
#     )
#     genres = forms.MultipleChoiceField(
#         choices=[],
#         widget=forms.CheckboxInput(
#             attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Production Company'
#             }),
#     )


class AddMovieForm(forms.ModelForm):
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

    def __init__(self):
        super(AddMovieForm, self).__init__()
        # self.title.widgets


class AddActorDirectorForm(forms.Form):
    pass


class AddActorToMovieForm(forms.Form):
    pass


class AddActorDirectorToMovieForm(forms.Form):
    pass
