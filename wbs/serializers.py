from rest_framework import serializers
from wbs.models import Wbs
from users.serializers import UserDetailSerializer
from projects.serializers import ProjectDetailsForWbsSerializer
from django.utils import timezone


class CreateWbsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wbs
        fields = (
            'id',
            'project',
            'assignee',
            'reporter',
            'title',
            'description',
            'start_date',
            'end_date',
            'hours_worked',
            'status',
            'progress',
            'comments',
            'deliverable',
            'date_created',
            'date_updated'
        )


class WbsDetailsSerializer(serializers.ModelSerializer):
    reporter = UserDetailSerializer()
    assignee = UserDetailSerializer()
    project = ProjectDetailsForWbsSerializer()

    class Meta:
        model = Wbs
        fields = (
            'id',
            'project',
            'assignee',
            'reporter',
            'title',
            'description',
            'start_date',
            'end_date',
            'hours_worked',
            'status',
            'progress',
            'comments',
            'deliverable',
            'date_created',
            'date_updated'
        )


class WbsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wbs
        fields = (
            'title',
            'description',
            'start_date',
            'end_date',
            'status',
            'progress',
            'comments',
            'deliverable',
            'date_updated'
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.status = validated_data.get('status', instance.status)
        instance.progress = validated_data.get('progress', instance.progress)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.deliverable = validated_data.get('deliverable', instance.deliverable)
        instance.date_updated = validated_data.get('date_updated', timezone.now)
        instance.save()
        return instance
