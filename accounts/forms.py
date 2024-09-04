from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CreateUserForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('role')

        if self.instance and self.instance.pk:
            # If the form is being used to edit an existing user, remove password fields
            self.fields.pop('password1')
            self.fields.pop('password2')
        else:
            # Apply custom attributes to password fields
            self.fields['password1'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"
            self.fields['password2'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"
            self.fields['password1'].label = "Mot de pass"
            self.fields['password2'].label = "Confirmez votre mot de pass"

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
        }

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        email_check = CustomUser.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError('This Email already exists')
        if len(password) < 5:
            raise forms.ValidationError(
                'Your password should have more than 5 characters')
        return super(CreateUserForm, self).clean(*args, **kwargs)

    # Automatically populate first_name, last_name and username from email (example logic)
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        if user.email:
            # Simple logic, customize as needed
            user.first_name = user.email.split('@')[0]
            user.last_name = "_"
            user.username = user.email.split('@')[0]
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'sex',
            'phone',
            'image',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'sex': forms.Select(attrs={'class': "input_selector mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
        }
