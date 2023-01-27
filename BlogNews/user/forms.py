from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from allauth.socialaccount.forms import SignupForm


class UserCreationFormBlog(UserCreationForm):

    error_messages = {
        'password_mismatch': 'As senhas informadas não coincidem.',
    }

    password1 = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Confirme a senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Digite a senha novamente para confirmação',
    )

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
            if self.fields[field].help_text:
                self.fields[field].widget.attrs['aria-describedby'] = field + 'Help'
                self.fields[field].help_text = '<div id="' + field + 'Help" class="form-text">' + \
                                               self.fields[field].help_text + '</div>'


class UserChangeFormBlog(forms.ModelForm):
    error_messages = {
        'password_mismatch': 'As senhas informadas não coincidem.',
    }

    password1 = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label='Confirme a senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Digite a senha novamente para confirmação',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
            if self.fields[field].help_text:
                self.fields[field].widget.attrs['aria-describedby'] = field + 'Help'
                self.fields[field].help_text = '<div id="' + field + 'Help" class="form-text">' + \
                                               self.fields[field].help_text + '</div>'
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['required'] = True

    def clean(self):
        cleaned_data = self.cleaned_data

        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if (password1 or password2) and not (password1 and password2):
            self.add_error('password2', self.error_messages['password_mismatch'])

        if password1 and password2:
            if password1 == password2:
                try:
                    password_validation.validate_password(password1, self.instance)
                except ValidationError as error:
                    self.add_error('password1', error)
            else:
                self.add_error('password2', self.error_messages['password_mismatch'])

        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class AuthenticationFormBlog(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label


class PasswordResetFormBlog(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'


class SetPasswordFormBlog(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label


class SignupFormBlog(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
