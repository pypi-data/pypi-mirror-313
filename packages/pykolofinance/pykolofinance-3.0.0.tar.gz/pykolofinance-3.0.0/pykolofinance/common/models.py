import uuid
from django.db import models

from .kgs import generate_unique_id


class AuditableModel(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=generate_unique_id, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
