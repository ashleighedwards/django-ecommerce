from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )

    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Address',
            'rows': 3
        })
    )
    default_shipping = forms.BooleanField(
        required=False,
        label="Use this as my default shipping address",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'address', 'default_shipping']

    # Full name validation
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if any(char.isdigit() for char in full_name):
            raise forms.ValidationError("Full name cannot contain numbers.")
        return full_name

    # Address validation
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise ValidationError("Address must be at least 10 characters long.")
        if not any(char.isdigit() for char in address):
            raise ValidationError("Address must include a street number.")
        # Optional: prevent special characters-only addresses
        import re
        if not re.search(r'[A-Za-z0-9]', address):
            raise ValidationError("Address must contain letters or numbers.")
        return address

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = User
        fields = ['email']

    # Example of validation: ensure email is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
