from django.db import models
from django.utils import timezone


class Organization(models.Model):
    """
    An organization instance is used to represent a customer's AWS account. Each customer can have multiple
    organizations with different AWS account_ids
    """
    organization_id = models.BigAutoField(primary_key=True)
    organization_name = models.CharField(max_length=255)
    organization_account_id = models.CharField(max_length=255)
    create_time = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        # managed = False
        db_table = 'organizations'

        unique_together = [['organization_name']]

    def __str__(self):
        return f"{self.organization_id} : {self.organization_name} - {self.organization_account_id}"
