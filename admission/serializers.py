from rest_framework.serializers import ModelSerializer
from .models import Statistic


class StatisticSerializer(ModelSerializer):
    class Meta:
        model = Statistic
        fields = '__all__'
