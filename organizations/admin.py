from django.contrib import admin
from organizations.models import Company, Department, Designation, HolidayPlan, Calender, Slc


class CompanyAdmin():
    list_display = (
        'name',  'license_number',
    )
    list_display_links = ('name',)
    search_fields = ('name', 'license_number')
    ordering = ('name',)


class DepartmentAdmin():
    list_display = (
        'name',  'details',
    )
    list_display_links = ('name',)
    search_fields = ('name', 'details')
    ordering = ('name',)


class DesignationAdmin():
    list_display = (
        'name',  'details',
    )
    list_display_links = ('name',)
    search_fields = ('name', 'details')
    ordering = ('name',)


class HolidayPlanAdmin(admin.ModelAdmin):
    list_display = (
        'week_start_day'
    )
    list_display_links = ('week_start_day',)
    search_fields = ('week_start_day')
    ordering = ('week_start_day',)


class CalenderAdmin(admin.ModelAdmin):
    list_display = (
        'vacation_title'
    )
    list_display_links = ('vacation_title',)
    search_fields = ('vacation_title')
    ordering = ('vacation_title',)


class SlcAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id'
    )
    list_display_links = ('employee_id',)
    search_fields = ('employee_id')
    ordering = ('employee_id',)

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(HolidayPlan)
admin.site.register(Calender)
admin.site.register(Slc)