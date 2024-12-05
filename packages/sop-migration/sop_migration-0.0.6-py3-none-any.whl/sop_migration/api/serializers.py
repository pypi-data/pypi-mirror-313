from rest_framework import serializers

from core.models import ObjectType
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer

from sop_migration.models import SopMigration


__all__ = ("SopMigrationSerializer",)


class SopMigrationSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:sop_migration-api:sopmigration-detail"
    )
    object_type = ContentTypeField(queryset=ObjectType.objects.all())

    class Meta:
        model = SopMigration
        fields = (
            "id",
            "url",
            "display",
            "object_type",
            "object_id",
            "date",
            "cut",
            "impact",
            "state",
            "description",
            "comments",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "date", "description")
