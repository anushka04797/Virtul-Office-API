from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import CustomUser


class Projects(models.Model):
    task_delivery_order = models.CharField(_('task delivery order'), max_length=50, blank=False)
    sub_task = models.CharField(_('subtask name'), max_length=50, blank=True)
    work_package_number = models.IntegerField(_('work package number'), blank=True)
    work_package_index = models.DecimalField(_('work package index'), max_digits=7, decimal_places=1, blank=True,
                                             null=True)
    task_title = models.CharField(_('task title'), max_length=150, blank=True)
    estimated_person = models.DecimalField(_('estimated person'), max_digits=4, decimal_places=2, blank=True)
    planned_delivery_date = models.DateField(_('planned delivery date'), blank=False)
    assignee = models.ForeignKey(CustomUser, related_name="project_assignee", blank=False, null=False,
                                 on_delete=models.CASCADE)
    pm = models.ForeignKey(CustomUser, related_name="project_manager", blank=False, null=True,
                                 on_delete=models.CASCADE)
    is_assignee_active = models.BooleanField(_('task title'), default=True, blank=False)
    planned_hours = models.DecimalField(_('planned hours'), max_digits=6, decimal_places=1, blank=False)
    planned_value = models.IntegerField(_('planned value'), blank=True)
    remaining_hours = models.DecimalField(_('remaining hours'), max_digits=6, decimal_places=1, blank=False)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    date_updated = models.DateTimeField(_('date updated'), default=timezone.now)

    class Meta:
        db_table = 'project'
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        indexes = [
            models.Index(fields=['work_package_index', ])
        ]

    def __str__(self):
        return self.task_delivery_order
