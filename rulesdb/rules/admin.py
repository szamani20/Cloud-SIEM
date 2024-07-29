from django.contrib import admin

from rules.models import Rule


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('rule_id', 'organization', 'rule_name', 'rule_type', 'create_time')
    list_filter = ('organization', 'rule_type', 'create_time')
    search_fields = ('organization__organization_name', 'organization__organization_account_id', 'rule_name', 'rule_description')
    ordering = ('-create_time',)
