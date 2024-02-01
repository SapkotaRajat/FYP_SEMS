# user_authentication/forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'contact_number', 'dob']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'type': 'text', 'autofocus': True}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'type': 'text', 'autofocus': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'type': 'text', 'autofocus': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'type': 'email', 'autofocus': True}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact Number', 'type': 'tel', 'autofocus': True}),
            'dob': forms.DateInput(attrs={'placeholder': 'DOB (DD/MM/YYYY)', 'type': 'date', 'autofocus': True}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password', 'type': 'password', 'autofocus': True}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'type': 'password', 'autofocus': True}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Username cannot be empty.')

        # Check if the username is unique
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Username must be unique.')

        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    # Field as username
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Authenticate the user using the provided username
        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError('Invalid username or password.')

        return cleaned_data


    
