from django.contrib import admin

from logs.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'organization', 'create_time')
    list_filter = ('organization', 'create_time')
    search_fields = ('organization__organization_name', 'organization__organization_account_id', 'log_content')
    ordering = ('-create_time',)
