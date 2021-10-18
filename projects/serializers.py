from rest_framework import serializers
from django.utils import timezone
from .models import Projects, ProjectAssignee, Tdo
from users.serializers import UserDetailSerializer


class CreateTdoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tdo
        fields = (
            'id',
            'title',
            'date_created',
            'date_updated'
        )


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = (
            'id', 
            'task_delivery_order', 
            'sub_task', 
            'work_package_number', 
            'work_package_index', 
            'task_title', 
            'estimated_person', 
            'planned_delivery_date',
            'pm',
            'planned_hours', 
            'planned_value', 
            'remaining_hours',
            'status',
            'date_created',
            'date_updated'
        )


class ProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssignee
        fields = (
            'id',
            'assignee',
            'is_assignee_active',
            'project',
            'date_created',
            'date_updated'
        )


class ProjectDetailsSerializer(serializers.ModelSerializer):

    task_delivery_order = CreateTdoSerializer()

    # assignee = UserDetailSerializer()
    pm = UserDetailSerializer()
    planned_delivery_date = serializers.DateTimeField(format="%d-%m-%Y")
    date_created = serializers.DateTimeField(format="%d-%m-%Y %I:%M:%S %p")
    date_updated = serializers.DateTimeField(format="%d-%m-%Y %I:%M:%S %p")

    class Meta:
        model = Projects
        fields = (
            'id',
            'task_delivery_order',
            'sub_task',
            'work_package_number',
            'work_package_index',
            'task_title',
            'estimated_person',
            'planned_delivery_date',
            'pm',
            'planned_hours',
            'planned_value',
            'remaining_hours',
            'status',
            'date_created',
            'date_updated',
        )


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = (
            'task_title',
            'estimated_person',
            'planned_delivery_date',
            'planned_hours',
            'planned_value',
            'remaining_hours',
            'status',
            'date_updated'
        )

    def update(self, instance, validated_data):
        instance.task_title = validated_data.get('task_title', instance.task_title)
        instance.estimated_person = validated_data.get('estimated_person', instance.estimated_person)
        instance.planned_delivery_date = validated_data.get('planned_delivery_date', instance.planned_delivery_date)
        instance.planned_hours = validated_data.get('planned_hours', instance.planned_hours)
        instance.planned_value = validated_data.get('planned_value', instance.planned_value)
        instance.remaining_hours = validated_data.get('remaining_hours', instance.remaining_hours)
        instance.date_updated = validated_data.get('date_updated', timezone.now)
        instance.save()
        return instance


class ProjectDetailsForWbsSerializer(serializers.ModelSerializer):
    assignee = UserDetailSerializer()

    class Meta:
        model = Projects
        fields = (
            'id',
            'task_delivery_order',
            'sub_task',
            'work_package_number',
            'work_package_index',
            'task_title',
            'planned_delivery_date',
            'assignee',
            'pm',
            'is_assignee_active',
            'planned_hours',
            'remaining_hours',
            'status',
        )


# class AddAssigneeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Projects
#         fields = (
#             'task_title',
#             'estimated_person',
#             'planned_delivery_date',
#             'planned_hours',
#             'planned_value',
#             'remaining_hours',
#         )

#     def update(self, instance, validated_data):
#         instance.task_title = validated_data.get('task_title', instance.task_title)
#         instance.estimated_person = validated_data.get('estimated_person', instance.estimated_person)
#         instance.planned_delivery_date = validated_data.get('planned_delivery_date', instance.planned_delivery_date)
#         instance.planned_hours = validated_data.get('planned_hours', instance.planned_hours)
#         instance.planned_value = validated_data.get('planned_value', instance.planned_value)
#         instance.remaining_hours = validated_data.get('remaining_hours', instance.remaining_hours)
#         instance.save()
#         return instance
