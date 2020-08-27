from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import User, Form, Profile
from bootstrap_datepicker_plus import DatePickerInput


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'dob', 'sex', 'phone', 'division', 'position', 'skill',)

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
