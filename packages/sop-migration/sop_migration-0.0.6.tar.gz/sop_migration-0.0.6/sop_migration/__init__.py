from netbox.plugins import PluginConfig


class SopMigrationConfig(PluginConfig):
    name = "sop_migration"
    verbose_name = "SOP Migration"
    description = "Pin your migrations to any NetBox model instance"
    version = "0.0.6"
    author = "Leorevoir"
    author_email = "leo.quinzler@epitech.eu"
    base_url = "sop-migration"
    min_version = "4.1.0"


config = SopMigrationConfig
