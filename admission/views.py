from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from rest_framework.generics import ListAPIView
from .forms import EnrollForm, LoginForm
from .models import EnrollApplication, ExtraAchievement, ProfileClass, Teacher, Statistic
from .serializers import StatisticSerializer, ProfileClassSerializer
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['profile_classes'] = ProfileClass.objects.all()
        ctx['teachers'] = Teacher.objects.all()
        ctx['statistics'] = Statistic.objects.all()
        ctx['active_statistic'] = ctx['statistics'][0]

        return ctx


class EnrollView(FormView):
    template_name = 'enroll.html'
    form_class = EnrollForm
    success_url = reverse_lazy('profile')


    def get_context_data(self, **kwargs):
        ctx = super(EnrollView, self).get_context_data(**kwargs)

        ctx['year'] = datetime.now().year

        return ctx

    def form_valid(self, form: EnrollForm):
        data = form.cleaned_data

        try:
            EnrollApplication.objects.get(
                passport_seria=data['passport_seria'],
                passport_number=data['passport_number']
            )

            form.errors['passport_seria'] = ['Такой паспорт уже зарегистрирован']
            form.errors['passport_number'] = ['Такой паспорт уже зарегистрирован']

            return super().form_invalid(form)
        except EnrollApplication.DoesNotExist:
            pass

        if data['profile_class'] is None:
            form.errors['profile_class'] = ['Это поле не может быть пустым']

            return super().form_invalid(form)

        application = form.save()

        for file in self.request.FILES.getlist('achievements'):
            ExtraAchievement.objects.create(
                file=file,
                enroll_application=application,
            )

        self.request.session['auth'] = f'{data["passport_seria"]}-{data["passport_number"]}'

        return super().form_valid(form)


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('auth'):
            return redirect('login')

        seria, number = request.session.get('auth').split('-')
        try:
            EnrollApplication.objects.get(passport_seria=seria, passport_number=number)
        except EnrollApplication.DoesNotExist:
            return redirect('login')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        seria, number = self.request.session.get('auth').split('-')
        enroll_app = EnrollApplication.objects.get(passport_seria=seria, passport_number=number)

        ctx['fio'] = enroll_app.fio
        ctx['status'] = list(filter(lambda el: el[0] == enroll_app.status, EnrollApplication.STATUSES))[0][1]
        ctx['message'] = enroll_app.message

        return ctx


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form: LoginForm):
        data = form.cleaned_data
        self.request.session['auth'] = data['passport']

        return super().form_valid(form)


class ListStatisticView(ListAPIView):

    serializer_class = StatisticSerializer
    queryset = Statistic.objects.all()


class ListProfileClassesView(ListAPIView):

    serializer_class = ProfileClassSerializer
    queryset = ProfileClass.objects.all()


def logout_view(request):
    request.session['auth'] = None
    return redirect('/')
