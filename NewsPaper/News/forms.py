from django import forms
from .models import Category


class SubscribeForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select)

    class Meta:
        fields = ('email', 'category')