from django.forms import ModelForm
from .models import EnrollApplication


class EnrollForm(ModelForm):

    class Meta:
        model = EnrollApplication
        exclude = ('status', 'rating_place')
