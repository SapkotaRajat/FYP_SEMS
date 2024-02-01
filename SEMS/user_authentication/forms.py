# user_authentication/forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'dob', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact Number'}),
            'dob': forms.DateInput(attrs={'placeholder': 'Date of Birth'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }
        
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')

        return confirm_password
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Add additional attributes or modify existing ones
        self.fields['confirm_password'].widget.attrs.update({'placeholder': 'Confirm Password'})
    
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(email=email, password=password)

        if user is None:
            print("user is none")
            raise forms.ValidationError('Invalid email or password.')

        return cleaned_data

    
