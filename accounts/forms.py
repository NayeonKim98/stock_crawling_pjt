from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import InterestedStock

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']

class InterestedStockForm(forms.ModelForm):
    class Meta:
        model = InterestedStock
        fields = ['company_name']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': '관심 종목 입력'}),
        }
        labels = {
            'company_name': '',
        }
