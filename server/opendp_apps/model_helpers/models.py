"""Abstract Convenience classes"""
import uuid
from django.db import models

class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimestampedModelWithUUID(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False
    )
    class Meta:
        abstract = True


