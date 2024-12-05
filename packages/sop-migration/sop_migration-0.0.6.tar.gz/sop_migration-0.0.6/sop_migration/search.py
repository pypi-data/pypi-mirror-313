from netbox.search import SearchIndex, register_search

from sop_migration.models import SopMigration


__all__ = ("SopMigrationSearchIndex",)


@register_search
class SopMigrationSearchIndex(SearchIndex):

    model = SopMigration
    fields = (
        ("object_type", 100),
        ("object_id", 100),
        ("date", 100),
        ("cut", 1000),
        ("impact", 1000),
        ("state", 1000),
        ("description", 500),
        ("comments", 500),
    )
