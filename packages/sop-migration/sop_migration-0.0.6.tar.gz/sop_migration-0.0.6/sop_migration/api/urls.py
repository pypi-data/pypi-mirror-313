from netbox.api.routers import NetBoxRouter

from sop_migration.api.views import SopMigrationViewSet


app_name = "sop_migrations"

router = NetBoxRouter()
router.register("sop-migrations", SopMigrationViewSet)

urlpatterns = router.urls
