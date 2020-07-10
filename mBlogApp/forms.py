from django import forms
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(label= 'Username', label_suffix= '', max_length= 20)
    password = forms.CharField(label= 'Password', label_suffix= '', widget= forms.PasswordInput, 
                               help_text= "Please don't use an important password.", required= False)
    confirm_password = forms.CharField(label= 'Confirm Password', label_suffix= '', widget= forms.PasswordInput)

    """
    These are called, once it has been affirmed that
    input has been given.
    """
    def clean_username(self):
        username_entered = self.cleaned_data['username']
        user = User.objects.filter(username= username_entered).first()
        
        if user:
            raise forms.ValidationError("That username is already taken", code='invalid')
        
        return username_entered

    def clean_confirm_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The passwords don't match", code='invalid')

        return password1
