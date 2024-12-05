from django.db.models import Q
from core.models.contenttypes import ObjectType
from netbox.filtersets import NetBoxModelFilterSet
from sop_migration.models import SopMigration


__all__ = ("SopMigrationFilterSet",)


class SopMigrationFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = SopMigration
        fields = ("id", "object_type", "object_id", "date", "state", "impact")

    def search_object_name(self, queryset, value):
        valid_ids: list[int] = []

        for instance in queryset:
            obj = ObjectType.objects.get(pk=instance.object_type_id)
            target = obj.get_object_for_this_type(pk=instance.object_id)

            if value in target.__str__():
                valid_ids.append(instance.id)
                continue

            elif value in str(instance.date.__str__()):
                valid_ids.append(instance.id)
                continue

        return queryset.filter(id__in=valid_ids)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        query = self.search_object_name(queryset, value)
        if query is not None:
            return query

        return queryset.filter(
            Q(object_type__id__icontains=value)
            | Q(object_id__icontains=value)
            | Q(description__icontains=value)
            | Q(comments__icontains=value)
        )
