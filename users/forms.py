from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
    

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username","email"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
       
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['password']