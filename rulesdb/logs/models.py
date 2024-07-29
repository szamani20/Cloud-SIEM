from django.db import models
from django.utils import timezone
from organization.models import Organization


class Log(models.Model):
    """
    A log instance is used to permanently save an AWS generated log by customers, for retention, inspection,
    and analytics purposes
    """
    log_id = models.AutoField(primary_key=True)

    organization = models.ForeignKey(Organization, models.DO_NOTHING)

    log_content = models.JSONField()

    create_time = models.DateTimeField(default=timezone.now, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'logs'

    def __str__(self):
        return f"{self.log_id} - {self.organization} - {self.create_time}"
