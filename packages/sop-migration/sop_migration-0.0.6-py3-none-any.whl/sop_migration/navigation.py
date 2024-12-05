from netbox.navigation import *
from netbox.navigation.menu import MENUS


MIGRATION = Menu(
    label="Migration",
    icon_class="mdi mdi-cog-transfer",
    groups=(
        MenuGroup(
            label="SOP-Migration",
            items=(
                MenuItem(
                    link=f"plugins:sop_migration:sopmigration_list",
                    link_text="Migrations",
                    permissions=[f"sop_migration.view_sopmigration"],
                    buttons=(
                        MenuItemButton(
                            link=f"plugins:sop_migration:sopmigration_add",
                            title="Add",
                            icon_class="mdi mdi-plus-thick",
                            permissions=[f"sop_migration.add_sopmigration"],
                        ),
                    ),
                ),
            ),
        ),
    ),
)


MENUS.append(MIGRATION)
