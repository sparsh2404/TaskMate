from django import forms
from .models import tasklist

class Taskform(forms.ModelForm):
    class Meta:
        model = tasklist
        fields = ['task','done']


