from django.contrib import admin

from organization.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_id', 'organization_name', 'organization_account_id', 'create_time')
    search_fields = ('organization_name', 'organization_account_id')
    ordering = ('-create_time',)
