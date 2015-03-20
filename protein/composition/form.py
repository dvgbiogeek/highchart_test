from django import forms
from composition.models import Protein
# import re


class ProteinForm(forms.ModelForm):
    class Meta:
        model = Protein
        fields = ['name', 'sequence']
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Protein Name',
                }),
            'sequence': forms.fields.TextInput(attrs={
                'placeholder': 'Protein Sequence',
                }),
        }
