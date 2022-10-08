from functools import reduce
from admission.models import EnrollApplication


def calc_rating(application: EnrollApplication):
    k1 = application.certificate_average_score
    k2 = sum([
        application.russian_exam_point,
        application.math_exam_point,
        application.first_profile_exam_point,
        application.second_profile_exam_point,
    ]) / 4
    k3 = reduce(lambda prev, new: prev + new.point, application.extra_achievements.all(), 0)

    return k1 + k2 + k3
