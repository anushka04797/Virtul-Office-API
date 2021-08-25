from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from projects.models import Projects
from users.models import CustomUser


class Meetings(models.Model):
    room_id = models.CharField(max_length=12, blank=False, null=False)
    participant = models.CharField(_('participants'), max_length=150, blank=False, null=False)
    project = models.ForeignKey(Projects, related_name="meeting_project_details", blank=False, null=False,
                                 on_delete=models.CASCADE)
    agenda = models.TextField(_('meeting agenda'), max_length=150, blank=True)
    comments =  models.TextField(_('meeting comments'), max_length=150, blank=True)
    start_time = models.DateTimeField(_('meeting start time'), blank=False)
    end_time = models.DateTimeField(_('meeting end time'), blank=False)
    duration = models.IntegerField(_('planned value'), blank=True)
    date_created = models.DateField(_('date created'), default=timezone.now)
    date_updated = models.DateField(_('date updated'), default=timezone.now)

    class Meta:
        db_table = 'meeting'
        verbose_name = _('meeting')
        verbose_name_plural = _('meetings')

    def __str__(self):
        return self.project.room_id
