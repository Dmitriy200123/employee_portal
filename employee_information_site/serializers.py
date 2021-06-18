from employee_information_site.models import EmployeePosition
from rest_framework import serializers


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = ['id', 'name']
