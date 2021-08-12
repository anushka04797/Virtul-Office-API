from rest_framework import serializers
from .models import Projects
from users.serializers import UserDetailSerializer


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
            'assignee',
            'is_assignee_active',
            'planned_hours', 
            'planned_value', 
            'remaining_hours'
        )


class ProjectDetailsSerializer(serializers.ModelSerializer):
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
            'estimated_person',
            'planned_delivery_date',
            'assignee',
            'is_assignee_active',
            'planned_hours',
            'planned_value',
            'remaining_hours',
        )


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = (
            'task_title',
            'estimated_person',
            'planned_delivery_date',
            'planned_hours',
            'planned_value',
            'remaining_hours',
        )

    def update(self, instance, validated_data):
        instance.task_title = validated_data.get('task_title', instance.task_title)
        instance.estimated_person = validated_data.get('estimated_person', instance.estimated_person)
        instance.planned_delivery_date = validated_data.get('planned_delivery_date', instance.planned_delivery_date)
        instance.planned_hours = validated_data.get('planned_hours', instance.planned_hours)
        instance.planned_value = validated_data.get('planned_value', instance.planned_value)
        instance.remaining_hours = validated_data.get('remaining_hours', instance.remaining_hours)
        instance.save()
        return instance


class AddAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = (
            'task_title',
            'estimated_person',
            'planned_delivery_date',
            'planned_hours',
            'planned_value',
            'remaining_hours',
        )

    def update(self, instance, validated_data):
        instance.task_title = validated_data.get('task_title', instance.task_title)
        instance.estimated_person = validated_data.get('estimated_person', instance.estimated_person)
        instance.planned_delivery_date = validated_data.get('planned_delivery_date', instance.planned_delivery_date)
        instance.planned_hours = validated_data.get('planned_hours', instance.planned_hours)
        instance.planned_value = validated_data.get('planned_value', instance.planned_value)
        instance.remaining_hours = validated_data.get('remaining_hours', instance.remaining_hours)
        instance.save()
        return instance
