from django.urls import reverse
from django.db import models

from utilities.choices import ChoiceSet
from core.models.contenttypes import ObjectType
from netbox.models import NetBoxModel


__all__ = ("SopMigration",)


class MigrationStateChoices(ChoiceSet):

    CHOICES = (
        ("unknown", "Unknown", "gray"),
        ("choix1", "Choix1", "green"),
        ("choix2", "Choix2", "red"),
    )


class SopMigration(NetBoxModel):

    # object to pin (type + ID)
    object_type = models.ForeignKey(
        to=ObjectType, on_delete=models.CASCADE, verbose_name="Object (Type)"
    )
    object_id = models.PositiveBigIntegerField(verbose_name="Object (ID)")

    # attributes
    date = models.DateTimeField(verbose_name="Migration date")
    cut = models.PositiveBigIntegerField()
    impact = models.PositiveBigIntegerField()
    state = models.CharField(choices=MigrationStateChoices)
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)

    class Meta(NetBoxModel.Meta):
        ordering = ("object_type", "pk", "date")
        verbose_name = "Migration"
        verbose_name_plural = "Migrations"

    def __str__(self) -> str:
        try:
            app = self.object_type.app_label.upper()
            obj = self.object_type.get_object_for_this_type(id=self.object_id)
            return f"{app} | {obj} Migration - {self.date}"
        except:
            return "Migration"

    def get_absolute_url(self):
        return reverse("plugins:sop_migration:sopmigration_detail", args=[self.pk])
