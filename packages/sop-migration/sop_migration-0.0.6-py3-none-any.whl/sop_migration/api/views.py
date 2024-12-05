from netbox.api.metadata import ContentTypeMetadata
from netbox.api.viewsets import NetBoxModelViewSet

from sop_migration.api.serializers import SopMigrationSerializer
from sop_migration.models import SopMigration


__all__ = ("SopMigrationViewSet",)


class SopMigrationViewSet(NetBoxModelViewSet):

    metadata_class = ContentTypeMetadata
    queryset = SopMigration.objects.all()
    serializer_class = SopMigrationSerializer
