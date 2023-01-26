from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import EnrollForm, LoginForm
from .models import EnrollApplication, ExtraAchievement
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


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

        if data['profile_class'] in None:
            form.errors['profile_class'] = ['Это поле не может быть пустым']

            return super().form_invalid(form)

        application: EnrollApplication = form.save()

        for file in self.request.FILES.getlist('achievements'):
            ExtraAchievement.objects.create(
                file=file,
                enroll_application=application,
            )

        self.request.session['auth'] = f'{data["passport_seria"]} {data["passport_number"]}'

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


def logout_view(request):
    request.session['auth'] = None
    return redirect('/')


def test_data(request):
    # todo delete
    import random
    import datetime
    from django.http.response import JsonResponse

    # EnrollApplication.objects.create(
    #     fio='test test test',
    #     birthday=datetime.datetime.now(),
    #     address='test',
    #     phone=f'test',
    #     email=f'test@mail.ru',
    #     passport_seria=1234,
    #     passport_number=123456,
    #
    #     father_fio='test test test',
    #     father_phone='test test test',
    #     father_address='test test test',
    #     mother_fio='test test test',
    #     mother_phone='test test test',
    #     mother_address='test test test',
    #
    #     certificate_average_score=5,
    #     russian_exam_point=27,
    #     russian_exam_mark=4,
    #     math_exam_point=25,
    #     math_exam_mark=5,
    #
    #     first_profile_exam_id=1,
    #     first_profile_exam_point=31,
    #     first_profile_exam_mark=4,
    #     second_profile_exam_id=2,
    #     second_profile_exam_point=18,
    #     second_profile_exam_mark=15,
    #
    #     is_accepted=True,
    #     notification_method='phone',
    #
    #     profile_class_id=1
    # )

    for i in range(500):
        EnrollApplication.objects.create(
            fio='test test test',
            birthday=datetime.datetime.now(),
            address='test',
            phone=f'test-{i}',
            email=f'test-{i}@mail.ru',
            passport_seria=random.randrange(1000, 9999),
            passport_number=random.randrange(100000, 999999),

            father_fio='test test test',
            father_phone='test test test',
            father_address='test test test',
            mother_fio='test test test',
            mother_phone='test test test',
            mother_address='test test test',

            certificate_average_score=random.randrange(2, 5),
            russian_exam_point=random.randrange(1, 33),
            russian_exam_mark=random.randrange(2, 5),
            math_exam_point=random.randrange(1, 33),
            math_exam_mark=random.randrange(2, 5),

            first_profile_exam_id=1,
            first_profile_exam_point=random.randrange(1, 33),
            first_profile_exam_mark=random.randrange(2, 5),
            second_profile_exam_id=2,
            second_profile_exam_point=random.randrange(1, 33),
            second_profile_exam_mark=random.randrange(2, 5),

            is_accepted=True,
            notification_method='phone',

            profile_class_id=1
        )

    return JsonResponse({'success': True})
