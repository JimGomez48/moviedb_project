"""
This file constitutes the Forms Layer. It is responsible for defining and
validating forms and their fields and any other forms behavior logic.

The Forms Layer knows about itself only.
"""

from datetime import date

from django import forms
from django.forms import widgets

from moviedb import models


class NavBarSearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=200,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search...",
            }
        ),
    )


class MovieForm(forms.ModelForm):
    class Meta:
        model = models.Movie
        fields = ["title", "year", "mpaa_rating"]
        # fields=['title', 'company', 'year', 'rating']
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Movie Title",
                }
            ),
            # 'company': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Production Company',
            # }),
            "year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "4",
                    "min": "1870",
                    "max": date.today().year,
                    "value": date.today().year,
                }
            ),
            "mpaa_rating": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class MovieGenreForm(forms.Form):
    genres = forms.MultipleChoiceField(
        choices=models.Genre.Genres.choices,
        widget=forms.CheckboxSelectMultiple(),
    )


class DateWidget(widgets.DateInput):
    """Plain HTML date input; replaces the unmaintained django-datetime-widget."""

    def __init__(self, bootstrap_version=None, options=None, attrs=None):
        super().__init__(attrs=attrs, format="%m/%d/%Y")


class DateOptions:
    OPTIONS = {
        "format": "mm/dd/yyyy",
        "pickerPosition": "bottom-left",
    }


class ActorForm(forms.ModelForm):
    dod = forms.DateField(
        required=False,
        label=models.Actor._meta.fields[5].verbose_name,
        widget=DateWidget(
            bootstrap_version=3,
            options=DateOptions.OPTIONS,
            attrs={
                "placeholder": DateOptions.OPTIONS["format"],
                "id": "actor_dod",
            },
        ),
    )

    class Meta:
        model = models.Actor
        fields = ["first", "last", "sex", "dob", "dod"]
        widgets = {
            "last": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Actor's Last Name"},
            ),
            "first": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Actor's First Name"},
            ),
            "sex": forms.Select(
                attrs={"class": "form-control"},
            ),
            "dob": DateWidget(
                bootstrap_version=3,
                options=DateOptions.OPTIONS,
                attrs={
                    "placeholder": DateOptions.OPTIONS["format"],
                    "id": "actor_dob",
                },
            ),
        }


class DirectorForm(forms.ModelForm):
    dod = forms.DateField(
        required=False,
        label=models.Director._meta.fields[4].verbose_name,
        widget=DateWidget(
            bootstrap_version=3,
            options=DateOptions.OPTIONS,
            attrs={
                "placeholder": DateOptions.OPTIONS["format"],
                "id": "director_dod",
            },
        ),
    )

    class Meta:
        model = models.Director
        fields = ["first", "last", "dob", "dod"]
        widgets = {
            "last": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Director's Last Name"},
            ),
            "first": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Director's First Name"},
            ),
            "dob": DateWidget(
                bootstrap_version=3,
                options=DateOptions.OPTIONS,
                attrs={
                    "placeholder": DateOptions.OPTIONS["format"],
                    "id": "director_dob",
                },
            ),
        }


class ActorToMovieForm(forms.ModelForm):
    class Meta:
        model = models.MovieActor
        # fields = ['movie', 'actor', 'role']
        fields = ["movie", "actor"]
        widgets = {
            "movie": forms.Select(
                attrs={"class": "form-control"},
            ),
            "actor": forms.Select(
                attrs={"class": "form-control"},
            ),
            # 'role': forms.TextInput(
            #     attrs={'class': 'form-control', 'placeholder': "Actor's role in the film"},
            # ),
        }


class DirectorToMovieForm(forms.Form):
    movie = forms.ModelChoiceField(
        queryset=models.Movie.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    director = forms.ModelChoiceField(
        queryset=models.Director.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        movie = cleaned_data.get("movie")
        director = cleaned_data.get("director")
        if movie and director and movie.directors.filter(pk=director.pk).exists():
            raise forms.ValidationError(
                f"{director.get_full_name()} is already a director of {movie.title}."
            )
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["user_name", "movie", "rating", "comment"]
        widgets = {
            "user_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your user name",
                },
            ),
            "movie": forms.Select(
                attrs={"class": "form-control"},
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "rating form-control",
                    "data-min": 0,
                    "data-max": max(models.Review.StarRatings.values),
                    "data-step": "1",
                    "data-size": "sm",
                    "data-show-clear": "false",
                },
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write a comment...",
                },
            ),
        }
