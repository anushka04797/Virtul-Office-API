from django.contrib import admin
from django.contrib.admin.helpers import Fieldset
from organizations.models import Company, Department, Designation, DmaCalender, HolidayCalender, Slc
from users.models import CustomUser
from organizations.forms import CustomAddSLCForm, CustomEditSLCForm


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
        'Company', 'Year', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'total'
    )
    list_display_links = ('Year',)
    search_fields = ['Year']
    ordering = ('Year',)

    def january(self, obj):
        return obj.January * 8

    def february(self, obj):
        return obj.February * 8

    def march(self, obj):
        return obj.March * 8

    def april(self, obj):
        return obj.April * 8

    def may(self, obj):
        return obj.May * 8

    def june(self, obj):
        return obj.June * 8

    def july(self, obj):
        return obj.July * 8

    def august(self, obj):
        return obj.August * 8

    def september(self, obj):
        return obj.September * 8

    def october(self, obj):
        return obj.October * 8

    def november(self, obj):
        return obj.November * 8

    def december(self, obj):
        return obj.December * 8

    def total(self, obj):
        return (obj.January + obj.February + obj.March + obj.April + obj.May + obj.June + obj.July + obj.August + obj.September + obj.October + obj.November + obj.December) * 8


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
    search_fields = ['hourly_rate', 'employee__first_name', 'employee__last_name', 'employee__email']
    ordering = ('employee',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["employee"]
        else:
            return []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            kwargs["queryset"] = CustomUser.objects.filter(slc_details=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Designation, DesignationAdmin)
admin.site.register(DmaCalender, DmaCalenderAdmin)
admin.site.register(HolidayCalender, HolidayCalenderAdmin)
admin.site.register(Slc, SlcAdmin)
