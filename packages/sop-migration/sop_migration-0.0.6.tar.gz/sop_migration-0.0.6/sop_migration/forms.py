from django.forms import DateTimeField, IntegerField, ChoiceField
from django.test.utils import require_jinja2

from core.models.contenttypes import ObjectType
from utilities.forms.utils import add_blank_choice
from utilities.forms.fields import CommentField, DynamicModelMultipleChoiceField
from utilities.forms.widgets import DateTimePicker
from utilities.forms.widgets.apiselect import APISelectMultiple
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm

from sop_migration.models import MigrationStateChoices, SopMigration


__all__ = ("SopMigrationForm", "SopMigrationFilterSetForm")


class SopMigrationForm(NetBoxModelForm):

    date = DateTimeField(label="Migration date", widget=DateTimePicker())
    comments = CommentField()

    class Meta:
        model = SopMigration
        fields = [
            "object_type",
            "object_id",
            "date",
            "cut",
            "impact",
            "state",
            "description",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "tags" in self.fields:
            del self.fields["tags"]


class SopMigrationFilterSetForm(NetBoxModelFilterSetForm):
    model = SopMigration
    object_type = DynamicModelMultipleChoiceField(
        queryset=ObjectType.objects.all(),
        required=False,
        label="Object (Type)",
        widget=APISelectMultiple(api_url=f"/api/extras/object-types/"),
    )
    date = DateTimeField(
        required=False, label="Migration date", widget=DateTimePicker()
    )
    cut = IntegerField(required=False)
    state = ChoiceField(choices=add_blank_choice(MigrationStateChoices), required=False)
