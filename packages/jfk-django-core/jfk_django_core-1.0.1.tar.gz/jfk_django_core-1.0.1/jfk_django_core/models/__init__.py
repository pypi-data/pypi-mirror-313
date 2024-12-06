import uuid

from django.db import models


class UuidModel(models.Model):
    """Base Model with uuid."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.id}"
