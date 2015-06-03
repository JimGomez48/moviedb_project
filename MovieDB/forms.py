################################################################################
# This file constitutes the Forms Layer. It is responsible for defining and
# validating forms and their fields and any other forms behavior logic.
#
# The Forms Layer knows about itself only.
################################################################################


from django import forms


class NavBarSearchForm(forms.Form):
    search_term = forms.CharField(max_length=200,
                                  label='',
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Search...',
                                   }))
