from django import forms

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')

class Cal(forms.Form) :
    number1= forms.IntegerField()
    number2= forms.IntegerField()
