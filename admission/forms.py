from django import forms
from captcha.fields import ReCaptchaField
from .models import EnrollApplication
from .validators import validate_password_exists


class EnrollForm(forms.ModelForm):
    captcha = ReCaptchaField(label=False)
    achievements = forms.FileField(label='Индивидуальные достижения', widget=forms.FileInput(attrs={
        'multiple': True
    }))

    class Meta:
        model = EnrollApplication
        exclude = ('status', 'rating_place', 'message', 'created_date')
        widgets = {
            'birthday': forms.DateInput(attrs={
                'type': 'date'
            })
        }


class LoginForm(forms.Form):
    captcha = ReCaptchaField(label=False)
    passport = forms.CharField(
        max_length=11,
        min_length=11,
        validators=[validate_password_exists],
        widget=forms.TextInput(attrs={
            'label': 'Серия и номер паспорта'
        })
    )
