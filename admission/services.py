from functools import reduce
from admission.models import EnrollApplication, ExtraAchievement


def calc_rating(application: EnrollApplication, profile_id: int):
    k1 = application.certificate_average_score
    k2 = sum([
        application.russian_exam_point,
        application.math_exam_point,
        application.first_profile_exam_point,
        application.second_profile_exam_point,
    ]) / 4
    k3 = reduce(lambda prev, new: prev + new.point, ExtraAchievement.objects.filter(enroll_application=application), 0)

    if profile_id:
        exams = map(lambda el: el.name, application.profile_classes.get(id=profile_id).profile_exams.all())

        if 'Русский язык' in exams:
            k2 = sum([
                application.russian_exam_point,
                application.russian_exam_point,
                application.math_exam_point,
                application.first_profile_exam_point,
                application.second_profile_exam_point,
            ]) / 5
        elif 'Математика' in exams:
            k2 = sum([
                application.russian_exam_point,
                application.russian_exam_point,
                application.math_exam_point,
                application.first_profile_exam_point,
                application.second_profile_exam_point,
            ]) / 5
            print(k2)

    application.rating_place = k1 + k2 + k3
    application.save(update_fields=['rating_place'])
