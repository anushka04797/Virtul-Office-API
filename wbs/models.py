from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from projects.models import Projects
from users.models import CustomUser


class Wbs(models.Model):
    project = models.ForeignKey(Projects, related_name="pro_details", blank=False, null=False,
                                on_delete=models.CASCADE)
    assignee = models.ForeignKey(CustomUser, related_name="employee_assigned", blank=False, null=False,
                                 on_delete=models.CASCADE)
    reporter = models.ForeignKey(CustomUser, related_name="wbs_reporter", blank=False, null=False,
                                 on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=50, blank=False)
    description = models.TextField(_('description'), max_length=150, blank=True)
    start_date = models.DateField(_('start date'), blank=False)
    end_date = models.DateField(_('end date'), blank=False)
    hours_worked = models.DecimalField(_('hours worked'), max_digits=6, decimal_places=1, blank=False)
    status = models.IntegerField(_('wbs status'), default=True, blank=False)
    progress = models.IntegerField(_('progress percentage'), default=True, blank=False)
    comments = models.TextField(_('comments'), max_length=150, blank=True)
    deliverable = models.CharField(_('deliverable'), max_length=50, blank=True)
    date_created = models.DateField(_('date created'), default=timezone.now)
    date_updated = models.DateField(_('date updated'), default=timezone.now)

    class Meta:
        db_table = 'wbs'
        verbose_name = _('wbs')
        verbose_name_plural = _('wbss')
        indexes = [
            models.Index(fields=['title', ])
        ]
        indexes = [
            models.Index(fields=['project', ])
        ]
        indexes = [
            models.Index(fields=['assignee', ])
        ]
        indexes = [
            models.Index(fields=['reporter', ])
        ]

    def __str__(self):
        return self.title