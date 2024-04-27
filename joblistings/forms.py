# forms.py in your wagtail app
from django import forms

class JobImportForm(forms.Form):
    excel_file = forms.FileField()
