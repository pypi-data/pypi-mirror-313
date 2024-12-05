import logging

from django.apps import apps
from django.conf import settings
from django.http import HttpResponse

from netbox.plugins import PluginTemplateExtension

from sop_migration.models import SopMigration


ALLOWED_POSITIONS = ["left_page", "right_page"]


# overrides NetBox PluginTemplateExtension method to display
# the right panel according to PLUGINS_CONFIG in configuration.py
def create_new_panel(self) -> HttpResponse:

    def get_extra_context() -> dict:
        return {"migration": SopMigration}

    return self.render(self.template_name, get_extra_context())


class SopMigrationDashboard:

    template_name = "sop_migration/panel.html"
    settings = settings.PLUGINS_CONFIG.get("sop_migration", {})

    def __init__(self) -> None:
        self.extensions = self.get_display_extensions()

    def get_display_position(self, model, _display) -> str | None:

        if exists := _display.get(model):

            if exists not in ALLOWED_POSITIONS:
                return None

            return exists

        return None

    def get_display_extensions(self) -> list | None:

        extensions = []
        _display = self.settings.get("display")

        if _display is None:
            return None

        # check if display is in intended format {model:position}
        if not isinstance(_display, dict):
            logging.error(f'Invalid syntax "{_display}" must be a dict.')
            return None

        # iterate existing application models
        for app_model in apps.get_models():

            # format object into something else than <class>
            model = app_model._meta.model_name

            if model not in _display:
                continue

            # get and check position in {model:position}
            position = self.get_display_position(model, _display)
            if position is None:
                logging.error(
                    f'Invalid position "{position}" is not a valid choice between {ALLOWED_POSITIONS}.'
                )
                return None

            new_class = type(
                f"{model}_migration_extension",
                (PluginTemplateExtension,),
                {
                    "template_name": self.template_name,
                    "model": f"{app_model._meta.app_label}.{model}",
                    position: create_new_panel,
                },
            )
            extensions.append(new_class)

        return extensions

    def push(self) -> list[object] | None:
        return self.extensions or None


template_extensions = SopMigrationDashboard().push()
