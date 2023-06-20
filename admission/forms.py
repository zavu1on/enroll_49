from django import forms
from captcha.fields import ReCaptchaField
from .models import EnrollApplication
from .validators import validate_password_exists


class EnrollForm(forms.ModelForm):
    # captcha = ReCaptchaField(label=False)
    achievements = forms.FileField(label='Индивидуальные достижения', required=False, widget=forms.FileInput(attrs={
        'multiple': True,
    }))

    def __init__(self, *args, **kwargs):
        super(EnrollForm, self).__init__(*args, **kwargs)
        self.labels = []
        with_helptext = [
            forms.fields.TypedChoiceField,
            forms.fields.FileField,
            forms.models.ModelChoiceField,
            forms.fields.DateField,
        ]

        for field in self.fields.keys():
            label = self.fields[field].label

            if field != 'is_accepted':
                self.labels.append({
                    'id': f'id_{field}',
                    'label': label
                })
                self.fields[field].widget.attrs['class'] = 'input'

            self.fields[field].widget.attrs['placeholder'] = label
            self.fields[field].label = ''
            self.fields[field].help_text = ''

            if type(self.fields[field]) in with_helptext:
                self.fields[field].help_text = label

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
            'placeholder': 'Паспорт',
            'class': 'mt-40'
        })
    )
