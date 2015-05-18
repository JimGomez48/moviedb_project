from django import forms


class NavBarSearchForm(forms.Form):
    search_term = forms.CharField(max_length=200,
                                  label='',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Search...',
                                   }))
