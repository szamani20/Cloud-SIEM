from django.db import models
from django.utils import timezone
from organization.models import Organization


class Rule(models.Model):
    """
    A rule instance represents one single customer-defined AWS monitoring rule in which a customer
    defines how logs from their AWS account should be inspected for unauthorized access. A rule is represented
    by a JSON (that can be visualized) in which the details of how to inspect logs are defined.
    """
    rule_id = models.AutoField(primary_key=True)

    organization = models.ForeignKey(Organization, models.DO_NOTHING)

    rule_name = models.CharField(max_length=255, blank=True, null=True)
    rule_description = models.TextField(blank=True, null=True)

    # These are not translated to SQL and are not enforced at DB level. MUST be validated at application level.
    rule_types = [
        ('USER_BASED', 'User Based'),
        ('RESOURCE_BASED', 'Resource Based'),
        ('ACTION_BASED', 'Action Based'),
    ]
    rule_type = models.CharField(max_length=100, choices=rule_types)

    rule_content = models.JSONField()

    create_time = models.DateTimeField(default=timezone.now, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'rules'

    def __str__(self):
        return f"{self.rule_id} - {self.organization} - {self.rule_name} - {self.rule_type}"
