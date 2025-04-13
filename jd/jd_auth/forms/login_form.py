from django import forms


class LoginForm(forms.Form):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    email = forms.EmailField(
        label="email",
        required=False
    )
    phone = forms.CharField(
        label="phone",
        max_length=20,
        required=False
    )


