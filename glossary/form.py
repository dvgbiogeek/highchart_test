from django import forms
from glossary.models import Glossary


class GlossaryForm(forms.ModelForm):
    class Meta:
        model = Glossary
        fields = ['term', 'definition', 'reference']
        widgets = {
            'term': forms.fields.TextInput(attrs={
                'placeholder': 'New term',
                'class': 'form-control',
                }),
            'definition': forms.Textarea(attrs={
                'placeholder': 'Term definition',
                'class': 'form-control',
                'type': 'textarea',
                'ng-model': 'ctrl.mark',
                }),
            'reference': forms.fields.TextInput(attrs={
                'placeholder': 'Reference',
                'class': 'form-control'
                })
        }
        error_messages = {
            'term': {'required': 'Please add a glossary term.'},
            'definition': {'required': 'Please add a definition to the glossary term.'},
            'reference': {'required': 'A reference is required.'}
        }
