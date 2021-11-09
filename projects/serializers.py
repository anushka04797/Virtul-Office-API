import datetime

from rest_framework import serializers
from django.utils import timezone
from .models import Projects, ProjectAssignee, Tdo, ProjectSharedFiles
from users.serializers import UserDetailSerializer


class TdoSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p",read_only=True)
    date_updated = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p",read_only=True)

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


class ProjectDetailsSerializer(serializers.ModelSerializer):
    task_delivery_order = TdoSerializer()

    # assignee = UserDetailSerializer()
    pm = UserDetailSerializer()
    planned_delivery_date = serializers.DateField(format="%Y-%m-%d",read_only=True)
    date_created = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p",read_only=True)
    date_updated = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p",read_only=True)

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


class TaskSerializer(serializers.ModelSerializer):
    task_delivery_order = TdoSerializer()
    date_created = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p")
    date_updated = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p")

    class Meta:
        model = Projects
        fields = (
            'id',
            'task_delivery_order',
            'sub_task',
            'work_package_number',
            'task_title',
            'work_package_index',
            'estimated_person',
            'status',
            'date_created',
            'date_updated',
        )


class SubTaskSerializer(serializers.ModelSerializer):
    task_delivery_order = TdoSerializer()

    # assignee = UserDetailSerializer()
    pm = UserDetailSerializer()
    planned_delivery_date = serializers.DateField(format="%Y-%m-%d")
    date_created = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p")
    date_updated = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p")

    class Meta:
        model = Projects
        fields = (
            'id',
            'task_delivery_order',
            'sub_task',
            'work_package_number',
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


class CreateProjectAssigneeSerializer(serializers.ModelSerializer):
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


class ProjectAssigneeSerializer(serializers.ModelSerializer):
    assignee = UserDetailSerializer(read_only=True)
    project = ProjectDetailsSerializer(read_only=True)
    date_created = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p", read_only=True)
    date_updated = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p", read_only=True)

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


class UpdateProjectSerializer(serializers.ModelSerializer):
    planned_delivery_date = serializers.DateField(format="%Y-%m-%d")
    date_updated = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p",required=False)

    class Meta:
        model = Projects
        fields = (
            'id',
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
        instance.status = validated_data.get('status', instance.status)
        instance.date_updated = timezone.now()
        instance.save()
        return instance


class UpdateProjectRemainingHrsSerializer(serializers.ModelSerializer):
    date_updated = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p", required=False)

    class Meta:
        model = Projects
        fields = (
            'remaining_hours',
            'date_updated'
        )

    def update(self, instance, validated_data):
        instance.remaining_hours = validated_data.get('remaining_hours', instance.remaining_hours)
        instance.date_updated = timezone.now()
        instance.save()
        return instance


class UpdateSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = (
            'id',
            'sub_task'
        )

    def update(self, instance, validated_data):
        instance.sub_task = validated_data.get('sub_task', instance.sub_task)
        instance.save()
        return instance


class ProjectDetailsForWbsSerializer(serializers.ModelSerializer):
    task_delivery_order = TdoSerializer()

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
            'pm',
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


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSharedFiles
        fields = (
            'id',
            'file',
            'date_created'
        )

class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSharedFiles
        fields = (
            'id',
            'project',
            'file',
        )
class ProjectWiseFileListSerializer(serializers.ModelSerializer):
    project_file = DocumentListSerializer(many=True)
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
            'pm',
            'planned_hours',
            'remaining_hours',
            'status',
            'project_file',
        )
