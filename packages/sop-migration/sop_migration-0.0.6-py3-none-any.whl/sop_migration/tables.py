import django_tables2 as tables
from netbox.tables import NetBoxTable
from sop_migration.models import SopMigration


__all__ = ("SopMigrationTable",)


class SopMigrationTable(NetBoxTable):

    object_type = tables.Column(verbose_name="Object (Type)", linkify=True)
    object_id = tables.Column(verbose_name="Object (ID)", linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SopMigration
        fields = (
            "actions",
            "pk",
            "id",
            "object_type",
            "object_id",
            "date",
            "cut",
            "impact",
            "state",
            "description",
            "comments",
        )
        default_columns = (
            "actions",
            "pk",
            " object_type",
            "object_id",
            "date",
            "description",
        )

    def render_object_id(self, record):
        return record.object_type.get_object_for_this_type(pk=record.object_id)
