from django.urls import path

from netbox.views.generic import ObjectChangeLogView, ObjectJournalView

from sop_migration.views import *
from sop_migration.models import *


urlpatterns = (
    path("migration/", SopMigrationListView.as_view(), name="sopmigration_list"),
    path("migration/add/", SopMigrationEditView.as_view(), name="sopmigration_add"),
    path(
        "migration/edit/<int:pk>/",
        SopMigrationEditView.as_view(),
        name="sopmigration_edit",
    ),
    path("migration/<int:pk>/", SopMigrationView.as_view(), name="sopmigration_detail"),
    path(
        "migration/delete/<int:pk>/",
        SopMigrationDeleteView.as_view(),
        name="sopmigration_delete",
    ),
    path(
        "migration/changelog/<int:pk>/",
        ObjectChangeLogView.as_view(),
        name="sopmigration_changelog",
        kwargs={"model": SopMigration},
    ),
    path(
        "migration/journal/<int:pk>/",
        ObjectJournalView.as_view(),
        name="sopmigration_journal",
        kwargs={"model": SopMigration},
    ),
)
