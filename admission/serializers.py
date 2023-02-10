from rest_framework.serializers import ModelSerializer
from .models import Statistic, ProfileClass, Exam


class StatisticSerializer(ModelSerializer):
    class Meta:
        model = Statistic
        fields = '__all__'


class ExamSerializer(ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ProfileClassSerializer(ModelSerializer):
    profile_exams = ExamSerializer(many=True)

    class Meta:
        model = ProfileClass
        exclude = ['color']
