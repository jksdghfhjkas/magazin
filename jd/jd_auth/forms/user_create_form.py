from django import forms
from jd_auth.models import User


"""
форма создания пользователя
"""

class CustomUserCreateForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    re_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )


    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 're_password']
        
        error_messages = {
            'phone': {
                'unique': "Пользователь с таким номером телефона уже существует.",
            },
            'email': {
                'unique': "Пользователь с такой почтой уже существует!"
            }
        }


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        email = cleaned_data.get("email")

        if email:
            # если пользователь ввел почту то должен ввести и пароли
            if password and re_password and password != re_password:
                raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


