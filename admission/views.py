from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from rest_framework.generics import ListAPIView
from .forms import EnrollForm, LoginForm
from .models import EnrollApplication, ExtraAchievement, ProfileClass, Teacher, Statistic, SiteConfiguration
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


class ContactsView(TemplateView):
    template_name = 'contacts.html'


class AdmissionNotAvailableView(TemplateView):
    template_name = 'not_available.html'

    def get(self, request, *args, **kwargs):
        config = SiteConfiguration.get_solo()

        if config.can_make_applications:
            return redirect('/')

        return super().get(request, *args, **kwargs)


class EnrollView(FormView):
    template_name = 'enroll.html'
    form_class = EnrollForm
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        config = SiteConfiguration.get_solo()

        if not config.can_make_applications:
            return redirect('not_available')

        return super().get(request, *args, **kwargs)

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
        config = SiteConfiguration.get_solo()

        if not config.can_make_applications:
            return redirect('not_available')

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
        status = list(filter(lambda el: el[0] == enroll_app.status, EnrollApplication.STATUSES))[0]

        ctx['fio'] = enroll_app.fio
        ctx['phone'] = enroll_app.phone
        ctx['email'] = enroll_app.email
        ctx['father_fio'] = enroll_app.father_fio
        ctx['father_phone'] = enroll_app.father_phone
        ctx['mother_fio'] = enroll_app.mother_fio
        ctx['mother_phone'] = enroll_app.mother_phone
        ctx['address'] = enroll_app.address
        ctx['passport'] = f'{enroll_app.passport_seria} {enroll_app.passport_number}'

        ctx['profile'] = enroll_app.profile_class
        ctx['exam_points'] = sum([
            enroll_app.russian_exam_point,
            enroll_app.math_exam_point,
            enroll_app.first_profile_exam_point,
            enroll_app.second_profile_exam_point
        ])
        ctx['status'] = status[1]
        ctx['can_show_literature_list'] = status[0] == 'success'
        ctx['can_show_rating'] = status[0] in [
            'resolved',
            'success',
            'rejected',
        ]
        ctx['rating_place'] = enroll_app.rating_place
        ctx['competitive_places'] = enroll_app.profile_class.competitive_places

        ctx['message'] = enroll_app.message

        return ctx


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        config = SiteConfiguration.get_solo()

        if not config.can_make_applications:
            return redirect('not_available')

        return super().get(request, *args, **kwargs)

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
