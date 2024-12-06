from django import forms


class YooMoneyForm(forms.Form):
    hash = forms.CharField(max_length=256)
    salt = forms.CharField(max_length=16)
    data = forms.CharField()
