from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from userlogin.models import UserProfile, UserAddress

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password_validation.validate_password(password1)
        return password1

    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        name = self.cleaned_data.get('name')

        user = UserProfile.objects.create_user(email=email, password=password, name=name)
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Invalid email or password')
            if not self.user.is_active:
                raise forms.ValidationError('This account is inactive')
        return self.cleaned_data

    def get_user(self):
        return self.user
        
class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['email', 'mobile', 'name', 'address_line_1', 'address_line_2', 'city', 'state', 'zip_code']
    
