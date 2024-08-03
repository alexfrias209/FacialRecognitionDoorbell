from django.forms import ModelForm,ValidationError
from .models import Account, UserProfile, MultipleImage,PhoneNumber
from django import forms
from django.forms import widgets
import re



class uploadForm(ModelForm):
    class Meta:
        model = Account
        fields = ['username','account_picture']


class uploadNumber(ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['name','phone_number']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
        }

class userUpdate(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username','profile_picture','user_email','unique_string']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'user_email': forms.TextInput(attrs={'placeholder': 'Enter Email'}),
            'unique_string':forms.TextInput(attrs={'placeholder': 'Enter Doorbell Serial Number'}),
        }


class UserProfileSelectionForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.none(), label="Select an account", required=False)

    def __init__(self, user_profile, *args, **kwargs):
        super(UserProfileSelectionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(profile=user_profile)
        self.fields['account'].choices = [('', 'Unknown')] + [(account.pk, account) for account in self.fields['account'].queryset]
