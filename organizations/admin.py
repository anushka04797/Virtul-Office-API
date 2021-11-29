from django.contrib import admin
from organizations.models import Company, Department, Designation, HolidayPlan, Calender, Slc


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'trade_license_number',
    )
    search_fields = ('name', 'trade_license_number')
    ordering = ('name',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'details', 'parent'
    )
    list_filter = ['parent', ]
    list_display_links = ('name',)
    search_fields = ('name', 'details')
    ordering = ('name',)


class DesignationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'details', 'parent'
    )
    list_filter = ['parent', ]
    list_display_links = ('name',)
    search_fields = ('name', 'details')
    ordering = ('name',)


class HolidayPlanAdmin(admin.ModelAdmin):
    list_display = (
        'week_start_day', 'week_holiday_1', 'week_holiday_2'
    )
    list_display_links = ('week_start_day',)
    search_fields = ['week_start_day']
    ordering = ('week_start_day',)


class CalenderAdmin(admin.ModelAdmin):
    list_display = (
        'vacation_title', 'vacation_type', 'start_data', 'end_date', 'duration'
    )
    list_display_links = ('vacation_title',)
    search_fields = ['vacation_title']
    ordering = ('vacation_title',)


class SlcAdmin(admin.ModelAdmin):
    list_display = [
        'employee'
    ]
    list_display_links = ('employee',)
    search_fields = ['employee']
    ordering = ('employee',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Designation, DesignationAdmin)
admin.site.register(HolidayPlan, HolidayPlanAdmin)
admin.site.register(Calender, CalenderAdmin)
admin.site.register(Slc, SlcAdmin)
