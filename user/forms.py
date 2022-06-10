from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation


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
