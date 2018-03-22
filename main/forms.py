from django import forms

class movieForm(forms.Form):
    title = forms.CharField(max_length=200)