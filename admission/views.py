from django.views.generic import TemplateView, FormView
from .forms import EnrollForm
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class EnrollView(FormView):
    template_name = 'enroll.html'
    form_class = EnrollForm


class ProfileView(TemplateView):
    template_name = 'profile.html'
