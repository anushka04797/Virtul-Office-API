from rest_framework import serializers
from organizations.models import Designation


class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = (
            'id',
            'name',
            'department',
            'parent',
        )


class SlcSerializer(serializers.ModelSerializer):
    designation = DesignationSerializer()

    class Meta:
        model = Designation
        fields = (
            'id',
            'salary',
            'department',
            'designation',
        )
