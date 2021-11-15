from django.db import models
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    name = models.CharField(_('company name'), max_length=150, blank=False)
    details = models.TextField(_('company details'), max_length=350, blank=True)
    license_number = models.CharField(_('license number'), max_length=150, blank=True)

    class Meta:
        db_table = 'company'
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def __str__(self):
        return self.name


class Department(models.Model):
    company = models.ForeignKey(Company, blank=False, null=False, on_delete=models.PROTECT)
    name = models.CharField(_('department name'), max_length=150, blank=False)
    details = models.TextField(_('department details'), max_length=350, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.PROTECT)

    class Meta:
        db_table = 'department'
        verbose_name = _('department')
        verbose_name_plural = _('departments')

    def __str__(self):
        return self.name


class Designation(models.Model):
    department = models.ForeignKey(Department, blank=False, null=False, on_delete=models.PROTECT)
    name = models.CharField(_('designation name'), max_length=150, blank=False)
    details = models.TextField(_('designation details'), max_length=350, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.PROTECT)

    class Meta:
        db_table = 'designation'
        verbose_name = _('designation')
        verbose_name_plural = _('designations')

    # def __str__(self):
    #     return self.name


class HolidayPlan(models.Model):
    WEEK_DAYS = (
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    week_start_day = models.CharField(_('Select week start day'), max_length=20, choices=WEEK_DAYS, default='Select',
                                      blank=False, null=False)
    week_holiday_1 = models.CharField(_('Select week holiday 1'), max_length=20, choices=WEEK_DAYS, default='Select',
                                      blank=False, null=False)
    week_holiday_2 = models.CharField(_('Select week holiday 2'), max_length=20, choices=WEEK_DAYS, default='Select',
                                      blank=False, null=True)
    government_holidays = models.IntegerField(_('government holidays'), blank=True, null=True)
    company_reserved_holidays = models.IntegerField(_('company\'s reserved holidays'), blank=True, null=True)
    allocated_leave_per_year = models.IntegerField(_('allocated leave per head in a year'), blank=True, null=True)

    class Meta:
        db_table = 'holiday_and_vacation_plan'
        verbose_name = _('holiday_and_vacation_plan')
        verbose_name_plural = _('holiday_and_vacation_plans')

    def __str__(self):
        return self.week_start_day


class Calender(models.Model):
    MONTHS = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )
    VACATION_TYPE = (
        ('Government', 'Government'),
        ('Reserved', 'Reserved'),
    )
    Year = models.CharField(_('Year'), max_length=20, blank=False, null=False)
    Month = models.CharField(_('Month'), max_length=20, choices=MONTHS, default='Select', blank=False, null=False)
    vacation_title = models.CharField(_('vacation title'), max_length=120, blank=False, null=False)
    vacation_type = models.CharField(_('select vacation type'), max_length=20, choices=VACATION_TYPE, default='Select',
                                     blank=False, null=True)
    start_data = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    duration = models.DurationField()

    class Meta:
        db_table = 'calender'
        verbose_name = _('calender')
        verbose_name_plural = _('calenders')

    def __str__(self):
        return self.Month


class Slc(models.Model):
    employee = models.ForeignKey(to='users.CustomUser', blank=False, null=False, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, blank=False, null=False, on_delete=models.PROTECT)
    designation = models.ForeignKey(Designation, blank=False, null=False, on_delete=models.PROTECT)
    salary = models.IntegerField(_('salary'), blank=False, null=False)
    hourly_rate = models.IntegerField(_('hourly rate'), blank=False, null=False)

    class Meta:
        db_table = 'slc'
        verbose_name = _('slc')
        verbose_name_plural = _('slcs')

    # def __str__(self):
    #     return self.employee.first_name + " " + self.employee.last_name
