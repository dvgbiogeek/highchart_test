from django import forms
from composition.models import Protein


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
        error_messages = {
            'name': {'required': 'Please add a name and sequence.'},
            'sequence': {'required': 'Please add a name and sequence.'},
        }
