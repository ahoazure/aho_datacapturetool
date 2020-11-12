from rest_framework.routers import SimpleRouter
from home import views

router = SimpleRouter()

router.register(
    r'disagregation_categories', views.StgDisagregationCategoryViewSet,
    "disagregation_categories",)
router.register(
    r'data_sources', views.StgDatasourceViewSet, "data_sources")
router.register(
    r'disagregation_options', views.StgDisagregationOptionsViewSet,
    "disagregation_options")
urlpatterns = router.urls
