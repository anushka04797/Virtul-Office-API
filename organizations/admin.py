from django.contrib import admin
from django.contrib.admin.helpers import Fieldset

from organizations.models import Company, Department, Designation, DmaCalender, HolidayCalender, Slc


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'website', 'vat_certificate'
    )
    search_fields = ('name', 'website')
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


class DmaCalenderAdmin(admin.ModelAdmin):
    fieldsets = (
        (Fieldset, {'fields': ('Company', 'Year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')}),
    )
    # readonly_fields = ('Calculated_hours',)
    list_display = (
        'Company', 'Year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'
    )
    list_display_links = ('Year',)
    search_fields = ['Year']
    ordering = ('Year',)


class HolidayCalenderAdmin(admin.ModelAdmin):
    list_display = (
        'Year', 'holiday_title', 'start_date', 'end_date'
    )
    list_display_links = ('holiday_title',)
    search_fields = ['holiday_title']
    ordering = ('Year',)


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
admin.site.register(DmaCalender, DmaCalenderAdmin)
admin.site.register(HolidayCalender, HolidayCalenderAdmin)
admin.site.register(Slc, SlcAdmin)
