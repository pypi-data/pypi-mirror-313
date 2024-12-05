from django.db.models.query import InstanceCheckMeta
from netbox.views import generic

from sop_migration.models import SopMigration
from sop_migration.forms import SopMigrationForm, SopMigrationFilterSetForm
from sop_migration.tables import SopMigrationTable
from sop_migration.filtersets import SopMigrationFilterSet


__all__ = (
    "SopMigrationView",
    "SopMigrationListView",
    "SopMigrationEditView",
    "SopMigrationDeleteView",
)


class SopMigrationView(generic.ObjectView):

    queryset = SopMigration.objects.all()

    def get_extra_context(self, request, instance) -> dict:
        context = super().get_extra_context(request, instance)
        pk = instance.object_id
        obj = instance.object_type

        # get model by ID
        context["model_name"] = obj.get_object_for_this_type(pk=pk)

        return {**context}


class SopMigrationListView(generic.ObjectListView):

    queryset = SopMigration.objects.all()
    table = SopMigrationTable
    filterset = SopMigrationFilterSet
    filterset_form = SopMigrationFilterSetForm


class SopMigrationEditView(generic.ObjectEditView):

    queryset = SopMigration.objects.all()
    form = SopMigrationForm

    def get_extra_context(self, request, instance):
        context: dict = super().get_extra_context(request, instance)

        return context

    def get_extra_addanother_params(self, request):

        return {"object_type": self.object_type, "object_id": self.object_id}

    def get(self, request, *args, **kwargs):
        self.object_type = request.GET.get("object_type")
        self.object_id = request.GET.get("object_id")

        return super().get(request, *args, **kwargs)


class SopMigrationDeleteView(generic.ObjectDeleteView):

    queryset = SopMigration.objects.all()
