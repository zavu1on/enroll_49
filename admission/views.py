from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import EnrollForm, LoginForm
from .models import EnrollApplication
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class EnrollView(FormView):
    template_name = 'enroll.html'
    form_class = EnrollForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form: EnrollForm):
        data = form.cleaned_data
        form.save()

        self.request.session['auth'] = f'{data["password_seria"]} {data["password_seria"]}'

        return super().form_valid(form)


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('auth'):
            return redirect('login')

        seria, number = request.session.get('auth').split()
        try:
            EnrollApplication.objects.get(passport_seria=seria, passport_number=number)
        except EnrollApplication.DoesNotExist:
            return redirect('login')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        seria, number = self.request.session.get('auth').split()
        enroll_app = EnrollApplication.objects.get(passport_seria=seria, passport_number=number)

        ctx['fio'] = enroll_app.fio
        ctx['status'] = list(filter(lambda el: el[0] == enroll_app.status, EnrollApplication.STATUSES))[0][1]

        return ctx


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form: LoginForm):
        data = form.cleaned_data
        self.request.session['auth'] = data['passport']

        return super().form_valid(form)


def logout_view(request):
    request.session['auth'] = None
    return redirect('/')
