from django import forms
from composition.models import Protein
import re


class ProteinForm(forms.ModelForm):
    class Meta:
        model = Protein
        fields = ['name', 'sequence']

    # def clean_sequence(self):
    #     return self.cleaned_data.get('sequence', '')

    # def remove_whitespace(seq):
    #     return re.sub(r"\s+", "", seq)
    # protein_name = forms.CharField(label='Protein Name', max_length=200)
