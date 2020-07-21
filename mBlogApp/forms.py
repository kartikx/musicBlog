from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(label_suffix= '', max_length= 20)
    password = forms.CharField(label_suffix= '', widget= forms.PasswordInput, 
                               help_text= "Please don't use an important password.")
    confirm_password = forms.CharField(label_suffix= '', widget= forms.PasswordInput)


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

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("confirm_password")

        if password1 != password2 :
            self.add_error('password', forms.ValidationError(""))
            self.add_error('confirm_password', forms.ValidationError("Passwords don't match"))
        
        return cleaned_data

