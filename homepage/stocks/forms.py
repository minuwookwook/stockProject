from django import forms

class NumForm(forms.Form):
    stock = forms.CharField()
