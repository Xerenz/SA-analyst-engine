from django import forms
from .models import Malware


class MalwareForm(forms.Form):
    name = forms.CharField(label='Malware Name', max_length=100)

    class Meta:
        model = Malware
        fields = ('name', )