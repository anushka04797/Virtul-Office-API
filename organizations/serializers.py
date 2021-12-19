from rest_framework import serializers
from organizations.models import Designation, Slc, DmaCalender, HolidayCalender


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

    class Meta:
        model = Slc
        fields = (
            'id',
            'employee',
            'monthly_rate',
            'hourly_rate',
            'ep',
            'planned_hours',
            'planned_value',
            'slc'
        )


class DmaCalenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = DmaCalender
        fields = (
            'id',
            'Company', 'Year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
        )


class HolidayCalenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = HolidayCalender
        fields = (
            'id',
            'Year', 'Month', 'holiday_title', 'start_date', 'end_date'
        )
